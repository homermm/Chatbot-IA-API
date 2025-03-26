from flask import Flask, request, jsonify
from gemini import consultar_google_ai
import json

app = Flask(__name__)

@app.route('/procesar', methods=['POST'])
def procesar_mensaje():
    data = request.json
    mensaje_usuario = data.get('mensaje')

    if not mensaje_usuario:
        return jsonify({"error": "No se recibió mensaje"}), 400

    # Paso 1: Pregunto a la IA
    respuesta_ai = consultar_google_ai(mensaje_usuario)

    try:
        # Intento detectar si la IA ya devolvio el JSON de datos completos
        respuesta_json = json.loads(respuesta_ai)

        if respuesta_json.get('status') == 'datos completos':
            # Paso 2: Llamo a mi API porque ya estan todos los datos
            resultado_api = llamar_a_mi_api(respuesta_json)
            return jsonify({
                "respuesta": "Datos completos recibidos. Llamando a la API...",
                "resultado_api": resultado_api
            })
    except Exception as e:
        # No hay JSON todavia, seguir preguntando
        pass

    # Si no hay datos completos, devolver la respuesta de la IA (seguimos la conversación)
    return jsonify({"respuesta": respuesta_ai})

def llamar_a_mi_api(datos):
    # Aca se llamaria a la API que procesa los datos completos
    return "Datos procesados correctamente"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
