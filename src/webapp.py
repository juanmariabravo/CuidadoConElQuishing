from flask import Flask, request, render_template_string
import os
from decoder import decode_qr
from analyzer import analyze_url

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QRShield Web</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 40px auto; background-color: #f4f4f9; color: #333; }
        h2 { color: #2c3e50; text-align: center; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .result { padding: 20px; border-radius: 6px; margin-top: 20px; border-left: 5px solid #ccc; }
        .SAFE { background-color: #d4edda; border-color: #28a745; color: #155724; }
        .SUSPICIOUS { background-color: #fff3cd; border-color: #ffc107; color: #856404; }
        .MALICIOUS { background-color: #f8d7da; border-color: #dc3545; color: #721c24; }
        .ERROR { background-color: #e2e3e5; border-color: #383d41; color: #383d41; }
        button { background-color: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 16px; transition: background 0.3s; }
        button:hover { background-color: #0056b3; }
        input[type="file"] { margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; width: 100%; box-sizing: border-box; }
        .footer { margin-top: 30px; text-align: center; font-size: 0.9em; color: #777; }
    </style>
</head>
<body>

<div class="container">
    <h2>🛡️ QRShield – Analizador de QR</h2>
    <p style="text-align: center;">Sube una imagen que contenga un código QR para analizarlo y detectar posibles amenazas de Quishing.</p>

    <form method="POST" enctype="multipart/form-data" style="text-align: center;">
        <input type="file" name="file" required accept="image/*" />
        <br>
        <button type="submit">Analizar Imagen</button>
    </form>

    {% if result %}
    <div class="result {{ result.classification }}">
        <h3>Resultado del Análisis</h3>
        <p><strong>URL detectada:</strong> <a href="{{ result.url }}" target="_blank" rel="noopener noreferrer">{{ result.url }}</a></p>
        <p><strong>Clasificación:</strong> <strong>{{ result.classification }}</strong></p>
        
        {% if result.reasons %}
            <p><strong>Razones de la clasificación:</strong></p>
            <ul>
            {% for r in result.reasons %}
                <li>{{ r }}</li>
            {% endfor %}
            </ul>
        {% else %}
            <p>✅ No se han detectado indicadores de compromiso conocidos.</p>
        {% endif %}
    </div>
    {% endif %}
</div>

<div class="footer">
    <p>QRShield MVP - Herramienta de Concienciación en Ciberseguridad</p>
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        if 'file' not in request.files:
            return render_template_string(HTML, result=None)
        
        file = request.files["file"]
        if file.filename == '':
            return render_template_string(HTML, result=None)

        # Save temporarily
        path = "temp_qr_upload.png"
        try:
            file.save(path)
            url = decode_qr(path)
            if url:
                result = analyze_url(url)
            else:
                result = {"url": "N/A", "classification": "ERROR", "reasons": ["No se pudo decodificar el código QR de la imagen. Asegúrate de que la imagen sea clara."]}
        except Exception as e:
             result = {"url": "Error", "classification": "ERROR", "reasons": [f"Error procesando el archivo: {str(e)}"]}
        finally:
            if os.path.exists(path):
                os.remove(path)

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
