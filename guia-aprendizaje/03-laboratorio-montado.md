# 03 · El laboratorio que montamos

> Qué tienes corriendo ahora mismo y cómo controlarlo. Guárdate los comandos de este archivo: te servirán cada vez que retomes el proyecto.

## Diagrama de lo que tenemos

```
   Tu navegador (Safari/Chrome)
            │
            │  http://localhost:8080

   ┌───────────────────────┐
   │  Contenedor "dvwa"     │   ← Docker
   │  (imagen web-dvwa)     │
   │  Apache + PHP + MySQL  │
   └───────────────────────┘

   Carpeta lab/  (código descargado, NO corriendo)
   ├── dvwa-src/     → para SAST y SCA
   └── webgoat-src/  → para SCA
```

**Idea clave:** hay dos cosas distintas con DVWA:
1. **DVWA corriendo** (el contenedor Docker) → lo atacamos "en vivo" = **DAST**.
2. **El código de DVWA** (carpeta `lab/dvwa-src/`) → lo leemos = **SAST/SCA**.

## ¿Qué comando usamos para montarlo? (y qué significa)

```bash
docker run -d -p 8080:80 --name dvwa vulnerables/web-dvwa
```

| Parte | Qué hace |
|-------|----------|
| `docker run` | Crea y arranca un contenedor. |
| `-d` | *Detached*: corre en segundo plano (no bloquea la terminal). |
| `-p 8080:80` | Conecta el **puerto 8080 de tu Mac** con el **puerto 80 del contenedor** (donde escucha Apache). Por eso entras por `localhost:8080`. |
| `--name dvwa` | Le pone nombre "dvwa" al contenedor, para referirte a él fácil. |
| `vulnerables/web-dvwa` | La **imagen** que se descarga y ejecuta. |

## Comandos para controlar el laboratorio

**Ver qué contenedores están corriendo:**
```bash
docker ps
```

**Parar DVWA (sin borrarlo):**
```bash
docker stop dvwa
```

**Volver a arrancarlo (ya no se re-descarga):**
```bash
docker start dvwa
```

> Si paras el contenedor y lo vuelves a arrancar, **se reinicia la base de datos**. Tendrás que entrar de nuevo con `admin`/`password`, pulsar *Create / Reset Database* y volver a poner la seguridad en *Low*.

**Ver los mensajes/logs del contenedor (si algo falla):**
```bash
docker logs dvwa
```

**Borrar DVWA del todo (al terminar el proyecto):**
```bash
docker rm -f dvwa
```

**Borrar también la imagen descargada (liberar espacio):**
```bash
docker rmi vulnerables/web-dvwa
```

## Datos de acceso a DVWA

- URL: **http://localhost:8080**
- Usuario: **admin**
- Contraseña: **password**
- Nivel de seguridad para las pruebas: **Low**

## Repos descargados (para SAST/SCA)

```bash
lab/dvwa-src/     # git clone de https://github.com/digininja/DVWA
lab/webgoat-src/  # git clone de https://github.com/WebGoat/WebGoat
```

Son solo **código** (no se ejecutan). Los leeremos y escanearemos cuando lleguemos a los hallazgos SAST y SCA.
