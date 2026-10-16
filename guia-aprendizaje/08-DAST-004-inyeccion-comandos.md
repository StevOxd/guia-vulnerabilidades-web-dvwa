# 08 · DAST-004 — Inyección de Comandos del SO (Command Injection)

## Parte 1: para aprender

### ¿Qué es?
Algunas aplicaciones ejecutan **comandos del sistema operativo** (como los que escribirías en una terminal) usando datos del usuario. Si no los limpian, puedes **añadir tus propios comandos** y el servidor los ejecutará.

En DVWA hay una herramienta que hace *ping* a una dirección IP. Por dentro ejecuta algo así:
```php
$target = $_REQUEST['ip'];
shell_exec('ping -c 4 ' . $target);   // pega tu texto en el comando
```
Si en vez de una IP escribes `127.0.0.1; whoami`, el servidor ejecuta **dos comandos**:
```bash
ping -c 4 127.0.0.1    # el que esperaban
whoami                 # ¡el tuyo!
```

### Los "conectores" que permiten encadenar comandos
En Linux/Unix puedes unir comandos con estos símbolos:

| Símbolo | Significado |
|---|---|
| `;` | Ejecuta el siguiente comando **siempre**, uno tras otro. |
| `&&` | Ejecuta el siguiente **solo si el anterior tuvo éxito**. |
| `\|` | Pasa la salida de un comando al siguiente (pipe). |

### ¿Por qué es de las MÁS peligrosas?
Porque es prácticamente **control del servidor** (lo que se llama **RCE – Remote Code Execution**, ejecución remota de código). Un atacante podría:
- Ver usuarios y archivos del sistema (`cat /etc/passwd`).
- Descargar y ejecutar malware.
- Pivotar hacia la red interna de la empresa.
- Borrar o cifrar datos (ransomware).

### Categoría OWASP
**A03:2021 – Inyección** (Inyección de comandos del SO).

### Payloads que usaremos
| Payload (en "Enter an IP address") | Qué demuestra |
|---|---|
| `127.0.0.1` | Uso normal: hace ping (línea base). |
| `127.0.0.1; whoami` | Muestra **con qué usuario corre el servidor web** (ej. `www-data`). |
| `127.0.0.1; cat /etc/passwd` | **Lee un archivo del sistema** con la lista de usuarios → fuga de información del SO. |

## Parte 2: datos para el informe

| Campo | Valor |
|-------|-------|
| **ID** | DEVSECOPS-DAST-004 |
| **Técnica de Análisis** | DAST |
| **Vulnerabilidad (OWASP Top 10)** | A03 – Inyección (OS Command Injection) |
| **Nivel de Riesgo** | Crítico |
| **Complejidad de Explotación** | Baja |
| **Dirección / URL** | http://localhost:8080/vulnerabilities/exec/ |

**Descripción específica:**
> El parámetro "ip" de la herramienta de ping se concatena directamente en una llamada al sistema operativo (`ping`) sin validación ni saneamiento. Mediante conectores de shell (`;`) es posible encadenar y ejecutar comandos arbitrarios del sistema con los privilegios del servidor web. Se confirmó la ejecución de `whoami` (identificación del usuario del servicio) y la lectura del archivo `/etc/passwd`, demostrando una ejecución remota de código (RCE) que compromete por completo el servidor.

**Evidencia (capturas a tomar):**
- `01_cmd_normal.png` — Ping normal a `127.0.0.1` (línea base).
- `02_cmd_whoami.png` — Resultado de `127.0.0.1; whoami` (usuario del servidor).
- `03_cmd_etc_passwd.png` — Resultado de `127.0.0.1; cat /etc/passwd` (lectura de archivo del SO).

**Tratabilidad / plan de acción:**
> - **Evitar llamadas al sistema** con entrada del usuario; usar APIs/funciones nativas del lenguaje.
> - Si es imprescindible, usar **listas blancas** estrictas (p. ej. validar que la entrada sea una IP válida con una expresión regular).
> - Escapar argumentos con funciones seguras (`escapeshellarg`) y nunca construir comandos por concatenación.
> - Aplicar **mínimo privilegio** al usuario del servidor y aislar el servicio.

---
**Estado:** evidencias capturadas y verificadas (`01_cmd_normal.png`, `02_cmd_whoami.png`, `03_cmd_etc_passwd.png`). Se confirmó ejecución de comandos (`www-data`) y lectura de `/etc/passwd` (RCE).
