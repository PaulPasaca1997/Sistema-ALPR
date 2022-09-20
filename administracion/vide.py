import cv2 
cap = cv2.VideoCapture('http://192.168.100.3:8080/')
ret, frame = cap.read()
cap.release()
