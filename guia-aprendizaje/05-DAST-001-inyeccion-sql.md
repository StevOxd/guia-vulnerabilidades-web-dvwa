# 05 · DAST-001 — Inyección SQL (SQLi)

## Parte 1: para aprender

### Primero: ¿qué es una base de datos y una "query"?
Las aplicaciones guardan su información (usuarios, contraseñas, productos…) en una **base de datos**. Para pedirle datos, la app le manda **consultas** escritas en un lenguaje llamado **SQL**. Por ejemplo, para buscar al usuario con ID 1:

```sql
SELECT first_name, last_name FROM users WHERE user_id = '1'
```

### ¿Qué es la Inyección SQL?
Ocurre cuando la app **construye la consulta pegando directamente lo que escribe el usuario**, sin limpiarlo. Si en la casilla "User ID" en vez de `1` escribes algo con comillas y comandos SQL, **tu texto se vuelve parte de la consulta** y puedes cambiar lo que hace.

Mira el código real de DVWA (lo confirmamos en su código fuente):
```php
$id = $_REQUEST['id'];                                   // lo que tú escribes
$query = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
```
Ese `'$id'` pega tu texto tal cual. Si escribes `1' OR '1'='1`, la consulta se convierte en:
```sql
SELECT first_name, last_name FROM users WHERE user_id = '1' OR '1'='1'
```
Como `'1'='1'` **siempre es verdadero**, la base de datos devuelve **todos los usuarios**, no solo el 1.

### ¿Por qué es tan peligroso?
Con inyección SQL un atacante puede:
- **Leer datos que no debería** (toda la tabla de usuarios, contraseñas, tarjetas…).
- **Saltarse el login** ("autenticación sin saber la contraseña").
- En casos graves, **modificar o borrar** datos, o incluso tomar control del servidor.

Es de las vulnerabilidades más críticas que existen. Por eso es la "estrella" del curso.

### Categoría OWASP
**A03:2021 – Inyección** (*Injection*). SQL Injection es el ejemplo más famoso de esta categoría.

### Los "payloads" que usaremos (y qué hace cada uno)
Un **payload** es el texto malicioso que escribimos para provocar la vulnerabilidad.

| Payload (lo escribes en "User ID") | Qué demuestra |
|---|---|
| `1` | Uso normal: devuelve solo el usuario 1. (Línea base para comparar.) |
| `1'` | Rompe la consulta y provoca un **error SQL** → confirma que el campo es inyectable. |
| `1' OR '1'='1` | Condición siempre verdadera → devuelve **todos los usuarios** (fuga de datos). |
| `' UNION SELECT user, password FROM users -- ` | Usa UNION para **extraer usuarios y sus contraseñas** (en hash MD5). |

> El `--` al final es un **comentario** en SQL: anula el resto de la consulta original para que no estorbe. (Nota: deja un espacio después de `--`.)

## Parte 2: datos para el informe

| Campo | Valor |
|-------|-------|
| **ID** | DEVSECOPS-DAST-001 |
| **Técnica de Análisis** | DAST |
| **Vulnerabilidad (OWASP Top 10)** | A03 – Inyección |
| **Nivel de Riesgo** | Crítico |
| **Complejidad de Explotación** | Baja |
| **Dirección / URL** | http://localhost:8080/vulnerabilities/sqli/ |

**Descripción específica:**
> El parámetro "id" del módulo de consulta de usuarios se concatena directamente en la sentencia SQL sin validación ni consultas parametrizadas. Esto permite a un atacante alterar la lógica de la consulta e inyectar comandos SQL arbitrarios. Se confirmó la extracción no autorizada de todos los registros de la tabla de usuarios, incluyendo nombres de usuario y los hashes de sus contraseñas, mediante payloads de tipo booleano (`1' OR '1'='1`) y de unión (`UNION SELECT`).

**Evidencia (capturas a tomar):**
- `01_sqli_normal.png` — Consulta normal con `id=1` (línea base).
- `02_sqli_error.png` — Error SQL al inyectar `1'` (confirma el punto inyectable).
- `03_sqli_todos_usuarios.png` — `1' OR '1'='1` devuelve todos los usuarios.
- `04_sqli_dump_passwords.png` — `UNION SELECT` extrae usuarios y hashes de contraseña.

**Tratabilidad / plan de acción:**
> - Usar **consultas parametrizadas / sentencias preparadas** (prepared statements), nunca concatenar entrada del usuario en el SQL.
> - Validar y sanear las entradas (listas blancas, tipos de dato esperados).
> - Aplicar el **principio de mínimo privilegio** a la cuenta de base de datos.
> - Usar un **ORM** o capa de acceso a datos segura y un **WAF** como defensa en profundidad.

---
**Estado:** evidencias capturadas (`01_sqli_normal.png`, `02_sqli_error.png`, `03_sqli_todos_usuarios.png`, `04_sqli_dump_passwords.png`). Verificado: se extrajeron todos los usuarios y hashes MD5.
