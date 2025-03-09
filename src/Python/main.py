from PIL import Image
import pillow_heif as ph
import os
import pytesseract
import re

# Set Tesseract path (adjust based on your installation)
# pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # Homebrew default path


## FUNTIONS-----------------------------------##
def convert_heic_to_jpg(image_path, output_path):
    heif_img = ph.open_heif(image_path)
    image = Image.frombytes(heif_img.mode, heif_img.size, heif_img.data)
    image.save(output_path, 'JPEG')

def check_image_format(image_path):
    if image_path.endswith('.heic') or image_path.endswith('.HEIC'):
        return 'heic'
    elif image_path.endswith('.jpg'):
        return 'jpg'
    else:
        return 'unsupported'

def process_image(image_path):
    # Open the image
    image = Image.open(image_path)
    # Perform OCR on the image
    return pytesseract.image_to_string(image)

def extract_price(text):
    price_pattern = r'(?i)(?:\$|USD\s?)?\d{1,5}(?:[.,]\d{2})?'
    prices = re.findall(price_pattern, text)
    
    # Return the first valid price (if any)
    return prices[-1] if prices else None

def extract_date(text):
    # Regex pattern to match different date formats
    date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\b\w{3,9} \d{1,2}, \d{4}\b|\d{4}-\d{2}-\d{2})'

    # Find all matches
    dates = re.findall(date_pattern, text)
    
    # Return the first valid date (if any)
    return dates[0] if dates else None

## MAIN----------------------------------------##
# Load an image from user prompt
ans = input('Do you want to load test image? (y/n): ')
if ans == 'y' or ans == 'Y':
    image_path = os.path.expanduser('~/Github/receipt-me/src/Python/test_images/IMG_0014.HEIC')
else:
    image_path = input('Type the path of the image: ')

# Check the image format
if check_image_format(image_path) == 'heic':
    convert_heic_to_jpg(image_path, 'temp.jpg')
    image_path = 'temp.jpg'
elif check_image_format(image_path) == 'unsupported':
    print('Unsupported format...')
    exit()

extracted_text = process_image(image_path)
extracted_price = extract_price(extracted_text)
extracted_date = extract_date(extracted_text)

# Print the extracted text
print("\n[EXTRACTED TEXT]")
print(extracted_text)
print("\n[EXTRACTED PRICE]")
print(extracted_price)
print("\n[EXTRACTED DATE]")
print(extracted_date)