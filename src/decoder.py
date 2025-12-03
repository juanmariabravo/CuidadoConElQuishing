from pyzbar.pyzbar import decode
from PIL import Image

def decode_qr(image_path: str) -> str | None:
    try:
        img = Image.open(image_path)
        data = decode(img)

        if not data:
            return None

        return data[0].data.decode("utf-8")

    except Exception as e:
        print(f"[ERROR] No se pudo leer el QR: {e}")
        return None
