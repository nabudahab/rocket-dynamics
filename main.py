import cv2
import pytesseract
import os

#Asks user for video filepath and checks if file exists
def get_video_fp():
    #Ask user for video file path
    video_fp = input("Video file path: ")

    #Check file exists, ask user again if it doesn't
    if not os.path.exists(video_fp):
        print("Filepath invalid.")
        get_video_fp()
    else:
        return video_fp

#Separates the video at the given filepath into frames, exports each as a .jpg to the given directory
def write_images(dir, vid_fp):
    #Create OpenCV video capture object
    vidcap = cv2.VideoCapture(vid_fp)

    #Read first frame from video
    success, image = vidcap.read()

    #increment variable
    i=0

    #write frames to /frame directory
    while success and not image is None:
        #Crop image to extract stage 1 speed
        image_s1_speed = image[645:670, 75:145]

        #Crop image to extract stage 1 altitude
        image_s1_alt = image[645:670, 190:245]

        #Write image
        cv2.imwrite(f"{dir}/frame{i}.jpg", image)

        #Write cropped images
        cv2.imwrite(f"{dir}/s1/speed/frame{i}.jpg", image_s1_speed)
        cv2.imwrite(f"{dir}/s1/alt/frame{i}.jpg", image_s1_alt)

        #go to next frame
        success, image = vidcap.read()
        #increment i
        i+=1