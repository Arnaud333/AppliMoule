from pyzbar import pyzbar
import cv2

def decode(image):
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    # for obj in decoded_objects:
    #     # draw the barcode
    #     # print("detected barcode:", obj)
    #     image = draw_barcode(obj, image)
    #     # print barcode type & data
    #     # print("Type:", obj.type)
    #     # print("Data:", obj.data)
    #     # print()

    return decoded_objects[0].data
def draw_barcode(decoded, image):
    # n_points = len(decoded.polygon)
    # for i in range(n_points):
    #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
    # uncomment above and comment below if you want to draw a polygon and not a rectangle
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
                            (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                            color=(0, 255, 0),
                            thickness=5)
    return image
