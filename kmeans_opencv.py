from os import listdir, path
import cv2 as cv
from K_Means_Opencv import K_Means_Opencv


if __name__ == '__main__':
    # Instanciando o método utilizado
    kmeans_opencv = K_Means_Opencv(k_clusters=2)

    # Encontrando arquivos da pasta do caminho escolhido
    subdir_path = path.join('teste')
    dir_path = path.join(path.curdir, 'images', subdir_path)
    files = [filename for filename in listdir(dir_path) if path.isfile(path.join(dir_path, filename))]

    # Percorrendo os arquivos
    progress = 0
    for file in files:
        full_path = path.join(dir_path, file)
        filename, extension = file.split('.')

        # Leitura da imagem
        image = cv.imread(full_path)

        # Aplicação do método de segmentação
        segmented_image, threshold_image = kmeans_opencv.image_segmentation(image)

        # Exportando as imagens geradas
        cv.imwrite(path.join(path.curdir, 'segmented_images', subdir_path, filename + '_mask' + f'.{extension}'), segmented_image)
        cv.imwrite(path.join(path.curdir, 'threshold_images', subdir_path, filename + '_mask' + '_threshold' + f'.{extension}'), threshold_image)

        progress += 1
        print(f'Progresso: {progress}/{len(files)} imagens')
