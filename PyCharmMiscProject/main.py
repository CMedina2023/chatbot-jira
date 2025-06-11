from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pptx import Presentation
from openai import OpenAI
import os

# Inicializa cliente OpenAI con tu clave
client = OpenAI(api_key="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")

app = FastAPI()

# Habilita CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Función para leer el contenido del PowerPoint
def cargar_conocimiento(path):
    texto = ""
    prs = Presentation(path)
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                texto += shape.text + "\n"
    return texto

conocimiento_jira = cargar_conocimiento("PLAN de Capacitacion.pptx")

# Endpoint para consultar
@app.post("/api/consultar")
async def consultar_jira(pregunta: str = Form(...)):
    print("📥 Pregunta recibida:", pregunta)

    prompt = f"""Eres un asistente de soporte técnico de Jira dentro de una empresa.
Utiliza la siguiente documentación interna para responder de forma clara:

{conocimiento_jira}

Pregunta del usuario: {pregunta}
Respuesta clara:"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente de soporte técnico de Jira para usuarios funcionales y técnicos."},
                {"role": "user", "content": prompt}
            ],  # ✅ Esto ahora es válido
            max_tokens=500,
            temperature=0.3
        )
        return {"respuesta": response.choices[0].message.content.strip()}
    except Exception as e:
        print("❌ Error:", e)
        return {"respuesta": f"❌ Error al generar respuesta: {str(e)}"}

# Monta HTML estático
app.mount("/", StaticFiles(directory="static", html=True), name="static")



