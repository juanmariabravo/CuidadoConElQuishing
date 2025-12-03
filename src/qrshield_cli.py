import argparse
import sys
import os

# Add the current directory to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from decoder import decode_qr
from analyzer import analyze_url

def main():
    parser = argparse.ArgumentParser(description="QRShield – Detector básico de QR Phishing")
    parser.add_argument("--input", "-i", required=True, help="Ruta de la imagen del código QR")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ Error: El archivo '{args.input}' no existe.")
        return

    print("\n[+] Leyendo QR...")
    url = decode_qr(args.input)

    if not url:
        print("❌ No se pudo decodificar ningún QR en la imagen.")
        return

    print(f"[+] URL detectada: {url}")

    print("\n[+] Analizando URL...")
    analysis = analyze_url(url)

    print(f"\nClasificación: {analysis['classification']}")
    print("Razones:")

    if analysis["reasons"]:
        for r in analysis["reasons"]:
            print(f" - {r}")
    else:
        print(" - No se detectaron problemas evidentes.")

    print("\n✔ Análisis completado.\n")

if __name__ == "__main__":
    main()
