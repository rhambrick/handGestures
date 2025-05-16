# Hand Gesture Mouse Control with MediaPipe & Pygame

This project is a lightweight prototype simulating gesture based mouse control using only a webcam and computer vision. It tracks hand landmarks with MediaPipe and provides visual feedback via a Pygame window.

- Real time (60 FPS) hand tracking using webcam
- Simulated cursor controlled by fingertips
- Gesture detection:
  - **Left click**: Touch thumb to index finger
  - **Right click**: Touch thumb to middle finger
  Click and drag supported
- Live feedback with outlined fingertip marker and click line indicator
- Design aimed for minimal hardware

![demo.gif](demo.gif)

### Notes:
- Project was built as a resume piece to explore gesture recognition and user interaction design
- Focused on responsiveness, usability, and visual clarity
- Easily expandable to support real cursor control via a simple library like pyautogui
- Input clarity is important, and I am exploring techniques on stabilizing input for clean controls.
- MediaPipe offers CNN parameter adjustments, so the program can be adjusted to different levels of confidence.

### Summary:
> Built a hand-tracking virtual mouse in Python using MediaPipe; implemented real-time gesture detection with left/right click logic and visual interaction feedback.
