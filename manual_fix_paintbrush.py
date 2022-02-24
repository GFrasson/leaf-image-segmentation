from genericpath import isdir
import cv2 as cv
import numpy as np
from os import path, walk
from enum import Enum
from typing import Tuple, Union

CONTOURED_IMAGE_WINDOW_NAME: str = 'Contours'
SEGMENTATION_IMAGE_WINDOW_NAME: str = 'Segmentation'


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


class Paint_Event_Handler():
    def __init__(self, original_image, added_image, color):
        self.original_image = original_image
        self.original_added_image = added_image
        self.color = color
        self.painting = False

        cv.namedWindow(SEGMENTATION_IMAGE_WINDOW_NAME, cv.WINDOW_NORMAL)
        cv.setMouseCallback(SEGMENTATION_IMAGE_WINDOW_NAME, self.paint_on_mouse_move)

    def paint_on_mouse_move(self, event, x, y, flags, parameters):
        if event == cv.EVENT_LBUTTONDBLCLK:
            self.painting = not self.painting
            
        if self.painting:
            self.original_image[y, x] = self.color
            self.original_added_image[y, x] = self.color
            cv.imshow(SEGMENTATION_IMAGE_WINDOW_NAME, self.original_added_image)

    def show_image(self):
        return self.original_added_image


def on_mouse(event, x, y, flags, param) -> None:
    global mouse_x, mouse_y
    if event == cv.EVENT_LBUTTONDOWN:
        mouse_x, mouse_y = x, y


def display_image(image, window_name: str = SEGMENTATION_IMAGE_WINDOW_NAME, mouse_interaction: bool = True, wait_key: bool = True) -> int | None:
    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    cv.imshow(window_name, image)

    if mouse_interaction:
        cv.setMouseCallback(window_name, on_mouse)

    if wait_key:
        return cv.waitKey(0)


def get_contoured_image(original_image, threshold_image, thickness=1):
    original_image_copy = original_image.copy()

    # Encontrando contornos
    contours, _ = cv.findContours(threshold_image, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # Desenhando contornos na imagem original
    contoured_image = cv.drawContours(original_image_copy, contours, -1, (0, 0, 255), thickness)

    return contoured_image


def update_contoured_image_window(original_image, threshold_image, contour_thickness) -> None:
    contoured_image = get_contoured_image(original_image, threshold_image, contour_thickness)

    if cv.getWindowProperty(CONTOURED_IMAGE_WINDOW_NAME, cv.WND_PROP_VISIBLE) >= 1:
        cv.imshow(CONTOURED_IMAGE_WINDOW_NAME, contoured_image)


def build_original_image_name(threshold_filename: str) -> str:
    image_filename_list = threshold_filename.split('_')
    new_image_filename_list = list()

    for partial_name in image_filename_list:
        if partial_name == 'mask':
            break

        new_image_filename_list.append(partial_name)

    image_filename = '_'.join(new_image_filename_list)
    image_name = image_filename + '.jpg'

    return image_name


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


def region_painting(original_image, threshold_image, contour_thickness):
    while True:
        image_copy = np.copy(threshold_image)

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

        update_contoured_image_window(original_image, image_copy, contour_thickness)

        print()
        print_options({
            'Espaço': 'Manter alterações',
            'Outro': 'Reverter'
        })

        key = display_image(image_copy)
        if key == Keyboard.SPACEBAR.value:
            threshold_image = np.copy(image_copy)
        else:
            update_contoured_image_window(original_image, threshold_image, contour_thickness)

    return threshold_image


def square_painting(original_image, threshold_image, contour_thickness):    
    while True:
        image_copy = np.copy(threshold_image)

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

        update_contoured_image_window(original_image, image_copy, contour_thickness)

        print()
        print_options({
            'Espaço': 'Manter alterações',
            'Outro': 'Reverter'
        })
        
        key = display_image(image_copy)

        if key == Keyboard.SPACEBAR.value:
            threshold_image = np.copy(image_copy)
        else:
            update_contoured_image_window(original_image, threshold_image, contour_thickness)

    return threshold_image


def free_painting(original_image, threshold_image, gray_image, contour_thickness):
    while True:
        threshold_image_copy = np.copy(threshold_image)

        added_image = cv.addWeighted(threshold_image_copy, 0.3, gray_image, 1, 0)

        print_options({
            'Esc': 'Pular/Salvar',
            'Outro': 'Executar'
        }, 'Pintando pixels')
    
        key = display_image(added_image)

        if key == Keyboard.ESC.value:
            break

        print()
        print_options({
            'Espaço': 'PRETO',
            'Outro': 'BRANCO',
        })

        key = cv.waitKey(0)
        color = Colors.BLACK.value if key == Keyboard.SPACEBAR.value else Colors.WHITE.value

        print('Clique duas vezes para ativar ou desativar o pincel')
        print_options({
            'Espaço': 'Finalizar pintura',
        }, 'Pintando pixels')

        cv.namedWindow(SEGMENTATION_IMAGE_WINDOW_NAME, cv.WINDOW_NORMAL)
        paint_event_handler = Paint_Event_Handler(threshold_image_copy, added_image, color)

        while True:
            cv.imshow(SEGMENTATION_IMAGE_WINDOW_NAME, paint_event_handler.show_image())
            key = cv.waitKey(1)

            if key == Keyboard.SPACEBAR.value:
                break

        update_contoured_image_window(original_image, threshold_image_copy, contour_thickness)
        
        print()
        print_options({
            'Espaço': 'Manter alterações',
            'Outro': 'Reverter'
        })
        
        key = display_image(added_image)

        if key == Keyboard.SPACEBAR.value:
            threshold_image = np.copy(threshold_image_copy)
        else:
            update_contoured_image_window(original_image, threshold_image, contour_thickness)

    return threshold_image


if __name__ == '__main__':
    # Caminho completo das imagens
    print('Exemplo de caminho de pasta: pasta/subpasta1/subpasta2')

    image_input_path = input('Digite o caminho da pasta com as imagens originais: ').split('/')
    image_dir_path = path.join(path.curdir, *image_input_path)
    
    threshold_image_input_path = input('Digite o caminho da pasta com as imagens limiarizadas: ').split('/')
    threshold_image_dir_path = path.join(path.curdir, *threshold_image_input_path)

    if not isdir(image_dir_path) or not isdir(threshold_image_dir_path):
        raise FileNotFoundError('Pasta nao foi encontrada')

    contour_thickness = input('Digite a espessura dos contornos que serão desenhados na imagem (padrao: 1) (max: 10): ')
    
    try:
        contour_thickness = int(contour_thickness)
        contour_thickness = min(contour_thickness, 10)
    except ValueError:
        contour_thickness = 1

    try:
        for root, dirs, files in walk(threshold_image_dir_path):
            print('*' * 45)
            print()
            print(f'Pasta atual: {root}')
            print()

            if len(files) == 0:
                print('Nenhum arquivo encontrado')
            else:
                files.sort()

            for progress_count, file in enumerate(files, start=1):
                threshold_image_name = file  # Nome da imagem
                filename, extension = threshold_image_name.split('.')  # Separando imagem e extensão

                image_name = build_original_image_name(filename)

                print('*' * 45)
                print()
                print(f'Imagem: {filename}')
                print(f'Progresso na pasta: {progress_count}/{len(files)} imagens')
                print()
                print('*' * 45)

                # Leitura da imagem
                threshold_image = cv.imread(path.join(threshold_image_dir_path, threshold_image_name), cv.IMREAD_UNCHANGED)

                try:
                    image = cv.imread(path.join(image_dir_path, image_name))

                    # Convertendo imagem original para escala de cinza
                    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
                    
                    contoured_image = get_contoured_image(image, threshold_image)
                    display_image(contoured_image, CONTOURED_IMAGE_WINDOW_NAME, False, False)

                    # Pintando regiões da imagem
                    threshold_image = region_painting(image, threshold_image, contour_thickness)

                    # Pintando o quadrado
                    threshold_image = square_painting(image, threshold_image, contour_thickness)

                    # Pintando pixels
                    threshold_image = free_painting(image, threshold_image, gray_image, contour_thickness)
                    
                    # Exportando a imagem
                    cv.imwrite(path.join(path.curdir, threshold_image_dir_path, threshold_image_name), threshold_image)

                except Exception as error:
                    print("Não foi possível ler a imagem original")

    except ValueError as error:
        print(error)
    except Exception as error:
        print(error)
    finally:
        cv.destroyAllWindows()
