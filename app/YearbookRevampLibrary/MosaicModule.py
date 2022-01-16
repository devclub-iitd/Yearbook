#/usr/bin/env python
import os, random, argparse
from PIL import Image
import numpy as np


def CreateMosaic(target_image,input_images,grid_size, output_filename=None, output_path=None, is_folder_input=False ,reuse_images=True):

    """
    :param target_image: the image whose mosaic is to be generated (Path of the image has to be entered in this parameter).
    :param input_images: the list/folder of the images that we want to use to generate the mosaic.
    :param grid_size: tuple containing the number of images we want along the height and breadth of mosaic respectively.
    :param output_filename: string containing the filename of the generated mosaic
    :param output_path: string containing the required path where the generated mosaic is to be saved (optional argument)
    :param is_folder_input: a boolean specify whether the input images are passed to the function as a folder or list (True means a folder is passed, default value is set to False)
    :param reuse_images: a boolean to specify whether we want input images to be reused to create the mosaic(optional argument , by default set to True )
    :return: generated mosaic image as a numpy array
    """
    def getImages(images_directory):
        files = os.listdir(images_directory)
        images = []
        for file in files:
            filePath = os.path.abspath(os.path.join(images_directory, file))
            try:
                fp = open(filePath, "rb")
                im = Image.open(fp)
                images.append(im)
                im.load()
                fp.close()
            except:
                print("Invalid image: %s" % (filePath,))
        return (images)

    
    def getAverageRGB(image):
        im = np.array(image)
        w, h, d = im.shape
        return (tuple(np.average(im.reshape(w * h, d), axis=0)))


    def splitImage(image, size):
        W, H = image.size[0], image.size[1]
        m, n = size
        w, h = int(W / n), int(H / m)
        imgs = []
        for j in range(m):
            for i in range(n):
                imgs.append(image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)))
        return (imgs)


    def getBestMatchIndex(input_avg, avgs):
        avg = input_avg
        index = 0
        min_index = 0
        min_dist = float("inf")
        for val in avgs:
            dist = ((val[0] - avg[0]) * (val[0] - avg[0]) + (val[1] - avg[1]) * (val[1] - avg[1]) + (val[2] - avg[2]) * (val[2] - avg[2]))
            if dist < min_dist:
                min_dist = dist
                min_index = index
            index += 1
        return (min_index)


    def createImageGrid(images, dims):
        m, n = dims
        width = max([img.size[0] for img in images])
        height = max([img.size[1] for img in images])
        grid_img = Image.new('RGB', (n * width, m * height))
        for index in range(len(images)):
            row = int(index / n)
            col = index - n * row
            grid_img.paste(images[index], (col * width, row * height))
        return (grid_img)


    def createPhotomosaic(target_image, input_images, grid_size, reuse_images=True):
        target_images = splitImage(target_image, grid_size)

        output_images = []
        count = 0
        batch_size = int(len(target_images) / 10)
        avgs = []
        for img in input_images:
            try:
                avgs.append(getAverageRGB(img))
            except ValueError:
                continue

        for img in target_images:
            avg = getAverageRGB(img)
            match_index = getBestMatchIndex(avg, avgs)
            output_images.append(input_images[match_index])
            if count > 0 and batch_size > 10 and count % batch_size == 0:
                print('processed %d of %d...' % (count, len(target_images)))
            count += 1
            # remove selected image from input if flag set
            if not reuse_images:
                input_images.remove(match_index)

        mosaic_image = createImageGrid(output_images, grid_size)
        return (mosaic_image)


    ### ---------------------------------------------

    
    target_image = Image.open(target_image)
    
    # input images
    
    if(is_folder_input==True):
        input_images = getImages(input_images)
    else :
        input_images = input_images 
    # check if any valid input images found
    if input_images == []:
        # print('No input images found in %s. Exiting.' % (args.images,))
        exit()

    # shuffle list - to get a more varied output?
    random.shuffle(input_images)


   

    # resize the input to fit original image size?
    resize_input = True

    print('starting photomosaic creation...')

    # if images can't be reused, ensure m*n <= num_of_images
    if not reuse_images:
        if grid_size[0] * grid_size[1] > len(input_images):
            print('grid size less than number of images')
            exit()

    # resizing input
    if resize_input:
        print('resizing images...')
        # for given grid size, compute max dims w,h of tiles
        dims = (int(target_image.size[0] / grid_size[1]),
                int(target_image.size[1] / grid_size[0]))
        print("max tile dims: %s" % (dims,))
        # resize
        for img in input_images:
            img.thumbnail(dims)

    # create photomosaic
    mosaic_image = createPhotomosaic(target_image, input_images, grid_size, reuse_images)
    
    # write out mosaic
    if(output_path!=None): 
        mosaic_image.save(f'{output_path}/{output_filename}.jpeg', 'jpeg')
    
    return mosaic_image

