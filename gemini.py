import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar las variables de entorno
API_KEY = os.getenv('GEMINI_API_KEY')
URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}'

def consultar_google_ai(prompt):
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(URL, headers=headers, json=body)

    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        print("Error:", response.text)
        return "Error al procesar la consulta."
