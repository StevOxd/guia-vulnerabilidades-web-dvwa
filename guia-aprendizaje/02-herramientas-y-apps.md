# 02 · Herramientas y aplicaciones que usamos

> Aquí explico cada "pieza" que instalamos o usamos, en palabras sencillas.

## Docker

**Qué es:** una herramienta para **empaquetar y ejecutar aplicaciones dentro de "cajas" aisladas** llamadas contenedores. En lugar de instalar DVWA, su servidor web, su base de datos y su versión exacta de PHP a mano (y arriesgarte a romper tu Mac), Docker trae **todo listo y empaquetado**.

**Por qué lo usamos:** para montar el laboratorio de forma **rápida, limpia y desechable**. Cuando terminemos, borramos el contenedor y tu computadora queda igual que antes, sin basura instalada.

### Conceptos de Docker

| Término | Qué es | Analogía |
|---------|--------|----------|
| **Imagen** | La "plantilla" congelada con la app y todo lo que necesita. | La **receta + ingredientes** empaquetados. |
| **Contenedor** | Una **copia en ejecución** de una imagen. Es la app ya corriendo. | El **platillo ya cocinado y servido**. |
| **Puerto** | La "puerta" por la que te comunicas con el contenedor. | El número de la casa para tocar el timbre. |

Ejemplo real de lo que hicimos: tomamos la **imagen** `vulnerables/web-dvwa` y la pusimos a correr como un **contenedor** llamado `dvwa`, accesible en el **puerto** 8080.

## DVWA (Damn Vulnerable Web Application)

**Qué es:** una aplicación web **hecha a propósito para ser insegura**. Su nombre significa literalmente "Aplicación Web Endemoniadamente Vulnerable". La crearon para que estudiantes y profesionales **practiquen ataques y defensas en un entorno legal y seguro**.

**Por qué es ideal para aprender:**
- Tiene un menú con las vulnerabilidades más clásicas: inyección SQL, XSS, subida de archivos, CSRF, etc.
- Tiene **niveles de seguridad** (Low, Medium, High, Impossible). En *Low* las vulnerabilidades están "abiertas" para que las veas funcionar; en *Impossible* están bien protegidas, para que compares el código correcto.
- Puedes ver el **código fuente** de cada nivel con un botón, así entiendes *por qué* falla.

**Importante:** DVWA es insegura **a propósito**. Nunca se expone a internet; solo se usa en un laboratorio local como el nuestro.

## WebGoat

**Qué es:** otra aplicación **deliberadamente vulnerable**, creada por **OWASP** (los del Top 10). Está hecha en Java y es más tipo "curso interactivo": te enseña lección por lección.

**Para qué la usamos aquí:** principalmente para el análisis **SCA**, porque al estar hecha en Java usa **muchas librerías de terceros** (dependencias), y ahí es fácil encontrar componentes con fallos conocidos.

## Git y repositorios

**Git** es el sistema más usado para **controlar versiones de código** (guardar el historial de cambios de un proyecto). Un **repositorio** ("repo") es el proyecto completo con todo su código e historial.

**GitHub** es un sitio web donde se publican repos. De ahí **clonamos** (descargamos una copia) el código de DVWA y WebGoat.

**Por qué clonamos el código:** para las técnicas **SAST** (leer el código buscando fallos) y **SCA** (revisar sus dependencias). Para esas dos técnicas necesitamos el **código fuente**, no solo la app corriendo.

## Trivy (lo instalaremos más adelante)

**Qué es:** un escáner de seguridad gratuito. Lo usaremos para **SCA**: revisará las dependencias de WebGoat (y/o la imagen de DVWA) y nos dirá qué componentes tienen **vulnerabilidades conocidas (CVE)**, con su gravedad. Es como un "antivirus de librerías".

> **CVE** = *Common Vulnerabilities and Exposures*. Es un identificador único y público para una vulnerabilidad ya conocida (ej. `CVE-2021-44228`, la famosa "Log4Shell"). Que algo tenga CVE significa que **ya está documentada y, normalmente, ya hay parche**.
