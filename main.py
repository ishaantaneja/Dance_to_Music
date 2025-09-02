import cv2
import mediapipe as mp
import pygame.midi

# Initialize MIDI
pygame.midi.init()
player = pygame.midi.Output(0)  # Use default MIDI output
instrument = 0  # Acoustic Grand Piano
player.set_instrument(instrument)

# Mediapipe pose setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        # Draw skeleton on frame
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get landmarks
        landmarks = results.pose_landmarks.landmark

        # Left hand (landmark 15), Right hand (landmark 16), Nose (landmark 0)
        left_hand = landmarks[15]
        right_hand = landmarks[16]
        nose = landmarks[0]

        # Simple trigger: if hand is above nose → play note
        if left_hand.y < nose.y:
            player.note_on(60, 100)  # Middle C
        else:
            player.note_off(60, 100)

        if right_hand.y < nose.y:
            player.note_on(64, 100)  # E
        else:
            player.note_off(64, 100)

    cv2.imshow("BodyBeats", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
player.close()
pygame.midi.quit()
