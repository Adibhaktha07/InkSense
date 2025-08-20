import cv2
import numpy as np
import mediapipe as mp

class FingerDrawer:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.canvas = None
        self.prev_x, self.prev_y = 0, 0
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.colors = [
            (255, 0, 255),    # Purple
            (0, 255, 0),      # Green
            (255, 255, 0),    # Cyan
            (0, 255, 255),    # Yellow
            (255, 0, 0),      # Blue
            (255, 255, 255)   # White
        ]
        self.color_index = 0
        self.brush_color = self.colors[self.color_index]

        self.eraser_mode = False
        self.last_finger_count = -1
        self.gesture_buffer = []
        self.buffer_length = 3

    def clear_canvas(self):
        if self.canvas is not None:
            self.canvas[:] = 0

    def count_fingers(self, lm_list):
        fingers = []
        # Thumb
        fingers.append(lm_list[4][0] > lm_list[3][0])
        # Index to pinky
        for tip_id in [8, 12, 16, 20]:
            fingers.append(lm_list[tip_id][1] < lm_list[tip_id - 2][1])
        return fingers.count(True)

    def generate(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            if self.canvas is None:
                self.canvas = np.zeros_like(frame)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)

            if result.multi_hand_landmarks:
                hand_landmarks = result.multi_hand_landmarks[0]
                lm_list = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]
                finger_count = self.count_fingers(lm_list)

                # Smooth gesture using buffer
                self.gesture_buffer.append(finger_count)
                if len(self.gesture_buffer) > self.buffer_length:
                    self.gesture_buffer.pop(0)

                stable_count = max(set(self.gesture_buffer), key=self.gesture_buffer.count)

                # Gesture actions
                if stable_count == 5:
                    self.eraser_mode = True
                elif stable_count == 1:
                    self.eraser_mode = False
                elif stable_count == 4 and self.last_finger_count != 4:
                    self.color_index = (self.color_index + 1) % len(self.colors)
                    self.brush_color = self.colors[self.color_index]

                self.last_finger_count = stable_count

                # Drawing with index finger only when 1 finger is up or 5 (eraser)
                if stable_count in [1, 5]:
                    x1, y1 = lm_list[8]  # Index finger tip

                    if self.prev_x == 0:
                        self.prev_x, self.prev_y = x1, y1

                    color = (0, 0, 0) if self.eraser_mode else self.brush_color
                    thickness = 30 if self.eraser_mode else 5

                    cv2.line(self.canvas, (self.prev_x, self.prev_y), (x1, y1), color, thickness, lineType=cv2.LINE_AA)
                    self.prev_x, self.prev_y = x1, y1
                else:
                    self.prev_x, self.prev_y = 0, 0

                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            blended = cv2.addWeighted(frame, 0.5, self.canvas, 0.5, 0)
            ret, buffer = cv2.imencode('.jpg', blended)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def save_canvas(self, filename):
        if self.canvas is not None:
            cv2.imwrite(filename, self.canvas)
