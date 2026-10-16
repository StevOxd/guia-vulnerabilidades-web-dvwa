# 11 · DAST-007 — Inclusión de Archivos (LFI / Path Traversal)

## Parte 1: para aprender

### ¿Qué es?
Algunas webs cargan páginas o fragmentos usando un parámetro, por ejemplo `?page=include.php`. Si la app **usa ese valor para abrir un archivo sin validarlo**, puedes pedirle que abra **otros archivos del servidor** que no deberías ver.

- **LFI** (*Local File Inclusion*): incluir/leer un archivo **que está en el propio servidor** (ej. `/etc/passwd`).
- **Path Traversal** (recorrido de directorios): usar `../` para "subir" de carpeta y salir del directorio permitido. Cada `../` sube un nivel.
- **RFI** (*Remote File Inclusion*): incluir un archivo **desde otro servidor** (más raro hoy, suele estar deshabilitado).

### ¿Cómo se ve el fallo?
El código de DVWA (nivel Low) hace algo como:
```php
$file = $_GET['page'];
include($file);      // abre lo que pongas, sin filtrar
```
Entonces:
```
?page=/etc/passwd                 → lee el archivo de usuarios del sistema
?page=../../../../etc/passwd      → lo mismo, "escalando" carpetas con ../
```

### ¿Por qué es peligroso?
- **Fuga de información**: leer archivos de configuración, contraseñas, código fuente, logs.
- Si se combina con otra falla (como el archivo que subimos en DAST-006), puede llevar a **ejecución de código**.
- Revelar la estructura interna del servidor facilita otros ataques.

### Diferencia entre las dos capturas que tomarás
- `?page=/etc/passwd` usa una **ruta absoluta** (desde la raíz del sistema `/`).
- `?page=../../../../../../etc/passwd` usa **path traversal** (sube carpetas con `../`). Es la técnica clásica cuando la app añade una carpeta base delante de tu entrada.

### Categoría OWASP
**A01:2021 – Pérdida de Control de Acceso** (el acceso a archivos no autorizados y el path traversal entran aquí). También se relaciona con A03 (Inyección) cuando permite ejecutar código.

## Parte 2: datos para el informe

| Campo | Valor |
|-------|-------|
| **ID** | DEVSECOPS-DAST-007 |
| **Técnica de Análisis** | DAST |
| **Vulnerabilidad (OWASP Top 10)** | A01 – Pérdida de Control de Acceso (LFI / Path Traversal) |
| **Nivel de Riesgo** | Alto |
| **Complejidad de Explotación** | Baja |
| **Dirección / URL** | http://localhost:8080/vulnerabilities/fi/?page=include.php |

**Descripción específica:**
> El parámetro "page" se pasa directamente a la función `include()` sin validación ni restricción de ruta. Esto permite leer archivos arbitrarios del servidor mediante rutas absolutas (`/etc/passwd`) o recorrido de directorios (`../../`). Se confirmó la lectura del archivo `/etc/passwd`, exponiendo información sensible del sistema. Combinado con la carga de archivos (DAST-006), esta falla puede derivar en ejecución remota de código.

**Evidencia (capturas a tomar):**
- `01_lfi_normal.png` — Página incluida de forma normal (`?page=include.php`).
- `02_lfi_etc_passwd.png` — Lectura de `/etc/passwd` con ruta absoluta.
- `03_lfi_traversal.png` — Lectura de `/etc/passwd` con path traversal (`../../`).

**Tratabilidad / plan de acción:**
> - **No** usar entrada del usuario para construir rutas de archivos.
> - Usar una **lista blanca** de páginas permitidas (p. ej. un `switch` con valores fijos).
> - Validar y normalizar rutas; rechazar `../`, rutas absolutas y protocolos (`http://`, `php://`).
> - Deshabilitar `allow_url_include` y `allow_url_fopen` en PHP.

---
**Estado:** evidencias capturadas y verificadas (`01_lfi_normal.png`, `02_lfi_etc_passwd.png`, `03_lfi_traversal.png`). Lectura de `/etc/passwd` por ruta absoluta y por path traversal.
