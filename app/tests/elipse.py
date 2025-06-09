import cv2
import numpy as np

height, width = 400, 400
frame = np.zeros((height, width, 3), dtype=np.uint8)

center_x, center_y = int(width / 2), int(height / 2)
a, b = 140, 180
color = (144, 238, 144)

cv2.ellipse(frame, (center_x, center_y), (a, b), 0, 0, 360, color, 10)

cv2.imshow("Elipse Verde Claro", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()