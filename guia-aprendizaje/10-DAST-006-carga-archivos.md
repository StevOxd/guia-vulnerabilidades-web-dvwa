# 10 · DAST-006 — Carga de Archivos sin Restricción (Web Shell)

## Parte 1: para aprender

### ¿Qué es?
Muchas webs permiten **subir archivos** (foto de perfil, documentos, etc.). Si la aplicación **no valida qué tipo de archivo** aceptas, un atacante puede subir un archivo **ejecutable del lado del servidor** (por ejemplo un `.php`) en vez de una imagen.

### ¿Qué es un "web shell"?
Es un pequeño programa (aquí, un archivo PHP) que, una vez subido al servidor, te permite **ejecutar comandos** en él a través del navegador. Es como instalar una **puerta trasera** (backdoor): a partir de ahí controlas la máquina.

### ¿Por qué DVWA es vulnerable aquí?
En nivel Low, el formulario de subida **acepta cualquier archivo** sin comprobar su tipo ni su contenido, y lo guarda en una carpeta **accesible desde el navegador** (`/hackable/uploads/`). Entonces:
1. Subimos `shell.php`.
2. DVWA nos dice la ruta donde quedó.
3. Abrimos esa ruta en el navegador y **ejecutamos comandos**.

### ¿Por qué es crítica?
Igual que la inyección de comandos, acaba en **RCE (ejecución remota de código)**: control total del servidor. Pero además deja una **puerta trasera persistente**: el archivo se queda ahí hasta que alguien lo borre.

### Categoría OWASP
Se relaciona con **A05:2021 – Configuración de Seguridad Incorrecta** y, sobre todo, con el diseño inseguro de la función de carga (**A04:2021 – Diseño Inseguro**). Para el informe la clasificaremos como **A05 (Carga de archivos sin restricción)**.

### El archivo que se sube
Se utiliza una web shell educativa (`shell.php`, guardada en el repositorio como `shell.php.txt` para que no sea ejecutable). Su contenido:
```php
<?php
  if (isset($_GET['cmd'])) { echo "<pre>"; system($_GET['cmd']); echo "</pre>"; }
  else { echo "Web shell activa. Usa ?cmd=comando"; }
?>
```
Recibe un comando por la URL (`?cmd=...`) y lo ejecuta en el servidor.

## Parte 2: datos para el informe

| Campo | Valor |
|-------|-------|
| **ID** | DEVSECOPS-DAST-006 |
| **Técnica de Análisis** | DAST |
| **Vulnerabilidad (OWASP Top 10)** | A05 – Configuración de Seguridad Incorrecta (Carga de archivos sin restricción) |
| **Nivel de Riesgo** | Crítico |
| **Complejidad de Explotación** | Baja |
| **Dirección / URL** | http://localhost:8080/vulnerabilities/upload/ |

**Descripción específica:**
> El formulario de carga de archivos no valida el tipo, la extensión ni el contenido del archivo subido, y lo almacena en un directorio accesible y ejecutable por el servidor web (`/hackable/uploads/`). Esto permitió subir un archivo PHP malicioso (web shell) y ejecutarlo desde el navegador, logrando la ejecución remota de comandos en el servidor (RCE) y estableciendo una puerta trasera persistente.

**Evidencia (capturas a tomar):**
- `01_upload_formulario.png` — Formulario de carga de archivos.
- `02_upload_exito.png` — Mensaje de subida exitosa con la ruta del archivo.
- `03_upload_shell_rce.png` — La web shell ejecutando un comando (`?cmd=whoami` o `id`) en el servidor.

**Tratabilidad / plan de acción:**
> - Validar el tipo real del archivo (listas blancas de extensiones y comprobación de contenido/MIME).
> - **Renombrar** los archivos y almacenarlos **fuera de la raíz web** o en un directorio **sin permisos de ejecución**.
> - Limitar tamaño y escanear con antivirus.
> - Servir las descargas a través de un script controlado, nunca por acceso directo.

---
**Estado:** evidencias capturadas y verificadas (`01_upload_formulario.png`, `02_upload_exito.png`, `03_upload_shell_rce.png`). Web shell subida y ejecutada (`?cmd=whoami` → www-data).
