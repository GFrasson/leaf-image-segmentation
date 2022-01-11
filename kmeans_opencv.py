from os import listdir, path
import cv2 as cv
import numpy as np
from K_Means_Opencv import K_Means_Opencv


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
            cv.polylines(image, [pts], True, color, 10, cv.LINE_AA)

    return image


if __name__ == '__main__':
    # Instanciando o método utilizado
    kmeans_opencv = K_Means_Opencv(k_clusters=2)

    # Encontrando arquivos da pasta do caminho escolhido
    image_dir_path = path.join(path.curdir, 'images')
    thresh_dir_path = path.join(path.curdir, 'threshold_images')
    contoured_image_dir_path = path.join(path.curdir, 'contoured_images')
    subdir_path = path.join('MotoC', 'Coffee')

    dir_path = path.join(image_dir_path, subdir_path)
    files = [filename for filename in listdir(dir_path) if path.isfile(path.join(dir_path, filename))]

    # Percorrendo os arquivos
    progress = 0
    for file in files:
        full_path = path.join(dir_path, file)
        filename, extension = file.split('.')

        # Leitura da imagem
        image = cv.imread(full_path)

        # Aplicação do método de segmentação
        threshold_image = kmeans_opencv.image_segmentation(image)

        # Exportando imagem preto e branco
        cv.imwrite(path.join(thresh_dir_path, subdir_path, filename + '_mask' + '.png'), threshold_image)

        # Convertendo a imagem para inteiro 8-bit
        threshold_image = np.uint8(threshold_image)

        # gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # Encontrando contornos
        contours = cv.findContours(threshold_image, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        # Desenhando contornos na imagem original
        contoured_image = draw_countours(image, contours)

        # Exportando imagem contornada
        cv.imwrite(path.join(contoured_image_dir_path, subdir_path, filename + '_contour' + '.png'), contoured_image)

        progress += 1
        print(f'Progresso: {progress}/{len(files)} imagens')
