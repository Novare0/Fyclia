# Ficlya — Extensión de navegador

**Ficlya** es una extensión de navegador diseñada para automatizar la navegación en FictionExpress y otros sitios de lectura. Incluye un sistema de IA para ayudar a responder quizzes mediante un servidor local que mantiene la clave del proveedor fuera del código del navegador.

## ✨ Características

- Automatización de la navegación en sitios de lectura compatibles.
- Asistente de IA para responder preguntas de quizzes.
- Servidor local para gestionar las solicitudes al proveedor de IA.
- Configuración del modelo utilizado por el asistente.
- Modo de práctica con una tasa configurable de respuestas incorrectas.

## 📦 Instalación

1. Descarga el proyecto desde GitHub mediante **Code → Download ZIP**, o clónalo con Git.
2. Si descargaste un ZIP, descomprímelo en una carpeta.
3. Abre Chrome y visita `chrome://extensions/`.
4. Activa el **Modo de desarrollador**.
5. Haz clic en **Cargar descomprimida** o **Cargar desempaquetada**, según la versión del navegador.
6. Selecciona la carpeta que contiene `manifest.json`.

Una vez instalada, puedes abrir la extensión desde el navegador.

## 🤖 Configuración del asistente de IA

El asistente utiliza un servidor local para comunicarse con el proveedor de IA sin exponer la clave API directamente en el navegador.

### Requisitos

- Python 3.11 o posterior.
- Una clave API válida del proveedor configurado.
- Acceso al modelo seleccionado en la configuración.

### 1. Configurar la clave API

Crea un archivo llamado `Key.txt` en la carpeta del proyecto y coloca la clave API en una sola línea.

**Importante:** no compartas este archivo ni lo subas a GitHub. Está excluido mediante `.gitignore`.

### 2. Iniciar el servidor

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
py ai_server.py
```

El servidor local estará disponible en:

`http://127.0.0.1:8765`

Mantén la terminal abierta mientras utilizas las funciones de IA.

### 3. Utilizar el asistente

1. Abre `chrome://extensions/`.
2. Recarga Ficlya.
3. Abre el sitio de lectura y accede al quiz.
4. Utiliza la función de IA de la extensión.

El texto del capítulo se envía al proveedor de IA para generar respuestas relacionadas con su contenido. Ten en cuenta que esto implica transmitir ese texto a un servicio externo.

## ⚙️ Configuración del modelo

El modelo predeterminado es:

`openai/gpt-oss-20b`

Puedes cambiarlo mediante la variable de entorno `QUIZ_AI_MODEL` antes de iniciar el servidor. Tu cuenta debe tener acceso al modelo elegido.

Ejemplo en PowerShell:

```powershell
$env:QUIZ_AI_MODEL = "openai/gpt-oss-20b"
py ai_server.py
```

## 🧪 Modo de práctica

Por defecto, el servidor no introduce errores intencionales en las respuestas.

Para probar el comportamiento de la extensión con respuestas incorrectas ocasionales, puedes configurar `QUIZ_ERROR_RATE`.

Por ejemplo, para establecer una tasa del 10 %:

```powershell
$env:QUIZ_ERROR_RATE = "0.10"
py ai_server.py
```

Esta configuración hace que aproximadamente el 10 % de las respuestas sean incorrectas de forma intencional. Utiliza esta opción únicamente para pruebas.

## 🛠️ Solución de problemas

**La extensión no aparece en Chrome**
- Comprueba que seleccionaste la carpeta que contiene `manifest.json`.
- Revisa si Chrome muestra algún error en `chrome://extensions/`.

**El asistente de IA no responde**
- Comprueba que el servidor esté ejecutándose.
- Verifica que `Key.txt` exista y contenga una clave válida.
- Confirma que tu cuenta tenga acceso al modelo configurado.
- Revisa los mensajes de error en la terminal de PowerShell.

**Los cambios no aparecen**
- Recarga Ficlya desde `chrome://extensions/`.
- Si modificaste el servidor Python, detén el proceso anterior y vuelve a iniciarlo.

## 🤝 Colaboraciones y contacto

¿Quieres colaborar, reportar un problema o proponer una mejora? Puedes ponerte en contacto por correo electrónico.

**Correo:** [novareestudio@gmail.com](mailto:novareestudio@gmail.com)

---

Desarrollado como un proyecto independiente bajo el nombre **Ficlya**.
