import numpy as np
import random
import os
import cv2
import operator
from YearbookRevampLibrary.Crop import CropBody
from YearbookRevampLibrary.utils import output_image_files, collect_image_files


def dist(a, b, c, d):
    return np.sqrt((a - b) ** 2 + (c - d) ** 2)


def withinedge(x, y, radius,WIDTH,HEIGHT):
    if x + radius < WIDTH and x > radius and y + radius < HEIGHT and y > radius:
        return True
    return False


def getTAngle(a, b, c):
    return np.arccos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))


def growSingle(cx, cy, cr, carray, growRate):
    angle = np.arctan((cy - carray[1]) / (cx - carray[0]))
    r = growRate
    return [-r * np.cos(angle), r * np.sin(angle), r]


def growDouble(cx, cy, cr, carray1, carray2, growRate):
    # angle = np.arctan((cy - carray1[1] )/(cx-carray1[0]))-np.arctan((carray2[1] - carray1[1] )/(carray2 [0]-carray1[0]))

    alpha = np.arctan((carray2[1] - carray1[1]) / (carray2[0] - carray1[0]))
    angle1 = getTAngle(cr + carray1[2], carray2[2] + carray1[2], cr + carray2[2])
    x1 = (cr + carray1[2]) * np.cos(np.sign(alpha) * angle1)
    y1 = (cr + carray1[2]) * np.sin(np.sign(alpha) * angle1)
    cr += growRate
    angle2 = getTAngle(cr + carray1[2], carray2[2] + carray1[2], cr + carray2[2])
    x2 = (cr + carray1[2]) * np.cos(np.sign(alpha) * angle2)
    y2 = (cr + carray1[2]) * np.sin(np.sign(alpha) * angle2)

    growx = (x2 - x1) * np.cos(alpha) - (y2 - y1) * np.sin(alpha)
    growy = (x2 - x1) * np.sin(alpha) + (y2 - y1) * np.cos(alpha)

    return [growx, growy, growRate]


class Circle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 1
        self.growing = True

    def grow(self,CircleList,TotalFalse,WIDTH,HEIGHT):
        if self.growing:
            growRate = 1
            if not withinedge(self.x, self.y, self.r,WIDTH,HEIGHT):
                TotalFalse += 1
                self.growing = False
            else:
                CircleCollisions = []
                for circle in CircleList:
                    if circle.x != self.x and circle.y != self.y:
                        if dist(circle.x, self.x, circle.y, self.y) < circle.r + self.r:
                            CircleCollisions.append([circle.x, circle.y, circle.r])
                            # self.growing = False
                            # TotalFalse += 1
                if len(CircleCollisions) == 0:
                    self.r += growRate
                elif len(CircleCollisions) == 1:
                    # output = growSingle(self.x,self.y,self.r,CircleCollisions[0],growRate)
                    # self.x+=output[0]
                    # self.y += output[1]
                    # self.r += output[2]
                    self.growing = False
                    TotalFalse += 1

                elif len(CircleCollisions) == 2:
                    # output = growDouble(self.x,self.y,self.r,CircleCollisions[0],CircleCollisions[1],growRate)
                    # self.x += output[0]
                    # self.y += output[1]
                    # self.r += output[2]
                    self.growing = False
                    TotalFalse += 1

                elif len(CircleCollisions) >= 3:
                    self.growing = False
                    TotalFalse += 1
        return TotalFalse

def MakeCircleCollage(TemplateFile,cv2_list = None, input_path = None, output_path = None,filename = "Collage.png"):
    """
        :param TemplateFile: Image file, used to make collage(Image file in black and white, white spots are places where circles will be made)
        :param cv2_list: list of cv2
        :param input_path: image folder path
        :param output_path: output folder path
        :param filename: Filename of the final collage, by default "Collage.png"
        """
    TotalFalse = 0
    CircleList = []
    TotalCircles = 2*len(os.listdir(input_path))


    TemplateImg = cv2.imread(TemplateFile)
    HEIGHT, WIDTH, C = TemplateImg.shape



    i = 0
    while i < TotalCircles - 1:
        y = random.randint(20, WIDTH - 20)
        x = random.randint(20, HEIGHT - 20)

        if TemplateImg[x][y][0] == 0:
            continue

        for circle in CircleList:
            if (circle.x - x) ** 2 + (circle.y - y) ** 2 < circle.r ** 2:
                break
        else:
            CircleList.append(Circle(x, y))
            i += 1

    while TotalFalse < len(CircleList):
        for circle in CircleList:
            if random.random() < 2:
                TotalFalse = circle.grow(CircleList,TotalFalse,WIDTH,HEIGHT)



    CircleList.sort(key=operator.attrgetter('r'),reverse=True)



    BlankImg_raw = np.zeros((WIDTH, HEIGHT), dtype=np.uint8)
    BlankImg = cv2.cvtColor(BlankImg_raw, cv2.COLOR_GRAY2BGRA)


    i = 0
    images, filenames = collect_image_files(cv2_list, input_path)    
    
    final_output = []

    for img_initial in images:
        img_out = CropBody(None,size= 2 * CircleList[i].r,output_path=None,makeCircle=True,removeBackground=False,img_file= img_initial)
        img_out = cv2.cvtColor(img_out,cv2.COLOR_BGR2BGRA)
        img_out = cv2.rotate(img_out, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        for row in range(2 * CircleList[i].r):
            for col in range(2 * CircleList[i].r):
                if img_out[col][row][3] != 0:
                    BlankImg[int(CircleList[i].y - CircleList[i].r + col) % WIDTH][int(CircleList[i].x - CircleList[i].r + row) % HEIGHT] = img_out[col][row]

        i+=1

    BlankImg = cv2.rotate(BlankImg, cv2.cv2.ROTATE_90_CLOCKWISE)


    BlankImg = cv2.flip(BlankImg, 1)
    
    output = output_image_files([BlankImg], output_path, [[filename,"png"]])
    return output



if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(BASE_DIR)

    input_path = os.path.join(BASE_DIR + "\\Input")
    output_path = os.path.join(BASE_DIR + "\\Output")
    TemplateFile = os.path.join(BASE_DIR + "\\Bitmap.png")

    MakeCircleCollage(TemplateFile,None,input_path,output_path)


