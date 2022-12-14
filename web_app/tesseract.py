import pytesseract
from PIL import Image, ImageEnhance, ImageFilter


def tesseract(image):
    im = Image.open(image) # Ouverture du fichier image

    # Filtrage (augmentation du contraste)
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')

    # Lancement de la procédure de reconnaissance
    text = pytesseract.image_to_string(im)
    return text