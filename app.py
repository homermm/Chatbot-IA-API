import os
from flask import Flask, request, jsonify
from google import genai
import json
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de API desde la variable de entorno
API_KEY = os.getenv('GEMINI_API_KEY')

# Crear cliente de la API de Google GenAI con la clave de API
client = genai.Client(api_key=API_KEY)

app = Flask(__name__)

@app.route('/procesar', methods=['POST'])
def procesar_mensaje():
    # Obtener los datos de la solicitud
    data = request.json
    mensaje_usuario = data.get('mensaje')

    # Verificar que se haya recibido un mensaje
    if not mensaje_usuario:
        return jsonify({"error": "No se recibió mensaje"}), 400

    try:
        # Paso 1: Obtener la respuesta generada por la IA
        respuesta_ai = obtener_respuesta_ai(mensaje_usuario) 

        # Paso 2: Intentamos detectar si la IA ha devuelto un JSON con los datos completos
        try:
            respuesta_json = json.loads(respuesta_ai)
            if respuesta_json.get('status') == 'datos completos':
                # Paso 3: Llamamos a nuestra API si ya están todos los datos
                resultado_api = llamar_a_mi_api(respuesta_json)
                return jsonify({
                    "respuesta": "Datos completos recibidos. Llamando a la API...",
                    "resultado_api": resultado_api
                })
        except Exception as e:
            # No se recibió un JSON válido, continuamos preguntando
            pass

        # Si no hay datos completos, devolvemos la respuesta de la IA (seguimos la conversación)
        return jsonify({"respuesta": respuesta_ai})

    except Exception as e:
        return jsonify({"error": f"Error al procesar la consulta: {str(e)}"}), 500

def obtener_respuesta_ai(mensaje_usuario):
    # Llamar a la API de Google GenAI para obtener la respuesta
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=mensaje_usuario
    )
    return response.text

def llamar_a_mi_api(datos):
    # Esta función simula la llamada a una API externa para procesar los datos completos
    return "Datos procesados correctamente"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
