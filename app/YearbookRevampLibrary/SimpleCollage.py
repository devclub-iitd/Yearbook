import numpy as np
import random
import os
import cv2
import operator
from YearbookRevampLibrary.Crop import CropBody
from YearbookRevampLibrary.utils import output_image_files, collect_image_files



def SimpleCollage(cv2_list = None, input_path = None, output_path = None,size = [2000,2000],makeCircle = True,array = np.ones((8,8)),removeBackground = False,filename = "Collage"):
    """
        :param cv2_list: list of cv2 objects 
        :param input_path: image folder path
        :param output_path: output folder path
        :param size: Specify the final image size as (rows,columns) tuple
        :param array: Pass a numpy array with 1s at the position you want the image and 0s at the place to leave blank
        :param makeCircle: Crop as circle or square
        :param removeBackground: Specify removing background or not, by default false
        :param filename: Filename of the final collage, by default "Collage"
        :return: cv2 object
        """
    # images_files = os.listdir(input_path)
    images, filenames = collect_image_files(cv2_list, input_path)    
    
    final_output = []

    arrayShape = array.shape

    rowsize = size[0]/arrayShape[0]
    colsize = size[1]/arrayShape[1]

    radius = int(min(rowsize,colsize)/2)

    final_img = np.zeros((size[0],size[1],4),dtype=np.uint8)



    i = 0
    max = len(images)
    for row in range(arrayShape[0]):
        for col in range (arrayShape[1]):
            if i >= max:
                break
            if array[row,col] == 1:

                img_out = CropBody(None,size= 2*radius,output_path=None,makeCircle=makeCircle,removeBackground=removeBackground,img_file= images[i])
                x_locn = int((row+0.5)*rowsize)
                y_locn = int((col + 0.5) * colsize)
                final_img[x_locn-radius:x_locn+radius,y_locn-radius:y_locn+radius,] = img_out
                i+=1

    output = output_image_files([final_img], output_path, [[filename,"png"]])
    return output


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(BASE_DIR)

    input_path = os.path.join(BASE_DIR + "\\Input")
    output_path = os.path.join(BASE_DIR + "\\Output")


    SimpleCollage(None,input_path,output_path,(2000,3000),True)


