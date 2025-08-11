from dotenv import load_dotenv
import os

load_dotenv()

AIMHARDER_URL = os.getenv("AIMHARDER_URL", "https://aimharder.com")
USUARIO = os.getenv("USUARIO")
CONTRASENA = os.getenv("CONTRASENA")

if not USUARIO or not CONTRASENA:
    raise RuntimeError("Faltan credenciales: define USUARIO y CONTRASENA en .env o variables de entorno.")
