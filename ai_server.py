import json
import os
import random
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


HOST = "127.0.0.1"
PORT = 8765
MODEL = os.environ.get("QUIZ_AI_MODEL", "openai/gpt-oss-20b")
ERROR_RATE = max(0.0, min(1.0, float(os.environ.get("QUIZ_ERROR_RATE", "0"))))
PROVIDER_URL = "https://api.groq.com/openai/v1/chat/completions"
SCORE_THRESHOLD = 7
sessions = {}


def load_api_key():
    key_path = Path(__file__).with_name("Key.txt")
    if not key_path.exists():
        raise RuntimeError("No existe Key.txt junto a ai_server.py")
    key = key_path.read_text(encoding="utf-8").strip()
    if not key:
        raise RuntimeError("Key.txt está vacío")
    return key


def clean_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("La IA no devolvió JSON")
    return json.loads(match.group(0))


def answer_question(payload):
    questions = payload.get("questions") or []
    if not questions:
        raise ValueError("Falta la pregunta")

    question = questions[0]
    options = [str(option).strip() for option in question.get("options", []) if str(option).strip()]
    if len(options) < 2:
        raise ValueError("Se necesitan al menos dos opciones")

    chapter = str(payload.get("chapterContent", ""))[:18000]
    prompt = {
        "question": str(question.get("question", "")),
        "options": options,
        "chapter": chapter,
    }
    system = (
        "Eres un asistente de comprensión lectora. Responde únicamente con JSON válido, "
        "sin markdown ni explicaciones. Usa exactamente el texto de una de las opciones. "
        "Elige la opción que esté mejor respaldada por el capítulo. Si no hay evidencia "
        "suficiente, elige la opción más razonable y baja la confianza. Formato: "
        '{"correctAnswer":"texto exacto de la opción","confidence":0.0,"reason":"breve"}'
    )
    body = {
        "model": MODEL,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
    }
    request = Request(
        PROVIDER_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {load_api_key()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Ficlya/1.0",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=45) as response:
            provider_data = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"Error del proveedor ({error.code}): {detail}") from error
    except URLError as error:
        raise RuntimeError(f"No se pudo conectar con el proveedor: {error.reason}") from error

    content = provider_data["choices"][0]["message"]["content"]
    result = clean_json(content)
    selected = str(result.get("correctAnswer", "")).strip()
    selected_normalized = re.sub(r"\s+", " ", selected).casefold()
    option = next((item for item in options if re.sub(r"\s+", " ", item).casefold() == selected_normalized), None)
    if option is None:
        raise ValueError("La IA devolvió una opción que no pertenece al quiz")
    intentionally_wrong = False
    if ERROR_RATE and random.random() < ERROR_RATE:
        alternatives = [item for item in options if item != option]
        if alternatives:
            option = random.choice(alternatives)
            intentionally_wrong = True

    session_key = "|".join(
        str(payload.get(field, "")).strip().casefold()
        for field in ("userName", "bookName", "chapterName")
    )
    session = sessions.setdefault(session_key, {"questions": 0, "answers": []})
    session["questions"] += 1
    session["answers"].append(option)
    return {
        "success": True,
        "answers": [{
            "number": question.get("questionNumber", session["questions"]),
            "question": question.get("question", ""),
            "correctAnswer": option,
            "confidence": 0.0 if intentionally_wrong else max(0, min(1, float(result.get("confidence", 0.5)))),
            "reason": str(result.get("reason", ""))[:300],
        }],
        "sessionQuestions": session["questions"],
        "requiresScore": True,
        "scoreThreshold": SCORE_THRESHOLD,
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, data):
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_OPTIONS(self):
        self._send(204, {})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length)
            try:
                body_text = raw_body.decode("utf-8")
            except UnicodeDecodeError:
                body_text = raw_body.decode("cp1252")
            payload = json.loads(body_text)
            if self.path == "/api/quiz-answer":
                self._send(200, answer_question(payload))
                return
            if self.path == "/api/quiz-finalize":
                self._send(200, {"success": True, "published": float(payload.get("score", 0)) >= SCORE_THRESHOLD})
                return
            self._send(404, {"success": False, "error": "Ruta no encontrada"})
        except (ValueError, KeyError, TypeError) as error:
            print(f"Solicitud inválida: {error}")
            self._send(400, {"success": False, "error": str(error)})
        except RuntimeError as error:
            print(f"Error del proveedor: {error}")
            self._send(502, {"success": False, "error": str(error)})
        except Exception as error:
            print(f"Error interno: {error}")
            self._send(500, {"success": False, "error": f"Error interno: {error}"})

    def log_message(self, format_string, *args):
        print(f"{self.address_string()} - {format_string % args}")


if __name__ == "__main__":
    print(f"Ficlya IA escuchando en http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()