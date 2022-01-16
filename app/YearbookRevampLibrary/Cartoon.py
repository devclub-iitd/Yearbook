import cv2
import os
import numpy as np
from YearbookRevampLibrary.utils import output_image_files, collect_image_files


def edge_mask(img, line_size, blur_value):
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      gray_blur = cv2.medianBlur(gray, blur_value)
      edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
      return edges

def Countours(image):
    contoured_image = image
    gray = cv2.cvtColor(contoured_image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 200, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]
    cv2.drawContours(contoured_image, contours, contourIdx=-1, color=6, thickness=1)
    return contoured_image

def ColourQuantization(image, K=9):
    Z = image.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    compactness, label, center = cv2.kmeans(Z, K, None, criteria, 1, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((image.shape))
    return res2

def BlurredCartoonFilter(cv2_list = None, input_path = None, output_path = None):
    """
        :param cv2_list: list of cv2 objects 
        :param input_path: image folder path

        :param output_path: output folder path
        :return: list of cv2 objects 


        """
    images, filenames = collect_image_files(cv2_list, input_path)    
    
    final_output = []

    for img in images:
        line_size = 7
        blur_value = 7
        edges = edge_mask(img, line_size, blur_value)
        total_color = 8
        k = total_color
        data = np.float32(img).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        blurred = cv2.bilateralFilter(result, d=10, sigmaColor=250, sigmaSpace=250)
        cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
        final_output.append(cartoon)

    output = output_image_files(final_output, output_path, filenames)
    return output

def CartoonFilter(cv2_list = None, input_path = None, output_path = None):
    """
        :param cv2_list: list of cv2 objects 
        :param input_path: image folder path

        :param output_path: output folder path
        :return: list of cv2 objects 


        """
    images, filenames = collect_image_files(cv2_list, input_path)    
    
    final_output = []
    for image in images:
        coloured = ColourQuantization(image)
        contoured = Countours(coloured)
        final_image = contoured

        final_output.append(final_image)

    output = output_image_files(final_output, output_path, filenames)
    return output

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(BASE_DIR)

    input_path = os.path.join(BASE_DIR + "\\Input")
    output_path = os.path.join(BASE_DIR + "\\Output")
    CartoonFilter(cv2_list=None,input_path=input_path, output_path = output_path)


