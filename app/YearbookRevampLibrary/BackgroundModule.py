import os
import cv2 as cv
import mediapipe as mp
import numpy as np
from YearbookRevampLibrary.utils import output_image_files, collect_image_files



class SelfiSegmentation():

    def __init__(self, model=1):
        """
        :param model: model type 0 or 1. 0 is general 1 is landscape(faster)
        """
        self.model = model
        self.mpDraw = mp.solutions.drawing_utils
        self.mpSelfieSegmentation = mp.solutions.selfie_segmentation
        self.selfieSegmentation = self.mpSelfieSegmentation.SelfieSegmentation(self.model)

    def removeBG(self, img, imgBg=(255, 255, 255), threshold=0.1):
        """
        :param img: image to remove background from
        :param imgBg: BackGround Image
        :param threshold: higher = more cut, lower = less cut
        :return: background removed image
        """
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = self.selfieSegmentation.process(imgRGB)
        condition = np.stack(
            (results.segmentation_mask,) * 3, axis=-1) > threshold
        if isinstance(imgBg, tuple):
            _imgBg = np.zeros(img.shape, dtype=np.uint8)
            _imgBg[:] = imgBg
            imgOut = np.where(condition, img, _imgBg)
        else:
            imgOut = np.where(condition, img, imgBg)
        return imgOut


def remove_background(cv2_list = None, input_path = None, output_path = None, background_img=(255, 255, 255), model=0, threshold=0.1):
    """
    :param cv2_list: list of cv2 objects 
    :param input_path: path of the folder containing images
    :param output_path: path of the folder to save background removed images
    :param background_img: image to set for the background
    :param model: model type 0 or 1. 0 is general 1 is landscape(faster)
    :param threshold: higher = more cut, lower = less cut
    :return: list of cv2 objects with background removed
    """

    images, filenames = collect_image_files(cv2_list, input_path)
    refined_images = []
    # makeFolder(output_file)

    segmentor = SelfiSegmentation(model)

    for idx, file in enumerate(images):

        img = images[idx]
        imgOut = segmentor.removeBG(img, background_img, threshold)

        refined_images.append(imgOut)

    output = output_image_files(refined_images, output_path, filenames)
    return output
    