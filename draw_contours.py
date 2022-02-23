import cv2 as cv
import numpy as np
from os import path, walk


def draw_countours(image, contornos, color: tuple = (0, 0, 255)):
    if len(contornos[0]) == 0:
        return image
    
    for contorno in contornos:
        for point in contorno:
            pts = []

            for point2 in point:
                try:
                    x = int(point2[0])
                    y = int(point2[1])
                except:
                    x = int(point2[0][0])
                    y = int(point2[0][1])

                    pts.append([x, y])

            pts = np.array(pts)
            cv.polylines(image, [pts], True, color, 2, cv.LINE_AA)

    return image


if __name__ == '__main__':
    # Caminhos das imagens
    image_dir_path = path.join(path.curdir, 'images')
    thresh_dir_path = path.join(path.curdir, 'threshold_images')
    contoured_image_dir_path = path.join(path.curdir, 'contoured_images')
    subdir_path = path.join('MotoC', 'Orange')

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
            contoured_image = draw_countours(image, contours)

            # Salvando imagem contornada
            cv.imwrite(path.join(contoured_image_dir_path, subdir_path, image_name + '_contour' + '.png'), contoured_image)
