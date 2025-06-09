import cv2
import numpy as np

height, width = 480, 360
frame = np.zeros((height, width, 3), dtype=np.uint8) 

side = 200
center_x, center_y = int(width / 2), int(height / 3)
top_left = (center_x - side // 2, center_y - side // 2)
bottom_right = (center_x + side // 2, center_y + side // 1)
color = (144, 238, 144)

cv2.rectangle(frame, top_left, bottom_right, color, 5)

cv2.imshow("Quadrado Verde Claro", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()