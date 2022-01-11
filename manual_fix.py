import cv2 as cv
import numpy as np
from os import path, walk
from enum import Enum
from typing import Tuple, Union


class Keyboard(Enum):
    ESC = 27
    SPACEBAR = 32
    NUM_1 = 49
    NUM_2 = 50
    NUM_3 = 51
    NUM_4 = 52
    NUM_6 = 54
    NUM_7 = 55
    NUM_8 = 56
    NUM_9 = 57


class Colors(Enum):
    BLACK = 0
    WHITE = 255
    GRAY = 127


def onMouse(event, x, y, flags, param) -> None:
    global mouse_x, mouse_y
    if event == cv.EVENT_LBUTTONDOWN:
        mouse_x, mouse_y = x, y


def display_image(image) -> int:
    cv.namedWindow('Window', cv.WINDOW_NORMAL)
    cv.imshow('Window', image)
    cv.setMouseCallback('Window', onMouse)

    return cv.waitKey(0)


def print_options(options: dict, title: str = None) -> None:
    print('-' * 18)
    if title:
        print(title)
    
    for key, value in options.items():
        print(f'[{key}] {value}')
    print('-' * 18)


def get_rectangle_boundaries(image) -> Tuple[int, int, int, int]:
    print()
    print('Pressione uma tecla para confirmar cada ponto')
    print('Primeiro ponto:')
    display_image(image)
    x1, y1 = mouse_x, mouse_y

    print()
    print('Segundo ponto:')
    display_image(image)
    x2, y2 = mouse_x, mouse_y

    superior_row = min(y1, y2)
    inferior_row = max(y1, y2)
    left_column = min(x1, x2)
    right_column = max(x1, x2)

    return superior_row, inferior_row, left_column, right_column


def get_boundaries(image, key: Union[Keyboard, int]) -> Tuple[int, int, int, int]:
    # Valores padrão
    superior_row: int = 0
    inferior_row: int = image.shape[0]
    left_column: int = 0
    right_column: int = image.shape[1]

    # Cantos
    if key in [
        Keyboard.NUM_1.value,
        Keyboard.NUM_3.value,
        Keyboard.NUM_7.value,
        Keyboard.NUM_9.value
    ]:
        print()
        print('Pressione uma tecla para confirmar o ponto da diagonal')
        print('Ponto:')
        display_image(image)

        # Linhas
        if key in [Keyboard.NUM_1.value, Keyboard.NUM_3.value]:  # Inferior
            superior_row = mouse_y
        else:                                                    # Superior
            inferior_row = mouse_y

        # Colunas
        if key in [Keyboard.NUM_1.value, Keyboard.NUM_7.value]:  # Esquerda
            right_column = mouse_x
        else:                                                    # Direita
            left_column = mouse_x

    # Lados
    elif key in [
        Keyboard.NUM_2.value,
        Keyboard.NUM_4.value,
        Keyboard.NUM_6.value,
        Keyboard.NUM_8.value
    ]:
        print()
        print('Pressione uma tecla para confirmar um ponto do lado oposto do retângulo')
        print('Ponto:')
        display_image(image)

        if key == Keyboard.NUM_2.value:
            superior_row = mouse_y

        elif key == Keyboard.NUM_4.value:
            right_column = mouse_x

        elif key == Keyboard.NUM_6.value:
            left_column = mouse_x

        elif key == Keyboard.NUM_8.value:
            inferior_row = mouse_y

    # Retângulo
    else:
        superior_row, inferior_row, left_column, right_column = get_rectangle_boundaries(image)

    return superior_row, inferior_row, left_column, right_column


def region_painting(image):
    while True:
        image_copy = np.copy(image)

        print_options({
            'Esc': 'Pular',
            '1': 'Canto Inferior Esquerdo',
            '2': 'Lado Inferior',
            '3': 'Canto Inferior Direito',
            '4': 'Lado Esquerdo',
            '6': 'Lado Direito',
            '7': 'Canto Superior Esquerdo',
            '8': 'Lado Superior',
            '9': 'Canto Superior Direito',
            'Outro': 'Retângulo'
        }, 'Pintando região')

        key: int = display_image(image_copy)

        if key == Keyboard.ESC.value:
            break

        superior_row, inferior_row, left_column, right_column = get_boundaries(image_copy, key)

        print()
        print_options({
            'Espaço': 'PRETO',
            'Outro': 'BRANCO',
        })

        key = display_image(image_copy)
        color = Colors.BLACK.value if key == Keyboard.SPACEBAR.value else Colors.WHITE.value

        # Ajustes na imagem [linha1:linha2, coluna1:coluna2] = 0
        # Cria um pequeno retângulo e aplica uma cor 0 -> preto ou 255 -> branco
        image_copy[superior_row:inferior_row, left_column:right_column] = color

        print()
        print_options({
            'Espaço': 'Manter alterações',
            'Outro': 'Reverter'
        })

        key = display_image(image_copy)
        if key == Keyboard.SPACEBAR.value:
            image = np.copy(image_copy)

    return image


def square_painting(image):
    while True:
        image_copy = np.copy(image)

        print_options({
            'Esc': 'Pular/Salvar',
            'Outro': 'Executar'
        }, 'Pintando quadrado')
    
        key = display_image(image_copy)

        if key == Keyboard.ESC.value:
            break

        superior_row, inferior_row, left_column, right_column = get_rectangle_boundaries(image_copy)

        # Ajustes para mudar a cor do quadrado
        for line in range(superior_row, inferior_row):
            for column in range(left_column, right_column):
                if image_copy[line, column] == 255:
                    image_copy[line, column] = Colors.GRAY.value

        print()
        print_options({
            'Espaço': 'Manter alterações',
            'Outro': 'Reverter'
        })
        
        key = display_image(image_copy)

        if key == Keyboard.SPACEBAR.value:
            image = np.copy(image_copy)

    return image


if __name__ == '__main__':
    # Caminho completo das imagens
    input_path = input('Digite o caminho da pasta com as imagens (Exemplo: pasta/subpasta1/subpasta2): ')
    input_path = input_path.split('/')

    dir_path = path.join(path.curdir, *input_path)

    for root, dirs, files in walk(dir_path):
        print('*' * 45)
        print()
        print(f'Pasta atual: {root}')
        print()

        if len(files) == 0:
            print('Nenhum arquivo encontrado')
        else:
            files.sort()

        for progress_count, file in enumerate(files, start=1):
            image_name = file  # Nome da imagem
            filename, extension = image_name.split('.')  # Separando imagem e extensão

            print('*' * 45)
            print()
            print(f'Imagem: {filename}')
            print(f'Progresso na pasta: {progress_count}/{len(files)} imagens')
            print()
            print('*' * 45)

            # Leitura da imagem
            image = cv.imread(path.join(dir_path, image_name), cv.IMREAD_UNCHANGED)

            # Pintando regiões da imagem
            image = region_painting(image)

            # Pintando o quadrado
            image = square_painting(image)

            # Exportando a imagem
            cv.imwrite(path.join(path.curdir, dir_path, image_name), image)
