# 12 · DAST-008 — Fuerza Bruta (Brute Force)

## Parte 1: para aprender

### ¿Qué es un ataque de fuerza bruta?
Consiste en **probar muchísimas contraseñas** hasta dar con la correcta. Puede ser:
- **Fuerza bruta pura:** probar todas las combinaciones posibles (aaaa, aaab, …).
- **Ataque de diccionario:** probar una **lista de contraseñas comunes** (mucho más rápido y efectivo). Es lo que hace nuestro script.

### ¿Por qué funciona aquí?
Porque DVWA **no tiene defensas contra intentos repetidos**:
- No bloquea la cuenta tras varios fallos (no hay *account lockout*).
- No hay CAPTCHA ni retardo entre intentos.
- No limita la cantidad de peticiones (*rate limiting*).

Entonces un atacante puede lanzar miles de intentos por segundo con una herramienta automática.

### ¿Qué hace el script `fuerza_bruta.py`?
1. Inicia sesión en DVWA (necesario para acceder al módulo).
2. Pone la seguridad en Low.
3. Prueba una lista de contraseñas comunes para el usuario `admin`.
4. Detecta cuándo acierta (cuando la respuesta dice *"Welcome to the password protected area"*).

> En el mundo real se usan herramientas como **Hydra** o **Burp Intruder** y diccionarios con millones de contraseñas (p. ej. `rockyou.txt`). Nuestro script hace lo mismo a pequeña escala, para que entiendas el concepto.

### ¿Por qué es peligroso?
Si las contraseñas son débiles o comunes, un atacante entra en minutos. Combinado con cuentas sin segundo factor (MFA), es una de las vías de intrusión más usadas del mundo.

### Categoría OWASP
**A07:2021 – Fallos de Identificación y Autenticación** (*Identification and Authentication Failures*).

## Parte 2: datos para el informe

| Campo | Valor |
|-------|-------|
| **ID** | DEVSECOPS-DAST-008 |
| **Técnica de Análisis** | DAST |
| **Vulnerabilidad (OWASP Top 10)** | A07 – Fallos de Identificación y Autenticación |
| **Nivel de Riesgo** | Alto |
| **Complejidad de Explotación** | Media |
| **Dirección / URL** | http://localhost:8080/vulnerabilities/brute/ |

**Descripción específica:**
> El formulario de autenticación no implementa mecanismos de protección contra intentos repetidos: no existe bloqueo de cuenta, CAPTCHA, retardo progresivo ni limitación de peticiones. Esto permitió ejecutar un ataque de diccionario automatizado que, sin ser bloqueado en ningún momento, identificó la contraseña válida de la cuenta administrativa (`admin`). La ausencia de controles anti-fuerza bruta, sumada al uso de contraseñas comunes, facilita el compromiso de cuentas.

**Evidencia (capturas a tomar):**
- `01_fuerza_bruta_script.png` — Terminal ejecutando el script: se ven los intentos y la contraseña encontrada (`admin : password`) sin bloqueo.
- `02_brute_navegador_exito.png` — En el navegador, inicio de sesión exitoso en el módulo con la credencial obtenida ("Welcome to the password protected area").

**Tratabilidad / plan de acción:**
> - Implementar **bloqueo temporal de cuenta** tras N intentos fallidos y **retardo progresivo**.
> - Añadir **CAPTCHA** tras varios fallos y **limitación de peticiones** (rate limiting) por IP/usuario.
> - Exigir **contraseñas robustas** y **autenticación multifactor (MFA)**.
> - Monitorizar y alertar sobre picos de intentos de autenticación fallidos.

---
**Estado:** evidencias capturadas y verificadas (`01_fuerza_bruta_script.png`, `02_brute_navegador_exito.png`). El script probó 16 contraseñas sin bloqueo y encontró `admin:password`.
