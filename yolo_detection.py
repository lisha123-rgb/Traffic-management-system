from ultralytics import YOLO
import cv2
import time

# Load YOLO model
model = YOLO("yolov8n.pt")

# Vehicle class IDs (COCO)
vehicle_classes = [2, 3, 5, 7]  # car, bike, bus, truck

# Load video
cap = cv2.VideoCapture("traffic.mp4")

if not cap.isOpened():
    print("Error: Cannot open video")
    exit()

# ----------------------------
# SIGNAL TIMER SETUP
# ----------------------------
signal_timer = 5  # seconds
last_switch_time = time.time()
current_green = "LEFT"

# ----------------------------
# LINE CROSSING SETUP
# ----------------------------
line_y = 250
crossed_ids = set()
vehicle_count_line = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Video ended")
        break

    frame = cv2.resize(frame, (640, 480))

    # Detection
    results = model(frame)
    annotated = frame.copy()

    boxes = results[0].boxes

    count = 0

    # Lane counters
    h, w, _ = frame.shape
    left_lane = right_lane = top_lane = bottom_lane = 0

    for i, box in enumerate(boxes):
        cls = int(box.cls[0])

        # ----------------------------
        # VEHICLE FILTERING
        # ----------------------------
        if cls not in vehicle_classes:
            continue

        count += 1

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # Draw box
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0,255,0), 2)

        # Label
        label = model.names[cls]
        cv2.putText(annotated, label, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        # ----------------------------
        # LINE CROSSING LOGIC
        # ----------------------------
        if cy > line_y and i not in crossed_ids:
            crossed_ids.add(i)
            vehicle_count_line += 1

        # ----------------------------
        # LANE ASSIGNMENT
        # ----------------------------
        if cx < w//2 and cy > h//2:
            left_lane += 1
        elif cx > w//2 and cy > h//2:
            right_lane += 1
        elif cy < h//2 and cx < w//2:
            top_lane += 1
        else:
            bottom_lane += 1

    # ----------------------------
    # SIGNAL LOGIC WITH TIMER
    # ----------------------------
    lanes = {
        "LEFT": left_lane,
        "RIGHT": right_lane,
        "TOP": top_lane,
        "BOTTOM": bottom_lane
    }

    if time.time() - last_switch_time > signal_timer:
        current_green = max(lanes, key=lanes.get)
        last_switch_time = time.time()

    # ----------------------------
    # TRAFFIC DENSITY
    # ----------------------------
    if count < 15:
        density = "LOW"
    elif count < 30:
        density = "MEDIUM"
    else:
        density = "HIGH"

    # ----------------------------
    # DRAW LINE
    # ----------------------------
    cv2.line(annotated, (0, line_y), (w, line_y), (0,0,255), 2)

    # ----------------------------
    # DISPLAY TEXT
    # ----------------------------
    cv2.putText(annotated, f"Vehicles: {count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(annotated, f"Density: {density}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.putText(annotated, f"GREEN: {current_green}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

    cv2.putText(annotated, f"Line Count: {vehicle_count_line}", (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

    # Lane counts
    cv2.putText(annotated, f"L: {left_lane}", (20, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
    cv2.putText(annotated, f"R: {right_lane}", (20, 230),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
    cv2.putText(annotated, f"T: {top_lane}", (20, 260),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
    cv2.putText(annotated, f"B: {bottom_lane}", (20, 290),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    # Lane lines
    cv2.line(annotated, (w//2, 0), (w//2, h), (255,255,255), 2)
    cv2.line(annotated, (0, h//2), (w, h//2), (255,255,255), 2)

    cv2.imshow("Traffic Management System", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()