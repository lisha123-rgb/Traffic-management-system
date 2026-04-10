# Traffic-management-system
# 🚦 Traffic Management System using YOLOv8

## 📌 Overview

This project implements a **smart traffic management system** using **YOLOv8 (Ultralytics)** for real-time vehicle detection and analysis.

The system processes a traffic video, detects vehicles, counts them, divides them into lanes, and dynamically assigns a **green signal** to the lane with the highest traffic density.

---

## 🎯 Features

* 🚗 Real-time vehicle detection using YOLOv8
* 🔢 Vehicle counting
* 🛣️ Lane-wise vehicle distribution
* 🚦 Smart traffic signal control
* 📊 Traffic density classification (Low / Medium / High)
* 🖥️ Visual output with annotations

---

## 🧠 How It Works

1. Video is read frame-by-frame using OpenCV
2. YOLOv8 detects objects in each frame
3. Only vehicle classes are considered
4. Frame is divided into 4 regions (lanes)
5. Vehicles are counted per lane
6. Lane with maximum vehicles → assigned **GREEN signal**

---

## 🛠️ Tech Stack

* Python
* Ultralytics YOLOv8
* OpenCV
* NumPy

---

## 📂 Project Structure

```
traffic-management-main/
├── yolo_detection.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/your-username/traffic-management-system.git
cd traffic-management-system
```

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ How to Run

```
python yolo_detection.py
```

---

## 📸 Output

* Bounding boxes around vehicles
* Total vehicle count
* Lane-wise counts
* Traffic density level
* Active green signal lane

---

## ⚠️ Limitations

* Lane detection is based on simple screen division (not real road lanes)
* Performance depends on video quality
* No tracking (same vehicle may be counted multiple times across frames)

---

## 🚀 Future Improvements

* Lane detection using computer vision
* Vehicle tracking (DeepSORT)
* Real-time camera integration
* Traffic signal timing optimization
* GUI dashboard

---

## 🎤 Viva Explanation (Short)

> “This system uses YOLOv8 for vehicle detection, divides the road into regions, counts vehicles in each lane, and dynamically assigns the green signal to the most congested lane.”

---

## 👩‍💻 Author

* Lisha

---
