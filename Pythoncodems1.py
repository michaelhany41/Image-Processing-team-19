#!/usr/bin/env python3
import cv2
import time
from datetime import datetime

DEVICE_INDEX = 0                # usually /dev/video0
WIDTH, HEIGHT = 3280, 2464      # full 8MP (if supported by your /dev/video0)
WARMUP_SECONDS = 1.0            # let exposure settle

def main():
    cap = cv2.VideoCapture(DEVICE_INDEX, cv2.CAP_V4L2)
    if not cap.isOpened():
        raise RuntimeError("Could not open camera. Try changing DEVICE_INDEX or check /dev/video0 permissions.")

    # Ask for full resolution (camera/driver may clamp to supported values)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    # Warm up: grab a few frames so auto exposure/white balance stabilizes
    start = time.time()
    while time.time() - start < WARMUP_SECONDS:
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        raise RuntimeError("Failed to capture frame from camera.")

    filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    ok = cv2.imwrite(filename, frame)
    if not ok:
        raise RuntimeError("Failed to write image to disk.")

    print(f"Saved: {filename}")
    print(f"Captured resolution: {frame.shape[1]}x{frame.shape[0]}")

if __name__ == "__main__":
    main()
