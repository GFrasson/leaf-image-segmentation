import cv2 as cv
import numpy as np


class K_Means_Opencv:
    def __init__(self, k_clusters):
        self.k_clusters = k_clusters
        self.image = None
        self.original_image_shape = None

    def __prepare_image(self, image):
        self.image = image
        self.original_image_shape = self.image.shape

        # Convertendo para o espectro RGB
        self.image = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)
        
        # Aplicando filtro Gaussiano
        self.image = cv.GaussianBlur(self.image, (7, 7), 0)

        # Redimensionando a imagem para uma matriz de 2 dimensões
        self.image = self.image.reshape((self.image.shape[0] * self.image.shape[1], 3))
        self.image = np.float32(self.image)

    def __kmeans_clustering(self):
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.85)  # Critério de parada
        return cv.kmeans(self.image, self.k_clusters, None, criteria, 10, cv.KMEANS_PP_CENTERS)  # Aplicando o método kmeans

    # Recria imagem a partir dos labels e centros encontrados pelo kmeans
    def __convert_to_segmented_image(self, centers, labels, shape):
        segmented_data = centers[labels.flatten()]
        return segmented_data.reshape(shape)

    def __get_threshold_image(self, centers, labels):
        # Intensidades da imagem binária
        binary_intensity = np.array([255, 0]) if centers[0][0] < centers[1][0] else np.array([0, 255])
        
        # Shape da imagem original com apenas um canal de cor
        shape = (self.original_image_shape[0], self.original_image_shape[1], 1)

        # Conversão do resultado do kmeans para a imagem binária
        threshold_image = self.__convert_to_segmented_image(binary_intensity, labels, shape)
        return threshold_image

    def __get_segmented_image(self, centers, labels):
        centers = np.uint8(centers)

        # Conversão do resultado do kmeans para a imagem segmentada
        segmented_image = self.__convert_to_segmented_image(centers, labels, self.original_image_shape)

        # Conversão para espectro BGR
        segmented_image = cv.cvtColor(segmented_image, cv.COLOR_RGB2BGR)
        return segmented_image

    def image_segmentation(self, image):
        # Preparação da imagem
        self.__prepare_image(image)

        # Aplicação do método kmeans
        retval, labels, centers = self.__kmeans_clustering()

        # Conversão do resultado para imagens
        # segmented_image = self.__get_segmented_image(centers, labels)
        threshold_image = self.__get_threshold_image(centers, labels)

        return threshold_image