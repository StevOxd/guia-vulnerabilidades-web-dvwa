# 07 · DAST-003 — XSS Almacenado (Stored XSS)

## Parte 1: para aprender

### ¿En qué se diferencia del XSS reflejado?
Es el **mismo problema** (la web ejecuta JavaScript que escribió un usuario), pero con una diferencia clave en **dónde queda el código**:

| | XSS Reflejado (DAST-002) | XSS Almacenado (DAST-003) |
|---|---|---|
| ¿Dónde vive el código? | En el enlace/petición (temporal) | **Guardado en la base de datos del servidor** |
| ¿A quién afecta? | Solo a quien abre el enlace trampa | **A TODOS los que visiten la página** |
| ¿Cuánto dura? | Una sola vez | Hasta que alguien lo borre (persistente) |
| Gravedad | Alta | **Más alta** |

Analogía: el reflejado es como dejarle una **nota trampa a una persona**; el almacenado es como **pintar la trampa en la pared de la recepción**, donde la ve y la "sufre" todo el que entra.

### ¿Cómo se ve el fallo?
DVWA tiene un **libro de visitas** (guestbook) con campos "Name" y "Message". Lo que escribes se **guarda** y se muestra a todos. Si en el mensaje pones `<script>...</script>`, ese script queda guardado y **se ejecuta cada vez que alguien abre la página**.

### ¿Por qué es peligroso?
Un solo mensaje malicioso puede, por ejemplo, **robar la cookie de sesión de cada visitante** automáticamente, afectar a administradores que revisen los comentarios, o propagar un "gusano" dentro del sitio. No necesita engañar a nadie para que haga clic: la víctima solo tiene que **visitar la página normal**.

### Categoría OWASP
**A03:2021 – Inyección** (Cross-Site Scripting).

### Payload que usaremos
| Campo | Qué escribir |
|---|---|
| Name | `Steven` (normal) |
| Message | `<script>alert('Stored XSS')</script>` |

> El campo "Message" tiene un límite de caracteres en el HTML, pero nuestro payload (29 caracteres) cabe sin problema en el nivel Low.

## Parte 2: datos para el informe

| Campo | Valor |
|-------|-------|
| **ID** | DEVSECOPS-DAST-003 |
| **Técnica de Análisis** | DAST |
| **Vulnerabilidad (OWASP Top 10)** | A03 – Inyección (Cross-Site Scripting Almacenado) |
| **Nivel de Riesgo** | Alto |
| **Complejidad de Explotación** | Baja |
| **Dirección / URL** | http://localhost:8080/vulnerabilities/xss_s/ |

**Descripción específica:**
> El campo "message" del libro de visitas almacena la entrada del usuario sin sanearla y la muestra a todos los visitantes sin codificación de salida. Esto permite inyectar código JavaScript que queda **persistido en el servidor** y se ejecuta automáticamente en el navegador de cualquier usuario que acceda a la página (Cross-Site Scripting almacenado). Al no requerir interacción de la víctima más allá de visitar la página, su impacto es mayor que el del XSS reflejado: posibilita el robo masivo de sesiones y el compromiso de cuentas administrativas.

**Evidencia (capturas a tomar):**
- `01_xss_s_formulario.png` — Formulario con el payload escrito en "Message" antes de enviar.
- `02_xss_s_alert.png` — Ventana emergente al guardar el mensaje (se ejecuta el script).
- `03_xss_s_persistente.png` — Al **recargar** la página, la alerta vuelve a aparecer sin reenviar nada (prueba de persistencia).

**Tratabilidad / plan de acción:**
> - **Codificar la salida** al mostrar cualquier contenido almacenado proveniente de usuarios.
> - Sanear y validar la entrada en el momento de guardarla (listas blancas, librerías anti-XSS).
> - Implementar **Content Security Policy (CSP)**.
> - Marcar las cookies de sesión como `HttpOnly` y `Secure`.

---
**Estado:** evidencias capturadas y verificadas (`01_xss_s_formulario.png`, `02_xss_s_alert.png`, `03_xss_s_persistente.png`). Se confirmó la persistencia (la alerta se dispara al recargar sin reenviar datos).
