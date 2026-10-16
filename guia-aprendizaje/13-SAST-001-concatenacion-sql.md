# 13 · SAST-001 — Concatenación de SQL en el código fuente

> Primera vulnerabilidad por **SAST** (análisis estático = revisar el código, sin ejecutarlo).

## Parte 1: para aprender

### ¿Qué estamos haciendo distinto?
Hasta ahora hicimos **DAST** (atacar la app en vivo). Ahora hacemos **SAST**: abrimos el **código fuente** (que clonamos en `lab/dvwa-src/`) y buscamos **por qué** falla. SAST encuentra la **causa raíz** de un vistazo, antes incluso de desplegar la aplicación.

### ¿Qué encontramos?
En el archivo que genera la consulta de usuarios, el código pega la entrada del usuario **directamente** dentro de la sentencia SQL:

```php
// lab/dvwa-src/vulnerabilities/sqli/source/low.php
$id = $_REQUEST[ 'id' ];                                         // entrada del usuario
$query = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";  // ← PELIGRO
```

Ese `'$id'` es el problema: lo que escriba el usuario se vuelve **parte del código SQL**. Esta es exactamente la causa de la Inyección SQL que explotamos en DAST-001.

### ¿Cómo se vería el código correcto?
DVWA incluye la versión segura (`impossible.php`), que usa **consultas parametrizadas** (prepared statements):
```php
$data = $db->prepare('SELECT first_name, last_name FROM users WHERE user_id = (:id) LIMIT 1;');
$data->bindParam(':id', $id, PDO::PARAM_INT);   // el dato va SEPARADO del código
$data->execute();
```
Aquí el dato nunca se mezcla con la instrucción SQL → no hay inyección.

### ¿Por qué es valioso reportarlo por SAST?
Porque señala **la línea exacta** que hay que corregir y el **patrón** a evitar en todo el proyecto. DAST dice "la app es vulnerable"; SAST dice "arregla esta línea, así".

### Categoría OWASP
**A03:2021 – Inyección.**

## Parte 2: datos para el informe

| Campo | Valor |
|-------|-------|
| **ID** | DEVSECOPS-SAST-001 |
| **Técnica de Análisis** | SAST |
| **Vulnerabilidad (OWASP Top 10)** | A03 – Inyección |
| **Nivel de Riesgo** | Crítico |
| **Complejidad de Explotación** | Baja |
| **Dirección / URL** | Archivo: `vulnerabilities/sqli/source/low.php` (repositorio DVWA) |

**Descripción específica:**
> La revisión del código fuente reveló que el parámetro `id`, recibido directamente de `$_REQUEST`, se concatena sin saneamiento dentro de la sentencia SQL (`"... WHERE user_id = '$id';"`). Esta construcción dinámica de consultas mediante concatenación de entrada no confiable es la causa raíz de la inyección SQL: permite alterar la lógica de la consulta e inyectar comandos arbitrarios. El código no utiliza consultas parametrizadas ni validación de tipos.

**Evidencia (capturas a tomar):**
- `01_sast_sqli_codigo.png` — Código fuente con la línea vulnerable (`$query = "... '$id' ..."`).

**Tratabilidad / plan de acción:**
> - Sustituir la concatenación por **consultas parametrizadas / prepared statements** (como en `impossible.php`).
> - Validar el tipo de dato esperado (p. ej. que `id` sea entero).
> - Aplicar revisión de código y herramientas SAST en el pipeline de CI/CD para detectar este patrón automáticamente.

---
**Estado:** evidencia capturada y verificada (`01_sast_sqli_codigo.png`). Código fuente de `sqli/source/low.php` con la concatenación `'$id'` en la consulta SQL.
