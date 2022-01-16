import os
import cv2 as cv

#Function to make a new folder of given filename in working directory
def makeFolder(filename):
    cwd = os.getcwd()
    path = cwd + "\\" + filename
    if not os.path.exists(path):
        os.mkdir(path)

#Function to collect image files 
def collect_image_files(cv2_list, input_path):
    IMAGE_FILES = []
    filenames = []
    if input_path == None:
        IMAGE_FILES = cv2_list.copy()
        filenames = [["image-"+ str(i), '.png'] for i in range(1,len(IMAGE_FILES)+1)]
    else:
        for file in os.listdir(input_path):
            image = cv.imread(input_path + "\\" + file)
            filename, file_ext = os.path.splitext(file)
            filenames.append([filename, file_ext])
            IMAGE_FILES.append(image)
  
    return IMAGE_FILES, filenames

def output_image_files(cv2_list, output_path, filenames):
    if output_path != None:
        for i in range(len(cv2_list)):
            
            filename, file_ext = filenames[i]
            try:
                cv.imwrite(output_path + '\\' + filename + file_ext, cv2_list[i])
            except :
                cv.imwrite(output_path + '\\' + filename + ".png", cv2_list[i])
            # cv.imwrite(output_path + '\\' + "image-{}".format(i) + ".png", cv2_list[i])
    return cv2_list


    
        