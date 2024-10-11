import cv2
from flask import Flask, request, send_file
import os

app = Flask(__name__)

def center_image(image, output_size=(500, 500)):
    # Obtener dimensiones de la imagen
    h, w, _ = image.shape

    # Calcular el factor de escala para que la imagen se ajuste al tamaño objetivo
    scale = min(output_size[0] / w, output_size[1] / h)

    # Redimensionar la imagen conservando la proporción
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized_image = cv2.resize(image, (new_w, new_h))

    # Crear un lienzo del tamaño deseado con un color de fondo (negro)
    canvas = np.zeros((output_size[1], output_size[0], 3), (0, 100, 0), dtype=np.uint8)

    x_offset = (output_size[0] - new_w) // 2
    y_offset = (output_size[1] - new_h) // 2

    # Copiar la imagen redimensionada al lienzo
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_image

    return canvas

@app.route('/resize-image', methods=['POST'])
def resize_image():
    if 'image' not in request.files:
        return "No image file found", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    # Leer la imagen desde el archivo
    np_img = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    if image is None:
        return "Error processing the image", 400

    # Redimensionar y centrar la imagen
    centered_image = center_image(image)

    # Guardar la imagen temporalmente
    output_path = "imagen_centrada.jpg"
    cv2.imwrite(output_path, centered_image)

    # Devolver la imagen resultante
    return send_file(output_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)