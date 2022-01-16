import os
import cv2 as cv
import mediapipe as mp
from YearbookRevampLibrary.utils import output_image_files, collect_image_files


class AutoAligner():

    def __init__(self):

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.mp_holistic = mp.solutions.holistic
        self.mp_face_detection = mp.solutions.face_detection

    def align_image(self, img, min_face_detection_confidence=0.5, min_pose_detection_confidence=0.5):
        """
        :param img: image to align
        :param min_face_detection_confidence: confidence for face detection in the image
        :param min_pose_detection_confidence: confidence for pose detection in the image
        :return: aligned image
        """
        with self.mp_pose.Pose(static_image_mode=True, model_complexity=2,
                               min_detection_confidence=min_pose_detection_confidence) as pose:
            image = img
            image_height, image_width, _ = image.shape

            results = pose.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

            if not results.pose_landmarks:
                i = 0
                while (True):
                    mp_face_detection = self.mp_face_detection

                    with mp_face_detection.FaceDetection(model_selection=1,
                                                         min_detection_confidence=min_face_detection_confidence) as face_detection:

                        if i == 4:
                            return image
                        results2 = face_detection.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
                        if not results2.detections:
                            i += 1
                            image = cv.rotate(image, rotateCode=0)
                            continue

                        return image

            n = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.NOSE].y
            r = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_SHOULDER].y
            l = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_SHOULDER].y

            if n < r and n < l:
                pass
            elif n > r and n > l:
                image = cv.rotate(image, rotateCode=1)
            elif n < r and n > l:
                image = cv.rotate(image, rotateCode=0)
            else:
                image = cv.rotate(image, rotateCode=2)

            return image


def auto_align(cv2_list = None, input_path = None, output_path = None, min_face_detection_confidence=0.5, min_pose_detection_confidence=0.5):
    """
    :param cv2_list: list of cv2 objects to be aligned
    :param input_path: path of the folder containing images
    :param output_path: path of the folder to save aligned images 
    :param min_face_detection_confidence: confidence for face detection in the image
    :param min_pose_detection_confidence: confidence for pose detection in the image
    :return: list of aligned cv2 objects 
    """
    images, filenames = collect_image_files(cv2_list, input_path)
    # makeFolder(output_file)

    path = output_path
    refined_images = []

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    mp_holistic = mp.solutions.holistic

    with mp_pose.Pose(static_image_mode=True, model_complexity=2,
                      min_detection_confidence=min_pose_detection_confidence) as pose:

        for idx, file in enumerate(images):

            image = images[idx]
            image_height, image_width, _ = image.shape

            results = pose.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

            if not results.pose_landmarks:
                i = 0
                while (True):

                    mp_face_detection = mp.solutions.face_detection
                    with mp_face_detection.FaceDetection(model_selection=1,
                                                         min_detection_confidence=min_face_detection_confidence) as face_detection:

                        if i == 4:
                            refined_images.append(image)
                            break

                        results2 = face_detection.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

                        if not results2.detections:
                            i += 1
                            image = cv.rotate(image, rotateCode=0)
                            continue

                        refined_images.append(image)
                        break

                continue

            n = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y
            r = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y
            l = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y

            if n < r and n < l:
                pass
            elif n > r and n > l:
                image = cv.rotate(image, rotateCode=1)
            elif n < r and n > l:
                image = cv.rotate(image, rotateCode=0)
            else:
                image = cv.rotate(image, rotateCode=2)

            refined_images.append(image)
        
        output = output_image_files(refined_images, output_path, filenames)
        return output
            
