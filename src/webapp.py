from flask import Flask, request, render_template_string, jsonify
import os
import time
from decoder import decode_qr
from analyzer import analyze_url

app = Flask(_name_)

# Modern, premium UI with Glassmorphism and smooth interactions
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CuidadoConElQuishing | Advanced Protection</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --bg-gradient: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            --glass-bg: rgba(255, 255, 255, 0.95);
            --glass-border: rgba(255, 255, 255, 0.2);
            --text-main: #1f2937;
            --text-muted: #6b7280;
            --shadow-lg: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
            
            /* Status Colors */
            --safe-bg: #ecfdf5; --safe-text: #065f46; --safe-border: #10b981;
            --suspicious-bg: #fffbeb; --suspicious-text: #92400e; --suspicious-border: #f59e0b;
            --malicious-bg: #fef2f2; --malicious-text: #b91c1c; --malicious-border: #ef4444;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-gradient);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-main);
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 600px;
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            box-shadow: var(--shadow-lg);
            overflow: hidden;
            transition: transform 0.3s ease;
        }

        .header {
            padding: 40px 40px 20px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(to right, #6366f1, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            letter-spacing: -0.02em;
        }

        .header p {
            color: var(--text-muted);
            font-size: 1.1rem;
        }

        .upload-area {
            margin: 20px 40px;
            border: 2px dashed #e5e7eb;
            border-radius: 16px;
            padding: 40px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: #fafafa;
            position: relative;
        }

        .upload-area:hover, .upload-area.dragover {
            border-color: var(--primary);
            background: #eef2ff;
            transform: scale(1.01);
        }

        .upload-icon {
            font-size: 48px;
            color: #9ca3af;
            margin-bottom: 15px;
            transition: color 0.3s;
        }

        .upload-area:hover .upload-icon {
            color: var(--primary);
        }

        .upload-text {
            font-weight: 500;
            color: var(--text-main);
            margin-bottom: 5px;
        }

        .upload-subtext {
            font-size: 0.875rem;
            color: var(--text-muted);
        }

        #fileInput {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            opacity: 0;
            cursor: pointer;
        }

        .result-container {
            padding: 0 40px 40px;
            display: none;
            animation: slideUp 0.4s ease-out;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .card {
            border-radius: 16px;
            padding: 25px;
            border-left: 6px solid transparent;
            background: white;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }

        .card.SAFE { background: var(--safe-bg); border-color: var(--safe-border); color: var(--safe-text); }
        .card.SUSPICIOUS { background: var(--suspicious-bg); border-color: var(--suspicious-border); color: var(--suspicious-text); }
        .card.MALICIOUS { background: var(--malicious-bg); border-color: var(--malicious-border); color: var(--malicious-text); }
        .card.ERROR { background: #f3f4f6; border-color: #4b5563; color: #1f2937; }

        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }

        .status-badge {
            font-size: 0.875rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 4px 12px;
            border-radius: 20px;
            background: rgba(255,255,255,0.5);
            margin-left: auto;
        }

        .url-box {
            background: rgba(255,255,255,0.6);
            padding: 12px;
            border-radius: 8px;
            font-family: 'Monaco', 'Consolas', monospace;
            word-break: break-all;
            font-size: 0.9rem;
            margin-bottom: 20px;
            border: 1px solid rgba(0,0,0,0.05);
        }

        .reasons-list {
            list-style: none;
        }

        .reasons-list li {
            margin-bottom: 8px;
            display: flex;
            align-items: start;
        }

        .reasons-list li::before {
            content: '•';
            margin-right: 10px;
            font-weight: bold;
        }

        .loader {
            display: none;
            margin: 20px auto;
            border: 4px solid #f3f3f3;
            border-top: 4px solid var(--primary);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        }

        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .footer {
            text-align: center;
            padding: 20px;
            font-size: 0.8rem;
            color: var(--text-muted);
            border-top: 1px solid rgba(0,0,0,0.05);
            background: rgba(255,255,255,0.5);
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>Cuidado Con El Quishing</h1>
        <p>Analizador Inteligente de Quishing</p>
    </div>

    <div class="upload-area" id="dropZone">
        <input type="file" id="fileInput" accept="image/*" name="file">
        <div class="upload-icon">📁</div>
        <div class="upload-text">Arrastra tu imagen aquí o haz clic</div>
        <div class="upload-subtext">Soporta PNG, JPG, JPEG</div>
    </div>

    <div class="loader" id="loader"></div>

    <div class="result-container" id="resultContainer">
        <!-- Results will be injected here -->
    </div>

    <div class="footer">
        Protegiendo tu seguridad digital • v1.0 MVP
    </div>
</div>

<script>
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('resultContainer');

    // Drag & Drop effects
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropZone.classList.add('dragover');
    }

    function unhighlight(e) {
        dropZone.classList.remove('dragover');
    }

    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFiles, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles({ target: { files: files } });
    }

    function handleFiles(e) {
        const files = e.target.files;
        if (files.length > 0) {
            uploadFile(files[0]);
        }
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        // UI Updates
        loader.style.display = 'block';
        resultContainer.style.display = 'none';
        dropZone.style.opacity = '0.5';
        dropZone.style.pointerEvents = 'none';

        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            showResult(data);
        })
        .catch(error => {
            console.error('Error:', error);
            showResult({
                classification: 'ERROR',
                url: 'Error de conexión',
                reasons: ['No se pudo conectar con el servidor.']
            });
        })
        .finally(() => {
            loader.style.display = 'none';
            dropZone.style.opacity = '1';
            dropZone.style.pointerEvents = 'auto';
        });
    }

    function showResult(data) {
        let icon = '';
        let title = '';
        
        switch(data.classification) {
            case 'SAFE': icon = '🛡'; title = 'Sitio Seguro'; break;
            case 'SUSPICIOUS': icon = '⚠'; title = 'Sospechoso'; break;
            case 'MALICIOUS': icon = '⛔'; title = 'Sitio Malicioso'; break;
            default: icon = '❓'; title = 'Error';
        }

        let reasonsHtml = '';
        if (data.reasons && data.reasons.length > 0) {
            reasonsHtml = '<ul class="reasons-list">' + 
                data.reasons.map(r => <li>${r}</li>).join('') + 
                '</ul>';
        } else {
            reasonsHtml = '<p>✅ No se encontraron amenazas conocidas.</p>';
        }

        const html = `
            <div class="card ${data.classification}">
                <div class="card-header">
                    <span style="font-size: 1.5rem; margin-right: 10px;">${icon}</span>
                    <h3 style="margin:0;">${title}</h3>
                    <span class="status-badge">${data.classification}</span>
                </div>
                <div class="url-box">
                    ${data.url}
                </div>
                <div>
                    <strong>Análisis:</strong>
                    <div style="margin-top: 10px;">
                        ${reasonsHtml}
                    </div>
                </div>
            </div>
        `;

        resultContainer.innerHTML = html;
        resultContainer.style.display = 'block';
    }
</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"classification": "ERROR", "url": "", "reasons": ["No se envió ningún archivo"]})
        
        file = request.files["file"]
        if file.filename == '':
            return jsonify({"classification": "ERROR", "url": "", "reasons": ["Nombre de archivo vacío"]})

        # Save temporarily
        path = f"temp_{int(time.time())}.png"
        try:
            file.save(path)
            url = decode_qr(path)
            
            if url:
                result = analyze_url(url)
                return jsonify(result)
            else:
                return jsonify({
                    "url": "N/A", 
                    "classification": "ERROR", 
                    "reasons": ["No se pudo decodificar el código QR. Intenta con una imagen más clara."]
                })
        except Exception as e:
             return jsonify({
                 "url": "Error interno", 
                 "classification": "ERROR", 
                 "reasons": [f"Error procesando el archivo: {str(e)}"]
             })
        finally:
            if os.path.exists(path):
                os.remove(path)

    return render_template_string(HTML)

if _name_ == "_main_":
    app.run(debug=True, port=5000)
