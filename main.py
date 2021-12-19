import cv2
from os.path import exists

#Asks user for video filepath and checks if file exists
def get_video_fp():
    #Ask user for video file path
    video_fp = input("Video file path: ")

    #Check file exists, ask user again if it doesn't
    if not exists(video_fp):
        print("Filepath invalid.")
        get_video_fp()
    else:
        return video_fp

        
#Create OpenCV video capture object
vidcap = cv2.VideoCapture(get_video_fp())

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