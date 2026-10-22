# Ficlya - Extensión de Navegador

Automatiza la navegación en FictionExpress y otros sitios de lectura, simulando actividad humana para evitar detecciones de inactividad.

## 📦 Instalación Rápida

1. Descarga el archivo **`AutoFic_v1.0.zip`**.
2. Descomprímelo en una carpeta de tu PC.
3. Abre Chrome y ve a `chrome://extensions/`.
4. Activa el **Modo de desarrollador** (esquina superior derecha).
5. Haz clic en **Cargar descomprimida o puede decir desempaquetado** y selecciona la carpeta descomprimida.

## IA para responder quizzes

La extensión usa un proxy local para que la clave de IA no quede expuesta en el navegador.

1. Instala Python 3.11 o posterior.
2. Deja la clave del proveedor en `Key.txt`, en una sola línea. No la publiques ni la subas a Git.
3. Abre PowerShell en esta carpeta y ejecuta:

	```powershell
	py ai_server.py
	```

4. Recarga la extensión desde `chrome://extensions/` y abre el quiz.

El servidor escucha en `http://127.0.0.1:8765`. El texto del capítulo se envía al proveedor de IA para poder responder la pregunta.

El modelo predeterminado es `openai/gpt-oss-20b`. Puedes cambiarlo antes de iniciar el servidor con `$env:QUIZ_AI_MODEL` si tu cuenta tiene acceso a otro modelo.

Por defecto no introduce errores. Para el modo de práctica puedes iniciar el servidor con un porcentaje controlado, por ejemplo:

```powershell
$env:QUIZ_ERROR_RATE = "0.10"
py ai_server.py
```

Ese ejemplo hace que aproximadamente el 10% de las respuestas sean incorrectas de forma intencionada.


# si quiere colaborar enviar mensaje a este
### correo: novarestudio@gmail.com