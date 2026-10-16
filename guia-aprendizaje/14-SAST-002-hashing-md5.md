# 14 · SAST-002 — Hashing débil de contraseñas (MD5)

## Parte 1: para aprender

### Primero: ¿qué es un "hash"?
Un **hash** es una función que convierte un texto (tu contraseña) en una cadena de longitud fija, en un solo sentido: del hash **no se puede volver** a la contraseña… en teoría. Por eso las apps **no guardan la contraseña**, sino su hash. Al iniciar sesión, calculan el hash de lo que escribes y lo comparan con el guardado.

### ¿Qué encontramos?
En el código, las contraseñas se procesan con **MD5**:
```php
// lab/dvwa-src/login.php  y  vulnerabilities/brute/source/low.php
$pass = md5( $pass );
```

### ¿Por qué MD5 es un problema para contraseñas?
1. **Es muy rápido de calcular** → un atacante puede probar **miles de millones** de hashes por segundo con una GPU.
2. **No lleva *salt*** (un valor aleatorio por usuario). Sin salt, **dos usuarios con la misma contraseña tienen el mismo hash**. ¿Recuerdas el DAST-001? `admin` y `smithy` tenían el **mismo hash** `5f4dcc3b5aa765d61d8327deb882cf99` → ambos usaban "password".
3. Existen **rainbow tables** y bases de datos públicas donde ese hash ya está resuelto. De hecho, `5f4dcc3b5aa765d61d8327deb882cf99` = `password` (búscalo en Google y lo confirmas).

Resultado: aunque las contraseñas estén "hasheadas", con MD5 se **crackean casi al instante**. Esto conecta directamente con la fuga de hashes del DAST-001: una vez robados, son triviales de revertir.

### ¿Qué se debe usar en su lugar?
Algoritmos **lentos y con salt**, diseñados para contraseñas: **bcrypt**, **scrypt** o **Argon2**. En PHP, `password_hash()` (usa bcrypt por defecto).

### Categoría OWASP
**A02:2021 – Fallos Criptográficos** (*Cryptographic Failures*).

## Parte 2: datos para el informe

| Campo | Valor |
|-------|-------|
| **ID** | DEVSECOPS-SAST-002 |
| **Técnica de Análisis** | SAST |
| **Vulnerabilidad (OWASP Top 10)** | A02 – Fallos Criptográficos |
| **Nivel de Riesgo** | Alto |
| **Complejidad de Explotación** | Media |
| **Dirección / URL** | Archivos: `login.php`, `vulnerabilities/brute/source/low.php` (repositorio DVWA) |

**Descripción específica:**
> La revisión del código fuente evidenció que las contraseñas se procesan con el algoritmo **MD5** (`$pass = md5( $pass );`) sin aplicar *salt*. MD5 es un algoritmo rápido y criptográficamente obsoleto para el almacenamiento de contraseñas: permite ataques de diccionario y rainbow tables a gran velocidad. La ausencia de salt provoca además que contraseñas idénticas generen hashes idénticos (confirmado en DAST-001, donde las cuentas `admin` y `smithy` comparten el mismo hash). En caso de fuga de la base de datos, las contraseñas se recuperan de forma casi inmediata.

**Evidencia (capturas a tomar):**
- `01_sast_md5_codigo.png` — Código fuente mostrando `$pass = md5( $pass );`.

**Tratabilidad / plan de acción:**
> - Reemplazar MD5 por un algoritmo de hashing de contraseñas **lento y con salt**: **bcrypt**, **scrypt** o **Argon2** (en PHP, `password_hash()` / `password_verify()`).
> - Aplicar un *salt* único por usuario (los algoritmos anteriores lo hacen automáticamente).
> - Forzar el restablecimiento de contraseñas tras la migración al nuevo esquema.
> - Considerar un *pepper* adicional y políticas de contraseñas robustas.

---
**Estado:** evidencia capturada y verificada (`01_sast_md5_codigo.png`). Código de `brute/source/low.php` mostrando `$pass = md5( $pass );`.
