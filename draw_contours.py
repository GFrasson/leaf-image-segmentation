import cv2 as cv
import numpy as np
from os import path, walk
from draw_contours_polylines import draw_contours_polylines


if __name__ == '__main__':
    # Caminhos das imagens
    image_dir_path = path.join(path.curdir, 'images')
    thresh_dir_path = path.join(path.curdir, 'threshold_images')
    contoured_image_dir_path = path.join(path.curdir, 'contoured_images')
    subdir_path = path.join('OneVision', 'Eucalyptus')

    for root, dirs, files in walk(path.join(image_dir_path, subdir_path)):
        for file in files:
            # Nome da imagem
            image_name = file.split('.')[0]
            print(image_name)

            # Leitura da imagem
            thresh = cv.imread(path.join(thresh_dir_path, subdir_path, image_name + '_mask.png'), cv.IMREAD_UNCHANGED)
            image = cv.imread(path.join(image_dir_path, subdir_path, image_name + '.jpg'))

            # Encontrando contornos
            contours = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

            # Desenhando contornos na imagem original
            contoured_image = draw_contours_polylines(image, contours)

            # Salvando imagem contornada
            cv.imwrite(path.join(contoured_image_dir_path, subdir_path, image_name + '_contour' + '.png'), contoured_image)
