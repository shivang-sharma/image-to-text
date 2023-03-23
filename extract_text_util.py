import cv2
import pytesseract


def extract_text(file_name):
    # load raw image
    img = cv2.imread("snips/" + file_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    # Perform text extraction
    data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
    print(data)
    return data
