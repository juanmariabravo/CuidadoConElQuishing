import qrcode
import os

# Ensure examples directory exists
output_dir = os.path.join(os.path.dirname(__file__), "examples")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Generando ejemplos en: {output_dir}")

# 1. Safe QR
# Normal HTTPS URL, no suspicious keywords
safe_url = "https://www.example.com/menu/dinner"
img = qrcode.make(safe_url)
img.save(os.path.join(output_dir, "safe_qr.png"))
print(f"[OK] Generado safe_qr.png -> {safe_url}")

# 2. Suspicious QR
# HTTP (no S), Shortener, Suspicious keyword 'confirm' (though bit.ly hides it, the analyzer checks the expanded URL if implemented, 
# but here our simple analyzer checks the string itself. 
# Let's make one that triggers our simple rules: HTTP + Keyword
suspicious_url = "http://login-secure-update.com/verify-account"
img = qrcode.make(suspicious_url)
img.save(os.path.join(output_dir, "suspicious_qr.png"))
print(f"[OK] Generado suspicious_qr.png -> {suspicious_url}")

# 3. Malicious QR
# IP Address
malicious_url = "http://192.168.1.50/admin/login"
img = qrcode.make(malicious_url)
img.save(os.path.join(output_dir, "malicious_qr.png"))
print(f"[OK] Generado malicious_qr.png -> {malicious_url}")

# 4. Another Suspicious (Shortener)
shortener_url = "https://bit.ly/free-prize"
img = qrcode.make(shortener_url)
img.save(os.path.join(output_dir, "shortener_qr.png"))
print(f"[OK] Generado shortener_qr.png -> {shortener_url}")

print("\n¡Ejemplos generados correctamente!")
