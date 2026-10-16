# Guía de aprendizaje — Proyecto Final Seguridad Web

Notas personales que explican, desde cero, cada concepto y cada hallazgo de este
proyecto. Recomendado leerlas en orden.

## Índice

| # | Nota | Contenido |
|---|------|-----------|
| 01 | [Conceptos base](01-conceptos-base.md) | Qué es una vulnerabilidad, pentesting y las técnicas DAST / SAST / SCA. OWASP Top 10. |
| 02 | [Herramientas y aplicaciones](02-herramientas-y-apps.md) | Docker, contenedores, DVWA, WebGoat y repositorios (git). |
| 03 | [El laboratorio](03-laboratorio-montado.md) | Qué se ejecuta, en qué puertos y los comandos para controlar el entorno. |
| 04 | [DAST-009: Configuración insegura](04-DAST-009-configuracion-insegura.md) | Credenciales por defecto. |
| 05 | [DAST-001: Inyección SQL](05-DAST-001-inyeccion-sql.md) | Qué es SQL, SQLi y cómo extraer datos de la base. |
| 06 | [DAST-002: XSS Reflejado](06-DAST-002-xss-reflejado.md) | Qué es XSS y cómo se roba una sesión con JavaScript. |
| 07 | [DAST-003: XSS Almacenado](07-DAST-003-xss-almacenado.md) | XSS que se guarda y afecta a todos los visitantes. |
| 08 | [DAST-004: Inyección de Comandos](08-DAST-004-inyeccion-comandos.md) | Ejecutar comandos del sistema operativo en el servidor. |
| 09 | [DAST-005: CSRF](09-DAST-005-csrf.md) | Forzar acciones en nombre de una víctima con sesión abierta. |
| 10 | [DAST-006: Carga de archivos](10-DAST-006-carga-archivos.md) | Subir una web shell PHP y controlar el servidor. |
| 11 | [DAST-007: Inclusión de archivos (LFI)](11-DAST-007-inclusion-archivos.md) | Leer archivos del servidor con LFI y path traversal. |
| 12 | [DAST-008: Fuerza bruta](12-DAST-008-fuerza-bruta.md) | Adivinar contraseñas con un ataque de diccionario. |
| 13 | [SAST-001: Concatenación SQL](13-SAST-001-concatenacion-sql.md) | Leer el código y hallar la causa raíz de la inyección SQL. |
| 14 | [SAST-002: Hashing MD5](14-SAST-002-hashing-md5.md) | Por qué guardar contraseñas con MD5 es inseguro. |
| 15 | [SCA-001: Componentes vulnerables](15-SCA-001-dependencias.md) | Escanear dependencias/imagen con Trivy y hallar CVE. |

## Sobre el proyecto

Guía basada en una práctica de seguridad sobre aplicaciones web de una empresa
ficticia ("Marvel Tech"), en el rol de un consultor de seguridad. Se documentan
vulnerabilidades combinando pruebas dinámicas (DAST), análisis de código (SAST) y
análisis de componentes (SCA), clasificadas según el OWASP Top 10 (2021).

## Estructura

```
.
├── README.md
├── guia-aprendizaje/   notas de estudio (estas)
└── evidencias/         capturas y pruebas de concepto por vulnerabilidad
```
