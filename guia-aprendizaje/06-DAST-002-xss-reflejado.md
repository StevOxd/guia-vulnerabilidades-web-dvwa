# 06 · DAST-002 — XSS Reflejado (Cross-Site Scripting)

## Parte 1: para aprender

### ¿Qué es XSS?
**XSS** (*Cross-Site Scripting*) ocurre cuando una web **muestra en la página lo que escribió el usuario sin limpiarlo**, y ese texto puede incluir **código JavaScript** que el navegador de la víctima **ejecuta como si fuera parte del sitio**.

Mientras que la inyección SQL ataca a la **base de datos**, el XSS ataca al **navegador de otros usuarios**.

### ¿"Reflejado"? ¿hay otros tipos?
Sí, hay varios. Los dos más comunes:
- **Reflejado (este):** el código malicioso viaja en la **petición actual** (por ejemplo, en un enlace trampa que le mandas a la víctima). Se "refleja" de vuelta en la respuesta y se ejecuta una sola vez. **No se guarda.**
- **Almacenado (DAST-003, el siguiente):** el código se **guarda en el servidor** (por ejemplo en un comentario) y afecta a **todo el que vea esa página**. Es más peligroso.

### ¿Cómo se ve el fallo?
En DVWA hay un campo "What's your name?". Si escribes `Steven`, la página responde `Hello Steven`. El problema: si escribes código, lo "pega" tal cual en el HTML:

```
Entrada:  <script>alert('XSS')</script>
Respuesta: Hello <script>alert('XSS')</script>   ← el navegador lo EJECUTA
```

### ¿Por qué es peligroso?
Con XSS un atacante puede, en el navegador de la víctima:
- **Robar cookies de sesión** → suplantar su sesión (entrar como ella sin su contraseña).
- Registrar lo que teclea (keylogger), redirigirla a sitios falsos, modificar la página (phishing).
- Realizar acciones en su nombre.

El robo de cookie se demuestra con `<script>alert(document.cookie)</script>`: si aparece la cookie de sesión (`PHPSESSID`), significa que un script podría enviársela a un atacante.

### Categoría OWASP
**A03:2021 – Inyección** (XSS está dentro de esta categoría en la versión 2021).

### Payloads que usaremos
| Payload (en "What's your name?") | Qué demuestra |
|---|---|
| `Steven` | Uso normal (línea base). |
| `<script>alert('XSS')</script>` | Ejecuta JavaScript → aparece una ventana emergente = hay XSS. |
| `<script>alert(document.cookie)</script>` | Muestra la **cookie de sesión** → prueba del impacto (robo de sesión). |

## Parte 2: datos para el informe

| Campo | Valor |
|-------|-------|
| **ID** | DEVSECOPS-DAST-002 |
| **Técnica de Análisis** | DAST |
| **Vulnerabilidad (OWASP Top 10)** | A03 – Inyección (Cross-Site Scripting) |
| **Nivel de Riesgo** | Alto |
| **Complejidad de Explotación** | Baja |
| **Dirección / URL** | http://localhost:8080/vulnerabilities/xss_r/ |

**Descripción específica:**
> El parámetro "name" se refleja en la respuesta HTML sin codificación ni validación de salida, permitiendo la inyección y ejecución de código JavaScript arbitrario en el navegador de la víctima (Cross-Site Scripting reflejado). Se confirmó la ejecución de scripts y el acceso a la cookie de sesión (`document.cookie`), lo que posibilita el robo de sesión, el phishing y la ejecución de acciones en nombre del usuario.

**Evidencia (capturas a tomar):**
- `01_xss_r_normal.png` — Entrada normal ("Hello Steven"), línea base.
- `02_xss_r_alert.png` — Ventana emergente ejecutada por `<script>alert('XSS')</script>`.
- `03_xss_r_cookie.png` — `document.cookie` mostrando la cookie de sesión (impacto).

**Tratabilidad / plan de acción:**
> - **Codificar la salida** (output encoding) según el contexto (HTML, atributo, JS) al mostrar datos del usuario.
> - Validar y sanear las entradas (listas blancas).
> - Implementar **Content Security Policy (CSP)** para limitar la ejecución de scripts.
> - Marcar las cookies de sesión como `HttpOnly` (evita que JavaScript las lea) y `Secure`.

---
**Estado:** evidencias capturadas y verificadas (`01_xss_r_normal.png`, `02_xss_r_alert.png`, `03_xss_r_cookie.png`). Se confirmó ejecución de JS y exposición de la cookie de sesión.
