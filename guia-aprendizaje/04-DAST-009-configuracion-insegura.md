# 04 · DAST-009 — Configuración insegura (credenciales por defecto)

> Lo trabajamos primero porque la evidencia sale del propio arranque de DVWA.

## Parte 1: para aprender

### ¿Qué encontramos?
DVWA viene de fábrica con un usuario y contraseña **conocidos por todo el mundo**: `admin` / `password`. Cualquiera que conozca la aplicación (y esos datos están en toda su documentación pública) puede entrar como **administrador** sin ningún esfuerzo. Además, el nivel de seguridad se puede dejar en **Low**, que desactiva las protecciones.

### ¿Por qué es peligroso?
Las **credenciales por defecto** son una de las causas más comunes de intrusiones reales. Muchísimos equipos (routers, cámaras, paneles de administración, bases de datos) se instalan y **nadie cambia la contraseña inicial**. Un atacante solo tiene que probar las combinaciones por defecto, que están publicadas.

Analogía: es como comprar una caja fuerte y **dejar la combinación 0-0-0-0** que trae de fábrica y que viene impresa en el manual que cualquiera puede descargar.

### ¿A qué categoría OWASP pertenece?
**A05:2021 – Configuración de Seguridad Incorrecta** (*Security Misconfiguration*). Las cuentas y contraseñas por defecto son el ejemplo clásico de esta categoría.

## Parte 2: datos para el informe

Esta vulnerabilidad se documenta así:

| Campo | Valor |
|-------|-------|
| **ID** | DEVSECOPS-DAST-009 |
| **Técnica de Análisis** | DAST |
| **Vulnerabilidad (OWASP Top 10)** | A05 – Configuración de Seguridad Incorrecta |
| **Nivel de Riesgo** | Alto |
| **Complejidad de Explotación** | Baja |
| **Dirección / URL** | http://localhost:8080/login.php |

**Descripción específica:**
> La aplicación utiliza credenciales administrativas por defecto (`admin` / `password`) ampliamente conocidas y documentadas públicamente, que otorgan acceso completo al panel de administración sin necesidad de ningún ataque. Adicionalmente, la configuración de seguridad de la aplicación permite seleccionar un nivel permisivo ("Low") que desactiva los controles de protección. Esta combinación representa una configuración de seguridad incorrecta que facilita el acceso no autorizado.

**Evidencia:**
- `01_login_dvwa.png` — Inicio de sesión exitoso con las credenciales por defecto `admin` / `password`.
- `02_security_low.png` — Nivel de seguridad de la aplicación configurado en "Low".

**Tratabilidad / plan de acción:**
> - Forzar el cambio de contraseña en el primer inicio de sesión y eliminar o deshabilitar las cuentas por defecto.
> - Aplicar una política de contraseñas robustas (longitud, complejidad y rotación).
> - Establecer configuraciones seguras por defecto ("secure by default") y endurecer el servidor.
> - Retirar paneles de configuración y funciones de depuración en entornos productivos.
> - Habilitar bloqueo de cuenta y autenticación multifactor (MFA) para accesos administrativos.

---
**Estado:** evidencias capturadas (`01_login_dvwa.png`, `02_security_low.png`).
