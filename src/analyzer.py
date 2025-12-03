import tldextract
import re

SUSPICIOUS_KEYWORDS = ["login", "verify", "secure", "pay", "update", "confirm", "account", "signin", "bank"]
URL_SHORTENERS = ["bit.ly", "tinyurl.com", "cutt.ly", "t.co", "goo.gl", "is.gd", "buff.ly", "ow.ly"]

def analyze_url(url: str) -> dict:
    result = {
        "url": url,
        "classification": "SAFE",
        "reasons": []
    }

    # --- Regla 1: HTTPS ---
    if not url.startswith("https://"):
        result["classification"] = "SUSPICIOUS"
        result["reasons"].append("No usa HTTPS")

    # --- Regla 2: Acortadores ---
    try:
        ext = tldextract.extract(url)
        domain = f"{ext.domain}.{ext.suffix}"
        
        if domain in URL_SHORTENERS:
            result["classification"] = "SUSPICIOUS"
            result["reasons"].append(f"Uso de acortador de URLs ({domain})")
            
        # --- Regla 4: Dominio con números extraño ---
        # Simple heuristic: if domain part has digits and is not an IP
        if any(char.isdigit() for char in ext.domain) and not re.match(r"^\d+$", ext.domain):
             # Check if it looks like a common service (e.g. w3schools) or something suspicious
             # This is a loose rule, might flag legitimate things, but good for MVP
             result["classification"] = "SUSPICIOUS"
             result["reasons"].append("Dominio contiene números (posible typosquatting o generado)")

    except Exception:
        pass

    # --- Regla 3: Palabras sospechosas ---
    if any(word in url.lower() for word in SUSPICIOUS_KEYWORDS):
        result["classification"] = "SUSPICIOUS"
        result["reasons"].append("Contiene palabras clave sospechosas (login, verify, etc.)")

    # --- Regla 5: Uso de IP en lugar de dominio ---
    # Regex for IP address at start of URL
    ip_pattern = r"^https?://\d{1,3}(\.\d{1,3}){3}"
    if re.match(ip_pattern, url):
        result["classification"] = "MALICIOUS"
        result["reasons"].append("URL utiliza dirección IP directa en lugar de nombre de dominio")

    # Upgrade to MALICIOUS if multiple suspicious factors or specific bad combos
    if len(result["reasons"]) >= 2:
        result["classification"] = "MALICIOUS"

    return result
