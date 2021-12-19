import cv2

#Ask user for video file path
video_fp = input("Video file path: ")

#Create OpenCV video capture object
vidcap = cv2.VideoCapture(video_fp)

#Read first frame from video
success, image = vidcap.read()

#increment variable
i=0

#write frames to /frame directory
while success and not image is None:
    #Write image
    s2 = cv2.imwrite(f"frames/frame{i}.jpg", image)
    #go to next frame
    succes, image = vidcap.read()
    #increment i
    i+=1