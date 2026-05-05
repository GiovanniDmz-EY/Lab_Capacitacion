from __future__ import annotations

import base64
import json
import re
from urllib.parse import urlencode

import requests
from flask import Flask, render_template, request


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024


FEATURES = {
    "read": "OCR / Read",
    "caption": "Descripcion",
    "denseCaptions": "Descripciones densas",
    "objects": "Deteccion de objetos",
    "tags": "Etiquetas",
    "people": "Personas",
}


DATA_URL_RE = re.compile(r"^data:(?P<mimetype>image/[-+.\w]+);base64,(?P<data>.+)$", re.DOTALL)


def build_analyze_url(endpoint: str, features: list[str], language: str, api_version: str) -> str:
    base = endpoint.strip().rstrip("/")
    query = urlencode(
        {
            "api-version": api_version,
            "features": ",".join(features),
            "language": language,
        }
    )
    return f"{base}/computervision/imageanalysis:analyze?{query}"


def decode_image_data_url(value: str) -> tuple[str, bytes] | None:
    match = DATA_URL_RE.match(value.strip())
    if not match:
        return None

    try:
        return match.group("mimetype"), base64.b64decode(match.group("data"), validate=True)
    except ValueError:
        return None


def analyze_image(form, files) -> tuple[dict, int | None, str | None]:
    endpoint = form.get("endpoint", "").strip()
    api_key = form.get("api_key", "").strip()
    image_url = form.get("image_url", "").strip()
    persisted_image = form.get("persisted_image", "").strip()
    language = form.get("language", "es").strip() or "es"
    api_version = form.get("api_version", "2024-02-01").strip() or "2024-02-01"
    features = [feature for feature in form.getlist("features") if feature in FEATURES]

    if not endpoint or not api_key:
        raise ValueError("Captura el endpoint y el API key del recurso de Azure.")

    if not features:
        raise ValueError("Selecciona al menos una capacidad para analizar la imagen.")

    uploaded = files.get("image_file")
    has_upload = uploaded and uploaded.filename
    decoded_persisted_image = decode_image_data_url(persisted_image) if persisted_image else None
    has_persisted_image = decoded_persisted_image is not None

    if has_upload and image_url:
        raise ValueError("Usa archivo o URL, no ambos al mismo tiempo.")

    if has_upload:
        has_persisted_image = False

    if image_url:
        has_persisted_image = False

    if not has_upload and not image_url and not has_persisted_image:
        raise ValueError("Carga una imagen o pega el link de una imagen.")

    url = build_analyze_url(endpoint, features, language, api_version)
    headers = {"Ocp-Apim-Subscription-Key": api_key}

    if image_url:
        headers["Content-Type"] = "application/json"
        response = requests.post(url, headers=headers, json={"url": image_url}, timeout=60)
    elif has_upload:
        headers["Content-Type"] = uploaded.mimetype or "application/octet-stream"
        response = requests.post(url, headers=headers, data=uploaded.read(), timeout=60)
    elif has_persisted_image:
        mimetype, image_bytes = decoded_persisted_image
        headers["Content-Type"] = mimetype
        response = requests.post(url, headers=headers, data=image_bytes, timeout=60)

    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text}

    return payload, response.status_code, url


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    status_code = None
    request_url = None
    selected_features = ["read", "caption", "objects", "tags"]

    if request.method == "POST":
        selected_features = request.form.getlist("features") or selected_features
        try:
            result, status_code, request_url = analyze_image(request.form, request.files)
            result = json.dumps(result, ensure_ascii=False, indent=2)
        except requests.RequestException as exc:
            error = f"No se pudo llamar al servicio: {exc}"
        except ValueError as exc:
            error = str(exc)

    return render_template(
        "index.html",
        features=FEATURES,
        selected_features=selected_features,
        result=result,
        error=error,
        status_code=status_code,
        request_url=request_url,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
