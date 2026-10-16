# Guía práctica de vulnerabilidades web — DVWA & WebGoat

Guía práctica, con fines educativos, para **identificar, explotar de forma
controlada y documentar** vulnerabilidades web usando los laboratorios DVWA y
WebGoat. Pensada como material de estudio y referencia, paso a paso y desde cero.

Cubre **12 vulnerabilidades** combinando tres técnicas de análisis:
pruebas dinámicas (**DAST**), análisis de código (**SAST**) y análisis de
composición de software (**SCA**), clasificadas según el **OWASP Top 10 (2021)**.

---

## Aviso importante (uso educativo)

Todo el trabajo de este repositorio se realizó en un **laboratorio local, propio y
autorizado**, utilizando aplicaciones **diseñadas deliberadamente para ser
vulnerables** con fines de aprendizaje:

- **DVWA** (Damn Vulnerable Web Application)
- **WebGoat** (OWASP)

Las técnicas, scripts y pruebas de concepto aquí incluidos tienen **únicamente
fines educativos y de documentación**. No deben utilizarse contra sistemas sobre
los que no se tenga autorización explícita. El autor no se responsabiliza del uso
indebido de este material.

---

## Objetivos

- Identificar vulnerabilidades en aplicaciones web.
- Explotar de forma controlada dichas vulnerabilidades en un entorno de laboratorio.
- Analizar el impacto de seguridad de cada hallazgo.
- Documentar los resultados de forma profesional.

## Metodología y herramientas

| Técnica | Descripción | Herramientas |
|---------|-------------|--------------|
| DAST | Pruebas sobre la aplicación en ejecución | DVWA en Docker, navegador, scripts propios |
| SAST | Revisión del código fuente | Repositorios DVWA / WebGoat |
| SCA | Análisis de componentes y dependencias | Trivy |

Entorno: **Docker** (DVWA), **Python** (scripts de prueba), **Trivy** (SCA).

## Vulnerabilidades cubiertas

| ID | Técnica | Vulnerabilidad | OWASP Top 10 | Riesgo |
|----|---------|----------------|--------------|--------|
| DAST-001 | DAST | Inyección SQL | A03 – Inyección | Crítico |
| DAST-002 | DAST | XSS Reflejado | A03 – Inyección | Alto |
| DAST-003 | DAST | XSS Almacenado | A03 – Inyección | Alto |
| DAST-004 | DAST | Inyección de Comandos del SO | A03 – Inyección | Crítico |
| DAST-005 | DAST | CSRF | A01 – Control de Acceso | Medio |
| DAST-006 | DAST | Carga de archivos sin restricción | A05 – Config. Incorrecta | Crítico |
| DAST-007 | DAST | Inclusión de archivos (LFI) | A01 – Control de Acceso | Alto |
| DAST-008 | DAST | Fuerza bruta / autenticación débil | A07 – Autenticación | Alto |
| DAST-009 | DAST | Configuración insegura (credenciales por defecto) | A05 – Config. Incorrecta | Alto |
| SAST-001 | SAST | Concatenación de SQL en el código | A03 – Inyección | Crítico |
| SAST-002 | SAST | Hashing débil de contraseñas (MD5) | A02 – Fallos Criptográficos | Alto |
| SCA-001 | SCA | Componentes vulnerables y desactualizados | A06 – Componentes Vulnerables | Alto |

Distribución por riesgo: **4 Críticas, 7 Altas, 1 Media**.

## Estructura del repositorio

```
.
├── README.md
├── LICENSE
├── guia-aprendizaje/     Notas de estudio sobre cada concepto y hallazgo
└── evidencias/           Capturas y pruebas de concepto por vulnerabilidad
    ├── DAST-001_sqli/
    ├── DAST-002_xss-reflejado/
    ├── ...
    └── SCA-001_dependencias/
```

> Nota: la carpeta del laboratorio (`lab/`), los entregables en Word/PDF y el
> material original del curso no se incluyen en el repositorio (ver `.gitignore`).

## Guía de aprendizaje

La carpeta [`guia-aprendizaje/`](guia-aprendizaje/) contiene notas de estudio que
explican, desde cero, cada concepto y cada hallazgo. Comienza por el
[índice](guia-aprendizaje/00-INDICE.md).

## Cómo reproducir el laboratorio

```bash
# 1. Levantar DVWA en Docker
docker run -d -p 8080:80 --name dvwa vulnerables/web-dvwa
# Acceder a http://localhost:8080  (usuario: admin / contraseña: password)
# Pulsar "Create / Reset Database" y poner DVWA Security en "Low".

# 2. (SCA) Analizar la imagen con Trivy
trivy image --scanners vuln --severity HIGH,CRITICAL vulnerables/web-dvwa
```

## Autor

**Marvin Steven Ortiz Valle** — Proyecto final, Módulo 3 (Seguridad Web).

## Licencia

Distribuido bajo la licencia MIT. Ver el archivo [`LICENSE`](LICENSE).
