from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Cargar modelo emocional
modelo_id = "project-nova/modelo_emocional_final"
emocionador = pipeline("text-classification", model=modelo_id, tokenizer=modelo_id, return_all_scores=True)

# Base de datos simulada en memoria
diario_personal = []
historia_clinica = []
contactos_emergencia = []

# Modelos de entrada
class Texto(BaseModel):
    texto: str

class Contacto(BaseModel):
    nombre: str
    telefono: str
    relacion: str

class HistoriaClinica(BaseModel):
    paciente_id: str
    resumen: str

# Endpoints

@app.get("/")
def raiz():
    return {"mensaje": "API psicólogo activa"}

@app.post("/procesar")
def procesar_texto(entrada: Texto):
    resultado = emocionador(entrada.texto)
    return {"emociones": resultado[0]}

@app.post("/paciente/diario")
def guardar_diario(entrada: Texto):
    diario_personal.append(entrada.texto)
    return {"mensaje": "Entrada guardada en el diario"}

@app.get("/paciente/diario")
def ver_diario():
    return {"diario": diario_personal}

@app.post("/paciente/historia_clinica")
def agregar_historia(datos: HistoriaClinica):
    historia_clinica.append(datos.dict())
    return {"mensaje": "Historia clínica guardada"}

@app.get("/paciente/historia_clinica")
def ver_historia():
    return {"historia_clinica": historia_clinica}

@app.post("/paciente/contactos")
def agregar_contacto(contacto: Contacto):
    contactos_emergencia.append(contacto.dict())
    return {"mensaje": "Contacto de emergencia guardado"}

@app.get("/paciente/contactos")
def ver_contactos():
    return {"contactos": contactos_emergencia}