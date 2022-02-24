from numpy import array
from cv2 import polylines, LINE_AA

def draw_contours_polylines(image, contornos, color: tuple = (0, 0, 255), thickness: int = 2):
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

            pts = array(pts)
            polylines(image, [pts], True, color, thickness, LINE_AA)

    return image
