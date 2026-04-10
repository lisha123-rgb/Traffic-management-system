from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("yolov8n.pt")

# Load video
cap = cv2.VideoCapture("traffic.mp4")

# Check video
if not cap.isOpened():
    print("Error: Cannot open video")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Video ended")
        break

    # Resize (optional for performance)
    frame = cv2.resize(frame, (640, 480))

    # Detection
    results = model(frame)
    annotated = results[0].plot()

    # ----------------------------
    # Total Vehicle Count
    # ----------------------------
    count = len(results[0].boxes)

    # ----------------------------
    # Lane-wise Counting
    # ----------------------------
    h, w, _ = frame.shape

    left_lane = 0
    right_lane = 0
    top_lane = 0
    bottom_lane = 0

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Center point
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # Assign to lanes
        if cx < w//2 and cy > h//2:
            left_lane += 1
        elif cx > w//2 and cy > h//2:
            right_lane += 1
        elif cy < h//2 and cx < w//2:
            top_lane += 1
        else:
            bottom_lane += 1

    # ----------------------------
    # Traffic Signal Logic
    # ----------------------------
    lanes = {
        "LEFT": left_lane,
        "RIGHT": right_lane,
        "TOP": top_lane,
        "BOTTOM": bottom_lane
    }

    green_lane = max(lanes, key=lanes.get)

    # ----------------------------
    # Traffic Density
    # ----------------------------
    if count < 15:
        density = "LOW"
    elif count < 30:
        density = "MEDIUM"
    else:
        density = "HIGH"

    # ----------------------------
    # Display Info
    # ----------------------------
    cv2.putText(annotated, f"Vehicles: {count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(annotated, f"Traffic: {density}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.putText(annotated, f"GREEN: {green_lane}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

    # Lane counts
    cv2.putText(annotated, f"L: {left_lane}", (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    cv2.putText(annotated, f"R: {right_lane}", (20, 190),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    cv2.putText(annotated, f"T: {top_lane}", (20, 220),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    cv2.putText(annotated, f"B: {bottom_lane}", (20, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    # ----------------------------
    # Draw Lane Lines (visual)
    # ----------------------------
    cv2.line(annotated, (w//2, 0), (w//2, h), (255,255,255), 2)
    cv2.line(annotated, (0, h//2), (w, h//2), (255,255,255), 2)

    # Show output
    cv2.imshow("Traffic Management System", annotated)

    # Exit on ESC
    if cv2.waitKey(1) == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()