# 15 · SCA-001 — Componentes vulnerables y desactualizados (SCA)

> Última técnica: **SCA** (análisis de composición de software).

## Parte 1: para aprender

### ¿Qué es SCA?
Ninguna aplicación se escribe 100% desde cero: usa **componentes de terceros** (librerías, el sistema operativo base, el servidor web, el lenguaje…). **SCA** revisa **todos esos componentes** y los compara con bases de datos de vulnerabilidades conocidas (**CVE**) para avisarte si alguno tiene fallos ya reportados.

Analogía: aunque tú construyas bien tu casa, si usas **ladrillos de un lote defectuoso ya reportado**, tu casa es insegura. SCA es el inspector que revisa la "lista de materiales".

### ¿Qué herramienta usamos?
**Trivy**, un escáner gratuito y muy usado. Puede escanear:
- El **código y sus dependencias** (ej. librerías de Java/Node/Python).
- **Imágenes de contenedores** (lo que hicimos): revisa el sistema operativo base y sus paquetes.

### ¿Qué escaneamos y qué encontramos?
Escaneamos la **imagen Docker de DVWA** (`vulnerables/web-dvwa`). El comando:
```bash
trivy image --scanners vuln --severity CRITICAL,HIGH vulnerables/web-dvwa
```
Resultado: la imagen está basada en **Debian 9.5**, una versión **antigua y sin soporte (EOL)**. Trivy encontró **805 vulnerabilidades** solo en severidad Alta/Crítica:

| Severidad | Cantidad |
|-----------|----------|
| CRITICAL  | 254 |
| HIGH      | 551 |
| **Total** | **805** |

Algunos ejemplos concretos (CVE críticos):
- **Apache** `CVE-2019-10082` — fallo de *read-after-free* en el servidor web.
- **PHP 7.0** (`libapache2-mod-php7.0`) `CVE-2017-8923` — desbordamiento que provoca caída.
- **glibc** (`libc6`) `CVE-2017-18269` — corrupción de memoria.

> **Nota:** primero intentamos escanear las dependencias de WebGoat, pero el repositorio de Maven bloqueó la descarga por exceso de peticiones (error 429). Por eso escaneamos la imagen de DVWA, que es un objetivo de SCA igualmente válido y se analiza sin conexión.

### ¿Por qué es importante?
Usar componentes desactualizados es el riesgo **A06** del OWASP Top 10. La mayoría de los ataques reales no explotan código nuevo, sino **vulnerabilidades conocidas en componentes que nadie actualizó** (el caso más famoso: Log4Shell en 2021).

### Categoría OWASP
**A06:2021 – Componentes Vulnerables y Desactualizados** (*Vulnerable and Outdated Components*).

## Parte 2: datos para el informe

| Campo | Valor |
|-------|-------|
| **ID** | DEVSECOPS-SCA-001 |
| **Técnica de Análisis** | SCA |
| **Vulnerabilidad (OWASP Top 10)** | A06 – Componentes Vulnerables y Desactualizados |
| **Nivel de Riesgo** | Alto |
| **Complejidad de Explotación** | Media |
| **Dirección / URL** | Imagen de contenedor: `vulnerables/web-dvwa` (base Debian 9.5) |

**Descripción específica:**
> El análisis de composición de software (SCA) con Trivy sobre la imagen del contenedor reveló que la aplicación se ejecuta sobre un sistema operativo base obsoleto y sin soporte (**Debian 9.5**, EOL), con un total de **805 vulnerabilidades conocidas** de severidad Alta y Crítica (254 críticas y 551 altas) en sus paquetes. Entre ellas destacan fallos críticos en Apache (`CVE-2019-10082`), PHP 7.0 (`CVE-2017-8923`) y glibc (`CVE-2017-18269`). El uso de componentes desactualizados con CVE públicos facilita la explotación mediante exploits ya disponibles.

**Evidencia (capturas a tomar):**
- `01_sca_trivy_resumen.png` — Salida de Trivy con el total de vulnerabilidades y los CVE críticos.
- *(Opcional)* `trivy_dvwa_reporte.txt` — Reporte completo ya guardado en esta carpeta.

**Tratabilidad / plan de acción:**
> - Actualizar la imagen base a una versión **con soporte** (p. ej. Debian estable actual) y actualizar PHP/Apache.
> - Establecer un proceso de **gestión de parches** y reconstrucción periódica de imágenes.
> - Integrar **SCA en el pipeline CI/CD** (Trivy, Dependency-Check) para bloquear componentes con CVE críticos.
> - Mantener un **inventario de dependencias (SBOM)** y suscribirse a avisos de seguridad.

---
**Estado:** evidencia capturada y verificada (`01_sca_trivy_resumen.png` + `trivy_dvwa_reporte.txt`). Trivy: 805 vulns (254 CRITICAL, 551 HIGH) en Debian 9.5.
