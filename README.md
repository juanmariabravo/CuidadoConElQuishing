# QRShield – Detector de QR Phishing (Quishing)

QRShield es un detector sencillo y extensible de quishing (phishing mediante códigos QR).
Permite analizar imágenes que contienen códigos QR, extraer la URL y aplicar reglas básicas de seguridad para clasificarlas como:

*   ✔ **SAFE** (Seguro)
*   ⚠ **SUSPICIOUS** (Sospechoso)
*   ❌ **MALICIOUS** (Malicioso)

Este proyecto es un MVP (Producto Mínimo Viable) pensado como demostración práctica de ciberseguridad.

## 🚀 Características

*   **Decodificación**: Lee códigos QR desde imágenes (PNG/JPG).
*   **Análisis**: Motor de reglas heurísticas para detectar patrones de riesgo.
*   **Detección**:
    *   Falta de HTTPS.
    *   Palabras clave sospechosas (login, verify, secure, etc.).
    *   Uso de acortadores de URL conocidos.
    *   Dominios con patrones extraños (números, typosquatting).
    *   Uso de direcciones IP directas.
*   **Interfaces**:
    *   CLI (Línea de comandos) para análisis rápido.
    *   Web (Flask) para una interfaz gráfica amigable.

## 📁 Estructura del Proyecto

```
CuidadoConElQuishing/
│
├── src/
│   ├── qrshield_cli.py      # CLI principal
│   ├── decoder.py           # Módulo lector de QR
│   ├── analyzer.py          # Motor de análisis de URLs
│   ├── webapp.py            # Interfaz web (Flask)
│   ├── requirements.txt     # Dependencias
│   └── examples/            # Ejemplos de QRs (generados)
│       ├── safe_qr.png
│       ├── suspicious_qr.png
│       └── malicious_qr.png
├── README.md                # Documentación
└── LICENSE                  # Licencia
```

## 🔧 Instalación

1.  **Clonar el repositorio** (si no lo has hecho ya):
    ```bash
    git clone https://github.com/tuusuario/qrshield.git
    cd qrshield
    ```

2.  **Crear y activar un entorno virtual** (recomendado):
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r src/requirements.txt
    ```

    *Nota: En Linux/Mac es posible que necesites instalar `libzbar0` (ej: `sudo apt-get install libzbar0`).*

## ▶ Uso

### Desde Línea de Comandos (CLI)

Ejecuta el script `qrshield_cli.py` pasando la ruta de la imagen del QR:

```bash
python src/qrshield_cli.py --input src/examples/safe_qr.png
```

**Ejemplo de salida:**
```text
[+] Leyendo QR...
[+] URL detectada: https://example.com/menu

[+] Analizando URL...

Clasificación: SAFE
Razones:
 - No se detectaron problemas evidentes.

✔ Análisis completado.
```

### Desde Interfaz Web

1.  Inicia el servidor Flask:
    ```bash
    python src/webapp.py
    ```
2.  Abre tu navegador y ve a: `http://localhost:5000`
3.  Sube una imagen con un QR para ver el análisis en tiempo real.

## 🧪 Generación de Ejemplos

Puedes generar tus propios códigos QR de prueba usando el script incluido (o creando uno propio):

```python
import qrcode

# QR Seguro
qrcode.make("https://example.com/menu").save("src/examples/safe_qr.png")

# QR Sospechoso
qrcode.make("http://bit.ly/pay-confirm").save("src/examples/suspicious_qr.png")

# QR Malicioso
qrcode.make("http://192.168.1.50/login").save("src/examples/malicious_qr.png")
```

## 🔐 Reglas de Análisis

| Regla | Clasificación | Descripción |
| :--- | :--- | :--- |
| **HTTPS** | SUSPICIOUS | La URL no utiliza protocolo seguro (http://). |
| **Acortadores** | SUSPICIOUS | Uso de servicios como bit.ly, tinyurl, etc. que ocultan el destino. |
| **Keywords** | SUSPICIOUS | Presencia de palabras como 'login', 'verify', 'update', 'bank'. |
| **Typosquatting** | SUSPICIOUS | Dominios con números inusuales o patrones extraños. |
| **Dirección IP** | MALICIOUS | La URL apunta directamente a una IP (ej: 123.45.67.89). |

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.
