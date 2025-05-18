import cv2
import numpy as np

def adjust_brightness(image, value):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

def adjust_contrast(image, factor):
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)

def reduce_noise(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

def sharpen_image(image):
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def adjust_saturation(image, value):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype("float32")
    h, s, v = cv2.split(hsv)
    s = np.clip(s * value, 0, 255)
    final_hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(np.uint8(final_hsv), cv2.COLOR_HSV2BGR)

def image_thresholding(image, threshold_value=128):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)

def image_negative(image):
    return cv2.bitwise_not(image)

def image_rotating(image, angle=90):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, matrix, (w, h))

def image_flipping(image, direction='horizontal'):
    if direction == 'horizontal':
        return cv2.flip(image, 1)
    elif direction == 'vertical':
        return cv2.flip(image, 0)

def image_zooming(image, scale=1.5):
    h, w = image.shape[:2]
    return cv2.resize(image, None, fx=scale, fy=scale)

def image_shrinking(image, scale=0.5):
    h, w = image.shape[:2]
    return cv2.resize(image, None, fx=scale, fy=scale)

def image_logarithmic(image):
    image = image.astype(np.float32)  # pastikan float agar tidak overflow
    max_val = np.max(image)
    if max_val == 0:
        max_val = 1  # hindari log(0)
    c = 255 / np.log(1 + max_val)
    log_image = c * (np.log(1 + image))
    return np.uint8(np.clip(log_image, 0, 255))

def image_translation(image, tx=50, ty=50):
    rows, cols = image.shape[:2]
    matrix = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(image, matrix, (cols, rows))

def image_blending(image1, image2, alpha=0.5):
    image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
    return cv2.addWeighted(image1, alpha, image2, 1 - alpha, 0)
