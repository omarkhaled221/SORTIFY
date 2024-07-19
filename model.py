from ultralytics import YOLO
import cv2

# Initialize the model
model = YOLO("C:/Users/Omar khaled/Desktop/best.pt")

# Map class indices to item types
item_types = {
    0: "cans",
    1: "plastic",
    2: "glass",
    3: "cardboard"
}

# Initialize webcam
cap = cv2.VideoCapture(0)  # Change the argument to switch between different cameras if necessary

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Perform prediction
    results = model.predict(source=frame, imgsz=416, conf=0.8, verbose=False)

    # Check predictions and print detections
    detected = False
    for result in results:
        if result.boxes:
            for box in result.boxes:
                class_id = int(box.cls)
                item_type = item_types.get(class_id, "other")
                print(f"Detection: {item_type}")
                detected = True

    if not detected:
        print("Detection: other")

    # Display the frame with detections
    cv2.imshow('Frame', frame)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close any open windows
cap.release()
cv2.destroyAllWindows()