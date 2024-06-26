import fitz  # PyMuPDF
import pytesseract
import cv2
from pytesseract import Output
import openai
import io
import numpy as np

openai.api_key = 'openai api key'
    
def extract_text_from_image(image_file):
    try:
        # Read the uploaded image file
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Convert image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
        
        # Configure Tesseract
        custom_config = r'--oem 3 --psm 6'
        
        # Extract text using Tesseract
        details = pytesseract.image_to_data(thresh_image, output_type=Output.DICT, config=custom_config)
        extracted_text = ""
        n_boxes = len(details['text'])
        
        # Collect text from detected boxes
        for i in range(n_boxes):
            if int(details['conf'][i]) > 50:
                extracted_text += details['text'][i] + " "
        
        print(extracted_text)
        
        return extracted_text
    except Exception as e:
        return str(e)

def extract_text_from_pdf(pdf_file):
    try:
        document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page_num in range(len(document)):
            page_text = document[page_num].get_text()
            text += page_text
        return text
    except Exception as e:
        return str(e)

def extract_health_info(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts key health information from text and give the medicine advice, diet plan and fitness plan"},
            {"role": "user", "content": f"Extract key health information from the following text: {text} and give the medicine advice, diet plan and fitness plan"}
        ]
    )
    return response.choices[0].message['content'].strip()

def generate_medicine_advice(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides medicine advice based on health information."},
            {"role": "user", "content": f"{text} and give the medicine advice"}
        ]
    )
    return response.choices[0].message['content'].strip()

def generate_diet_plan(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides diet plans based on health information."},
            {"role": "user", "content": f"{text} and give the diet plan"}
        ]
    )
    return response.choices[0].message['content'].strip()

def generate_fitness_plan(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides fitness plans based on health information."},
            {"role": "user", "content": f"{text} and give the fitness plan"}
        ]
    )
    return response.choices[0].message['content'].strip()