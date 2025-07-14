def scan_label():
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Camera not available. Returning mock image data.")
            return "image_data"
        print("Press SPACE to capture label image...")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            cv2.imshow('Scan Label - Press SPACE to capture', frame)
            key = cv2.waitKey(1)
            if key % 256 == 32:  # SPACE pressed
                img_name = "scanned_label.jpg"
                cv2.imwrite(img_name, frame)
                print(f"Image saved as {img_name}")
                break
        cap.release()
        cv2.destroyAllWindows()
        return "scanned_label.jpg"
    except ImportError:
        print("OpenCV not installed. Returning mock image data.")
        return "image_data"
