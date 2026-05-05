# Prueba simple de Azure AI Vision

Aplicacion Flask para probar OCR, descripcion, objetos, etiquetas y otras capacidades del endpoint de Azure AI Vision.

## Ejecutar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Abre `http://127.0.0.1:5000`.

## Datos requeridos

- Endpoint del recurso, por ejemplo `https://mi-recurso.cognitiveservices.azure.com`
- API key del recurso
- Una imagen cargada desde archivo o una URL publica de imagen

La aplicacion usa la API `imageanalysis:analyze` con version `2024-02-01` por defecto.
