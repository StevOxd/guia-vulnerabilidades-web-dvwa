# 09 · DAST-005 — CSRF (Cross-Site Request Forgery)

## Parte 1: para aprender

### ¿Qué es CSRF?
**CSRF** (falsificación de petición entre sitios) engaña al navegador de una víctima **que ya tiene la sesión abierta** para que ejecute una acción **sin su consentimiento**.

La clave: el navegador **envía automáticamente las cookies de sesión** en cada petición a un sitio. Si una página maliciosa logra que tu navegador mande una petición a DVWA (por ejemplo "cambiar mi contraseña"), DVWA la aceptará porque **viene con tu cookie válida**… aunque tú no quisieras hacerlo.

Analogía: es como si alguien falsificara una orden con **tu firma ya estampada**. El banco (DVWA) la ejecuta porque la firma (la cookie) es válida, sin verificar que **tú** realmente la pediste.

### ¿Por qué DVWA es vulnerable aquí?
Miramos su código real. El cambio de contraseña:
- Se hace con una petición **GET** (todo va en la URL).
- **No pide la contraseña actual.**
- **No usa un token anti-CSRF** (un valor secreto y único por formulario que el atacante no podría adivinar).

Entonces basta con lograr que la víctima (ya logueada) cargue esta URL:
```
http://localhost:8080/vulnerabilities/csrf/?password_new=csrf123&password_conf=csrf123&Change=Change
```
…y su contraseña cambia a `csrf123`.

### ¿Cómo se demuestra?
Para demostrarlo se utiliza una **página de ataque simulada** (`csrf_poc.html`) que aparenta ser un "premio". Contiene un formulario oculto que apunta a DVWA: al abrirla con una sesión de DVWA activa y hacer clic, la contraseña del usuario cambia. Esto demuestra que una web externa puede forzar acciones en la cuenta de la víctima.

> Nota técnica: los navegadores modernos protegen un poco con la política **SameSite** de cookies, por eso la PoC usa un **clic** (una navegación de nivel superior) en lugar de una imagen oculta. Aun así, la lección es la misma: no hay token anti-CSRF que detenga la petición.

### Categoría OWASP
**A01:2021 – Pérdida de Control de Acceso** (el CSRF se incluye aquí en la versión 2021).

## Parte 2: datos para el informe

| Campo | Valor |
|-------|-------|
| **ID** | DEVSECOPS-DAST-005 |
| **Técnica de Análisis** | DAST |
| **Vulnerabilidad (OWASP Top 10)** | A01 – Pérdida de Control de Acceso (CSRF) |
| **Nivel de Riesgo** | Medio |
| **Complejidad de Explotación** | Media |
| **Dirección / URL** | http://localhost:8080/vulnerabilities/csrf/ |

**Descripción específica:**
> La funcionalidad de cambio de contraseña se ejecuta mediante una petición GET que no incluye un token anti-CSRF ni solicita la contraseña actual. Esto permite a un atacante construir una página o enlace malicioso que, al ser visitado por una víctima con sesión activa, fuerza el cambio de su contraseña sin su conocimiento ni consentimiento. Se demostró el ataque con una página externa (`csrf_poc.html`) que modificó la contraseña de la cuenta administrativa.

**Evidencia (capturas a tomar):**
- `01_csrf_formulario.png` — Formulario legítimo de cambio de contraseña en DVWA.
- `02_csrf_poc.png` — Página maliciosa simulada (`csrf_poc.html`) abierta en el navegador.
- `03_csrf_exito.png` — Mensaje "Password Changed" tras el clic (la petición forjada fue aceptada).

**Tratabilidad / plan de acción:**
> - Incluir un **token anti-CSRF** único e impredecible en cada formulario que cambie estado, y validarlo en el servidor.
> - Usar métodos **POST** para acciones que modifican datos (no GET).
> - Marcar las cookies de sesión con el atributo **SameSite** (`Lax` o `Strict`).
> - Para acciones sensibles, **re-solicitar la contraseña actual** o un segundo factor.

---
**Estado:** evidencias capturadas y verificadas (`01_csrf_formulario.png`, `02_csrf_poc.png`, `03_csrf_exito.png`). Una página externa (`file://`) cambió la contraseña del admin ("Password Changed").
