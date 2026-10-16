# 01 · Conceptos base de seguridad web

> Nota para principiantes. Si no vienes del mundo de la seguridad, empieza aquí.

## ¿Qué es una vulnerabilidad?

Una **vulnerabilidad** es un **fallo o debilidad** en una aplicación que un atacante puede aprovechar para hacer algo que no debería: robar datos, entrar sin permiso, modificar información, tumbar el servicio, etc.

Analogía: si una casa es la aplicación, una vulnerabilidad es una **ventana sin seguro**. No significa que ya entraron, pero **el riesgo existe**.

## ¿Qué es un pentest (prueba de penetración)?

Es una **evaluación de seguridad autorizada**: alguien actúa como "atacante ético" para **encontrar las vulnerabilidades antes que los malos**, y así poder arreglarlas. Lo clave es la palabra **autorizado**: se hace con permiso y sobre sistemas propios o de práctica.

En este proyecto actuamos como **consultores de seguridad** contratados por una empresa ficticia. Y practicamos sobre aplicaciones **hechas a propósito para ser vulnerables** (DVWA y WebGoat), que es la forma correcta y legal de aprender.

## Las 3 técnicas que usaremos: DAST, SAST y SCA

El proyecto pide **variedad**, mezclando estas tres formas de buscar vulnerabilidades. Son complementarias:

| Técnica | Qué significa | Cómo trabaja | Analogía |
|---------|---------------|--------------|----------|
| **DAST** | *Dynamic Application Security Testing* (prueba **dinámica**) | Ataca la aplicación **mientras está corriendo**, desde afuera, como lo haría un hacker real (sin ver el código). | Probar si las puertas de la casa abren pateándolas. |
| **SAST** | *Static Application Security Testing* (prueba **estática**) | Revisa el **código fuente** sin ejecutar la app, buscando patrones peligrosos. | Leer los planos de la casa para ver dónde quedó una puerta mal diseñada. |
| **SCA** | *Software Composition Analysis* (análisis de **composición**) | Revisa las **librerías y dependencias** de terceros que usa la app, buscando componentes con fallos conocidos (CVE). | Revisar si las cerraduras que compraste (de otra marca) tienen un defecto ya reportado. |

**Por qué las tres importan:** una app puede estar bien programada (SAST limpio) pero usar una librería vieja con un fallo conocido (SCA lo detecta); o verse bien por fuera pero fallar al atacarla en vivo (DAST). Un buen análisis combina las tres.

## ¿Qué es OWASP y el "OWASP Top 10"?

**OWASP** (Open Worldwide Application Security Project) es una organización sin fines de lucro, referente mundial en seguridad de aplicaciones.

El **OWASP Top 10** es su lista de las **10 categorías de riesgos más críticos** en aplicaciones web. Es el "estándar" que usan los profesionales para clasificar hallazgos. En nuestro informe, cada vulnerabilidad se etiqueta con su categoría, por ejemplo:

- **A01 – Pérdida de Control de Acceso** (Broken Access Control)
- **A02 – Fallos Criptográficos** (Cryptographic Failures)
- **A03 – Inyección** (Injection: SQLi, XSS, comandos…)
- **A05 – Configuración de Seguridad Incorrecta** (Security Misconfiguration)
- **A06 – Componentes Vulnerables y Desactualizados**
- **A07 – Fallos de Identificación y Autenticación**

Clasificar con OWASP hace que el informe sea **profesional y comparable**: cualquier experto en el mundo entiende de qué hablas.

## Dos medidas que verás en cada hallazgo

- **Nivel de riesgo** (Bajo / Medio / Alto / Crítico): **qué tan grave** sería si alguien la explota. Combina el impacto (qué tanto daño) y la probabilidad.
- **Complejidad de explotación** (Baja / Media / Alta): **qué tan difícil** es aprovecharla. Ojo: *baja complejidad* es **peor**, porque cualquiera podría hacerlo.

Ejemplo: una inyección SQL que saca toda la base de datos escribiendo un texto simple = **riesgo Alto + complejidad Baja** = muy peligrosa.
