from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory=".")

# Ensure style.css is placed in the same folder as main.py
app.mount("/static", StaticFiles(directory="."), name="static")

def encode(text, key):
    return "".join(chr((ord(char) + key) % 256) for char in text)

def decode(text, key):
    return "".join(chr((ord(char) - key) % 256) for char in text)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/encoding", response_class=HTMLResponse)
def encoding_(request: Request, en: str = Form(...), num1: int = Form(...)):
    encoded_text = encode(en, num1)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"n1": encoded_text, "num1": num1}
    )

@app.post("/decoding", response_class=HTMLResponse)
def decoding_(request: Request, de: str = Form(...), num2: int = Form(...)):
    decoded_text = decode(de, num2)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"n2": decoded_text, "num2": num2}
    )