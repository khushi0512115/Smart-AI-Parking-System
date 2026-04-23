# 🚗 Smart Parking System using AI

## 📌 Overview

This project is a Smart Parking System that uses Artificial Intelligence and Computer Vision to detect parking availability in real time. It helps reduce traffic congestion, saves time, and improves parking efficiency.

---

## 🎯 Features

* 🔐 User Login & Registration
* 🎥 Real-time vehicle detection using YOLO
* 📊 Live dashboard (Free / Occupied slots)
* 🗺️ Integrated map view (OpenStreetMap + Leaflet)
* 📈 Analytics with charts
* 🎛️ Start/Stop camera control

---

## 🧠 Technologies Used

* Python
* Flask (Backend)
* OpenCV (Image Processing)
* YOLO (Object Detection)
* SQLite (Database)
* HTML, CSS, JavaScript
* Leaflet (Map)

---

## ⚙️ How It Works

1. Camera/video captures parking area
2. YOLO model detects vehicles
3. System calculates free and occupied slots
4. Data is stored in database
5. Dashboard and map update in real time

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/smart-parking-ai.git
cd smart-parking-ai
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Project

```bash
python app.py
```

---

## 🌐 Access the App

Open in browser:

```
http://127.0.0.1:5000
```

---

## 📊 Project Structure

```
app.py            -> Main Flask app  
detector.py       -> AI detection logic  
database.py       -> Database handling  
templates/        -> HTML pages  
static/           -> CSS & assets  
```

---

## 🔮 Future Scope

* Mobile app integration
* Parking booking system
* Cloud deployment
* IoT-based smart parking

---

## 👨‍💻 Author

Khushi Garg

---

## ⭐ If you like this project, give it a star!
