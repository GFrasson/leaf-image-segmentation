from os import listdir, path
import cv2 as cv
# import numpy as np
from K_Means_Opencv import K_Means_Opencv


if __name__ == '__main__':
    kmeans_opencv = K_Means_Opencv(k_clusters=2)

    subdir_path = path.join('teste')
    dir_path = path.join(path.curdir, 'images', subdir_path)
    files = [filename for filename in listdir(dir_path) if path.isfile(path.join(dir_path, filename))]

    progress = 0
    for file in files:
        full_path = path.join(dir_path, file)
        filename, extension = file.split('.')

        image = cv.imread(full_path)
        segmented_image, threshold_image = kmeans_opencv.image_segmentation(image)

        cv.imwrite(path.join(path.curdir, 'segmented_images', subdir_path, filename + '_mask' + f'.{extension}'), segmented_image)
        cv.imwrite(path.join(path.curdir, 'threshold_images', subdir_path, filename + '_mask' + '_threshold' + f'.{extension}'), threshold_image)

        progress += 1
        print(f'Progresso: {progress}/{len(files)} imagens')
