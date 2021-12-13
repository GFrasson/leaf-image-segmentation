import cv2 as cv
import numpy as np
from os import path


def draw_countours(image, contornos, color: tuple = (0, 0, 255)):
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
            cv.polylines(image, [pts], True, color, 10, cv.LINE_AA)

    return image


if __name__ == '__main__':
    # Caminhos das imagens
    image_dir_path = path.join(path.curdir, 'images')
    thresh_dir_path = path.join(path.curdir, 'threshold_images')
    contoured_image_dir_path = path.join(path.curdir, 'contoured_images')
    subdir_path = path.join('MotoC', 'Coffee')

    # Nome da imagem
    image_name = 'Coffee_1_pat_1cm_dist_30cm_MotoC'

    # Leitura da imagem
    thresh = cv.imread(path.join(thresh_dir_path, subdir_path, image_name + '_mask.png'), cv.IMREAD_UNCHANGED)
    image = cv.imread(path.join(image_dir_path, subdir_path, image_name + '.jpg'), cv.IMREAD_UNCHANGED)

    # Encontrando contornos
    contours = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # Desenhando contornos na imagem original
    contoured_image = draw_countours(image, contours)

    # Preview
    # cv.namedWindow("Window", cv.WINDOW_NORMAL);
    # cv.imshow("Window", image);
    # cv.waitKey(0)

    # Salvando imagem contornada
    cv.imwrite(path.join(contoured_image_dir_path, subdir_path, image_name + '_contour' + '.png'), contoured_image)
