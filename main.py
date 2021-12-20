import cv2
import pytesseract
import os

#set tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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
        image_s1_speed = image[640:680, 65:155]

        #Crop image to extract stage 1 altitude
        image_s1_alt = image[640:680, 180:260]

        #Write image
        cv2.imwrite(f"{dir}/frame{i}.jpg", image)

        #Write cropped images
        cv2.imwrite(f"{dir}/s1/speed/frame{i}.jpg", image_s1_speed)
        cv2.imwrite(f"{dir}/s1/alt/frame{i}.jpg", image_s1_alt)

        #go to next frame
        success, image = vidcap.read()
        #increment i
        i+=1

#Usere optical character recognition to extract speed and altitude data from given directory and outputs it to a text file
def extract_data(data_dir, out_file):
    data = []
    #loop through images in stage 1 speed folder
    for im_path in os.listdir(f"{data_dir}"):
        #read image from full path
        im = cv2.imread(os.path.join(data_dir, im_path))

        #convert image to greyscale for OCR
        im_g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        #create threshold image to simplify things.
        im_t = cv2.threshold(im_g, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)[1]
        im_r = cv2.resize(im_t, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        #define kernel size
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20,20))

        #Apply dilation to threshold image
        im_d = cv2.dilate(im_r, rect_kernel, iterations = 1)

        #Find countours
        contours = cv2.findContours(im_d, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]

        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            
            #Draw rectangle around contour
            rect = cv2.rectangle(im, (x,y), (x+w, y+h), (0, 255, 0), 2)

            #crop
            im_c = im[y:y+h, x:x+w]

            data.append(pytesseract.image_to_string(im_c, config = "--psm 7 outputbase digits"))
    return data