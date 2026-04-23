
from flask import Flask, render_template, Response, jsonify, request, redirect, session
import cv2
import sqlite3
import numpy as np
import atexit
import sys

from detector import detect_parking
from database import init_db, insert_log

app = Flask(__name__)
app.secret_key = "secret123"

# -------------------------------
# 🎥 HYBRID MODE
# -------------------------------
VIDEO_SOURCE = 0
if len(sys.argv) > 1:
    VIDEO_SOURCE = sys.argv[1]

cap = cv2.VideoCapture(VIDEO_SOURCE)

# -------------------------------
# 🧠 GLOBAL STATE
# -------------------------------
camera_running = True

latest_data = {
    "total": 0,
    "free": 0,
    "occupied": 0
}

init_db()

# -------------------------------
# 🎥 VIDEO STREAM
# -------------------------------
def gen_frames():
    global latest_data, camera_running

    while True:

        # 🛑 If stopped → show blank screen
        if not camera_running:
            blank = 255 * np.ones((600, 800, 3), dtype=np.uint8)
            cv2.putText(blank, "Camera Stopped", (200,300),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

            ret, buffer = cv2.imencode('.jpg', blank)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            continue

        success, frame = cap.read()

        # 🔁 Loop video
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = cv2.resize(frame, (800, 600))

        frame, free, occupied = detect_parking(frame)

        insert_log(free, occupied)

        # 📊 Update data
        latest_data = {
            "total": free + occupied,
            "free": free,
            "occupied": occupied
        }

        cv2.putText(frame, f"Free: {free}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.putText(frame, f"Occupied: {occupied}", (20,80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# -------------------------------
# 🔐 AUTH SYSTEM
# -------------------------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("parking.db")
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username,password) VALUES (?,?)",
                      (username, password))
            conn.commit()
        except:
            return "User already exists"

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("parking.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, password))

        user = c.fetchone()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid login"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/analytics-data')
def analytics_data():
    from database import get_logs

    logs = get_logs()

    timestamps = [row[0] for row in logs]
    free = [row[1] for row in logs]
    occupied = [row[2] for row in logs]

    return jsonify({
        "labels": timestamps,
        "free": free,
        "occupied": occupied
    })


# -------------------------------
# 🌐 PAGES
# -------------------------------
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html')


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')


@app.route('/slots')
def slots():
    return render_template('slots.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/map')
def map_view():
    return render_template('map.html')


# -------------------------------
# 🎥 VIDEO ROUTE
# -------------------------------
@app.route('/video')
def video():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# -------------------------------
# 📊 STATUS API
# -------------------------------
@app.route('/status')
def status():
    return jsonify(latest_data)


# -------------------------------
# 🎛️ CONTROL BUTTONS
# -------------------------------
@app.route('/start')
def start_camera():
    global camera_running
    camera_running = True
    return jsonify({"status": "started"})


@app.route('/stop')
def stop_camera():
    global camera_running
    camera_running = False
    return jsonify({"status": "stopped"})


# -------------------------------
# 🧹 CLEANUP
# -------------------------------
def cleanup():
    cap.release()
    cv2.destroyAllWindows()

atexit.register(cleanup)


# -------------------------------
# 🚀 RUN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)