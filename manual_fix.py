import cv2 as cv
import numpy as np
from os import path, walk


def onMouse(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv.EVENT_LBUTTONDOWN:
       mouse_x, mouse_y = x, y


def display_image(image):
    cv.namedWindow("Window", cv.WINDOW_NORMAL);
    cv.imshow("Window", image);
    cv.setMouseCallback("Window", onMouse)
    return cv.waitKey(0)


if __name__ == '__main__':
    # Caminho completo das imagens
    dir_path = path.join(path.curdir, 'threshold_images', 'MotoC', 'Eucalyptus')

    for root, dirs, files in walk(dir_path):
        for file in files:
            # Nome da imagem
            image_name = file
            filename, extension = image_name.split('.')  # Separando imagem e extensão

            # Leitura da imagem
            image = cv.imread(path.join(dir_path, image_name), cv.IMREAD_UNCHANGED)

            finish_painting = False
            while not finish_painting:
                image_copy = np.copy(image)
                print('-' * 18)
                print('Pintando fundo')
                print('[Esc] Pular')
                print('[outro] Executar')
                print('-' * 18)
                key = display_image(image_copy)

                if key == 27:
                    break
                
                print()
                print('Pressione uma tecla para confirmar cada ponto')
                print('Primeiro ponto:')
                display_image(image_copy)
                x1, y1 = mouse_x, mouse_y

                print()
                print('Segundo ponto:')
                display_image(image_copy)
                x2, y2 = mouse_x, mouse_y
                
                print()
                print('[Espaço] PRETO')
                print('[outro] BRANCO')
                key = display_image(image_copy)
                color = 0 if key == 32 else 255

                # Ajustes na imagem [linha1:linha2, coluna1:coluna2] = 0
                # Cria um pequeno retângulo e aplica uma cor 0 -> preto ou 255 -> branco
                if y2 <= y1 and x1 <= x2:
                    image_copy[y2:y1, x1:x2] = color
                else:
                    print('o primeiro ponto precisa estar abaixo e à esquerda do segundo')
                
                print()
                print('[Espaço] Manter alterações')
                print('[outro] Reverter')
                key = display_image(image_copy)
                
                if key == 32:
                    image = np.copy(image_copy)


            finish_square_painting = False
            while not finish_square_painting:
                image_copy = np.copy(image)
                print('-' * 18)
                print('Pintando quadrado')
                print('[Esc] Pular')
                print('[outro] Executar')
                print('-' * 18)
                key = display_image(image_copy)

                if key == 27:
                    break
                
                print()
                print('Pressione uma tecla para confirmar cada ponto')
                print('Primeiro ponto:')
                display_image(image)
                x1, y1 = mouse_x, mouse_y

                print()
                print('Segundo ponto:')
                display_image(image)
                x2, y2 = mouse_x, mouse_y

                # Ajustes para mudar a cor do quadrado
                color = 127

                if y2 <= y1 and x1 <= x2:
                    for line in range(y2, y1):
                        for column in range(x1, x2):
                            if image_copy[line, column] == 255:
                                image_copy[line, column] = color
                else:
                    print('o primeiro ponto precisa estar abaixo e à esquerda do segundo')
                
                print()
                print('[Espaço] Manter alterações')
                print('[outro] Reverter')
                key = display_image(image_copy)
                
                if key == 32:
                    image = np.copy(image_copy)

            # Exportando a imagem
            cv.imwrite(path.join(path.curdir, dir_path, image_name), image)
