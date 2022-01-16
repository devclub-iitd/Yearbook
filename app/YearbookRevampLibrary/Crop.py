import cv2
import os
import numpy as np
import mediapipe as mp
import re
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
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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

def incircle(point, radius,makeCircle):
    if not makeCircle:
        return True
    if (point[0] - radius) ** 2 + (point[1] - radius) ** 2 <= radius ** 2:
        return True
    else:
        return False


def CropFace(img_file_src, size, output_path=None, makeCircle = True,img_file = None):
    """

        :param img_file_src: image file path
        :param size: diameter of final image
        :param output_path: output folder location(if nothing specified, return image as array)
        :param makeCircle: Crop as circle or square, By default True
        :param img_file: Pass an image file as cv2 object, if you dont want to pass image file path, By default none
        :return: list of cv2 objects 


        """
    # print(img_file)
    if img_file.any() == None:
        img_initial = cv2.imread(img_file_src)
    else:
        img_initial = img_file
    final_img = []
    grayImg = cv2.cvtColor(img_initial, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = face_cascade.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        faces = []
        rows, cols, c = img_initial.shape
        ColCenter = int(cols / 2)
        RowCenter = int(rows / 2)
        radius = min(ColCenter, RowCenter)
        faces.append( [ColCenter, RowCenter, radius,radius])

    # print(faces)

    for face in faces:

        face_img_raw = img_initial[face[1]:face[1] + face[2], face[0]:face[0] + face[2]]

        face_img = cv2.cvtColor(face_img_raw, cv2.COLOR_BGR2BGRA)

        radius = int(face[2] / 2)

        for rows in range(face_img.shape[0]):
            for cols in range(face_img.shape[1]):
                if not incircle([rows, cols], radius,makeCircle):
                    face_img[rows][cols][3] = 0

        face_img_final = cv2.resize(face_img, (size, size))

        final_img.append(face_img_final)
    # else:
    #     blankimg = np.zeros((size, size), dtype=np.uint8)
    #     final_img.append(cv2.cvtColor(blankimg, cv2.COLOR_GRAY2BGR))

    if output_path == None:
        return final_img
    else:
        file = re.split(r"[./\\]", img_file_src)[-2:-1]

        i = 0
        for img in final_img:
            try:
                cv2.imwrite(output_path + "\\" + file[0] + str(i)+ "." + file[1], img)
            except:
                cv2.imwrite(output_path + "\\" + file[0] + str(i) + ".png", img)
            i+=1


def CropBody(img_file_src, size, output_path=None ,makeCircle = True,removeBackground = True,img_file = None):
    """

        :param img_file_src: image file path
        :param size: diameter of final image
        :param output_path: output folder location(if nothing specified, return image as array)
        :param makeCircle: Crop as circle or square, By default True
        :param removeBackground: Removing the background via mediapipe, By default True
        :param img_file: Pass an image file as cv2 object, if you dont want to pass image file path, By default none
        :return: cv2 object


        """
    if img_file.any() == None:
        img = cv2.imread(img_file_src)
    else:
        img = img_file
    rows, cols, c = img.shape
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)
        image.flags.writeable = True
        # print(results.pose_landmarks)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Find location of nose, to center circle around it
            Nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
            if Nose:
                RowCenter = int(Nose.y * rows)
                ColCenter = int(Nose.x * cols)
            else:
                RowCenter = int(rows / 2)
                ColCenter = int(cols / 2)

            # Calculates maximum possible radius size
            if cols < rows:
                radius = int(cols / 2)
                ColCenter = radius
                if RowCenter < radius:
                    RowCenter = radius
                elif rows - RowCenter < radius:
                    RowCenter = rows - radius
            else:
                radius = int(rows / 2)
                RowCenter = radius
                if ColCenter < radius:
                    ColCenter = radius
                elif cols - ColCenter < radius:
                    ColCenter = cols - radius

            segment = SelfiSegmentation(0)
            if removeBackground:
                ImageOut = segment.removeBG(img, (255, 255, 255))
            else:
                ImageOut = img


            # Crops image
            face_img_raw = ImageOut[RowCenter - radius:RowCenter + radius, ColCenter - radius:ColCenter + radius]

            # Convert to include an alpha value
            face_img = cv2.cvtColor(face_img_raw, cv2.COLOR_BGR2BGRA)

            for rows in range(face_img.shape[0]):
                for cols in range(face_img.shape[1]):
                    if not incircle([rows, cols], radius, makeCircle):
                        face_img[rows][cols][3] = 0

            face_img_final = cv2.resize(face_img, (size, size))
        else:

            ColCenter = int(cols / 2)
            RowCenter = int(rows / 2)
            radius = min(ColCenter,RowCenter)
            if removeBackground:
                segment = SelfiSegmentation(0)
                img = segment.removeBG(img, (255, 255, 255))


            face_img_raw = img[RowCenter - radius:RowCenter + radius, ColCenter - radius:ColCenter + radius]

            face_img_raw = cv2.cvtColor(face_img_raw, cv2.COLOR_BGR2BGRA)
            for rows in range(face_img_raw.shape[0]):
                for cols in range(face_img_raw.shape[1]):
                    if not incircle([rows, cols], radius, makeCircle):
                        face_img_raw[rows][cols][3] = 0

            face_img_final = cv2.resize(face_img_raw, (size, size))
        if output_path == None:
            return face_img_final
        else:
            file = re.split(r"[./\\]", img_file_src)[-2:-1]


            try:
                cv2.imwrite(output_path + "\\" + file[0] + "." + file[1], face_img_final)
            except:
                cv2.imwrite(output_path + "\\" + file[0] + ".png", face_img_final)


def CropAll(cv2_list = None, input_path = None, output_path = None, type=0, makeCircle = True,removeBackground = True):
    """
        :param cv2_list: list of cv2 objects
        :param input_path: image folder path
        :param output_path: output folder path
        :param type: type of crop, 0 to crop body, 1 to get face crop , default is 0
        :param makeCircle: Crop as circle or square, By default True
        :return: list of cv2 objects 
    

        """
    images, filenames = collect_image_files(cv2_list, input_path)    
    final_filenames = []
    final_output = []
    
    
    for img_initial,filename in zip(images,filenames):
        rows, cols, c = img_initial.shape
        size = int(min(rows, cols))

        if type == 0:
            Image_Out = CropBody(None, size, None ,makeCircle,removeBackground,img_initial)
            final_output.append(Image_Out)
        else:
            Images_Out = CropFace(None, size, None ,makeCircle,img_initial)
            for iindex,img_out in enumerate(Images_Out):
                final_output.append(img_out)
                final_filenames.append([filename[0]+ str(iindex),filename[1]])
    if type == 0:
        output = output_image_files(final_output, output_path, filenames)
    else:
        output = output_image_files(final_output, output_path, final_filenames)
    return output


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(BASE_DIR)

    input_path = os.path.join(BASE_DIR + "\\Input")
    output_path = os.path.join(BASE_DIR + "\\Output")
    CropAll(None,input_path,output_path,0,True,False)


