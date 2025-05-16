# I hate how abstracted this is...
# but i learn a lot about venvs.
# Must use python 3.10.x for this to interpret
# command to activate this venv:
# source handtrack-env/bin/activate
# that venv has pip (to install other packages), numpy, pygame, and mediapipe

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # stack overflow says this hides the prompt when importing pygame
import pygame   # used for window and drawing on screen
import pygame.camera
import mediapipe as mp  # used for hand tracking
import numpy as np  # used for quick maths
import time # for timing inputs

# Initialize Pygame and camera
pygame.init()
pygame.camera.init()

# Set up camera
camlist = pygame.camera.list_cameras()
if not camlist:
    raise Exception("No camera found :(")
cam = pygame.camera.Camera(camlist[0], (640, 480))
cam.start()

# Mediapipe hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 1,
    min_detection_confidence = 0.90,
    min_tracking_confidence = 0.8
)   # tweak these with trial and error based on camera and how it operates
mp_drawing = mp.solutions.drawing_utils

# Pygame display setup
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Hand Tracking Program")

clock = pygame.time.Clock()
running = True

# Distance thresholds - these are gonna be trial and error for sure
# folks online say this is a common way to handle input bouncing
LEFT_CLICK_TRIGGER = 35
LEFT_CLICK_RELEASE = 50
RIGHT_CLICK_TRIGGER = 35
RIGHT_CLICK_RELEASE = 50

# Track click states
left_down = False
right_down = False

while running:
    clock.tick(60)  # Limit to 60 FPS

    # Cleanly exit when user closes window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get image from camera
    frame = cam.get_image()
    frame_rgb = pygame.surfarray.array3d(frame)
    # Flip image (I had to trial and error this to get the orientation correct, it rotates 90 and flips it vertically)
    frame_rgb = np.rot90(frame_rgb)
    frame_rgb = np.flipud(frame_rgb)
    frame_rgb = np.ascontiguousarray(frame_rgb)

    # Mediapipe expects RGB image in: height, width, channels
    results = hands.process(frame_rgb)

    screen.blit(frame, (0, 0))  # Show camera image in window

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]

        # Get finger coordinates
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

        # Convert to screen coordinates
        ix, iy = int(index_tip.x * 640), int(index_tip.y * 480)
        mx, my = int(middle_tip.x * 640), int(middle_tip.y * 480)
        tx, ty = int(thumb_tip.x * 640), int(thumb_tip.y * 480)

        # Draw hollow green circle on index finger
        pygame.draw.circle(screen, (0, 255, 0), (ix, iy), 12, width=3)

        # Draw hollow blue on middle finger
        pygame.draw.circle(screen, (0, 0, 255), (mx, my), 10, width=2)

        # Draw hollow red on thumb
        pygame.draw.circle(screen, (255, 0, 0), (tx, ty), 10, width=2)

        # Calculate distances for clicking (index to thumb is left click, middle to thumb is right)
        dist_index_thumb = np.hypot(ix - tx, iy - ty)
        dist_middle_thumb = np.hypot(mx - tx, my - ty)

        # Handle left click (index + thumb ONLY)
        if dist_index_thumb < LEFT_CLICK_TRIGGER and dist_middle_thumb > RIGHT_CLICK_RELEASE:   # Ensures middle finger is out of the way
            if not left_down:
                left_down = True
                print("LEFT MOUSE DOWN")
        elif dist_index_thumb > LEFT_CLICK_RELEASE:
            if left_down:
                left_down = False
                print("LEFT MOUSE UP")

        # Handle right click (middle + thumb ONLY)
        if dist_middle_thumb < RIGHT_CLICK_TRIGGER and dist_index_thumb > LEFT_CLICK_RELEASE:   # ensures index finger is out of the way
            if not right_down:
                right_down = True
                print("RIGHT MOUSE DOWN")
        elif dist_middle_thumb > RIGHT_CLICK_RELEASE:
            if right_down:
                right_down = False
                print("RIGHT MOUSE UP")

    # Draw line when clicking for good visualization
    if left_down:
        wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
        wx, wy = int(wrist.x * 640), int(wrist.y * 480)
        pygame.draw.line(screen, (255, 255, 0), (wx, wy), (ix, iy), 4)
    if right_down:
        wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
        wx, wy = int(wrist.x * 640), int(wrist.y * 480)
        pygame.draw.line(screen, (0, 255, 255), (wx, wy), (mx, my), 4)
    
    pygame.display.update()

# Clean things up
hands.close()
cam.stop()
pygame.quit()

# Thanks to mediapipe docs, stack overflow, reddit, etc because without that this would've taken days :)