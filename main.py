import io
import json

from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import StreamingResponse
import streamlit_authenticator as stauth

from config.envs import vars
from models.credentials import CredencialesInput

app = FastAPI(
    title=vars.API_NAME,
    description=vars.DESCRIPTION,
    version=vars.VERSION,
    #terms_of_service="https://misitio.com/terms/",
    #contact={
    #    "name": "Equipo de Desarrollo",
    #    "email": "dev@example.com",
    #},
    license_info={
        "name": vars.LICENSE,
        "url": vars.LICENSE_URL,
    }
)

# Función auxiliar
def guardar_sin_comentarios_espacios(contenido: str) -> str:
    lineas = contenido.split('\n')
    lineas_filtradas = [linea for linea in lineas if not linea.strip().startswith("#") and linea.strip()]
    return '\n'.join(lineas_filtradas)

def crear_credenciales(names, usernames, passwords):
    if not (len(names) == len(usernames) == len(passwords)):
        raise ValueError("Las listas names, usernames y passwords deben tener la misma longitud.")
    
    hashed_passwords = stauth.Hasher(passwords).generate()

    users_dict = {}
    for i in range(len(usernames)):
        users_dict[usernames[i]] = {
            "failed_login_attempts": 0,
            "logged_in": "False",
            "name": names[i],
            "password": hashed_passwords[i]
        }

    contenido_dict = {"usernames": users_dict}
    contenido = json.dumps(contenido_dict, indent=4, ensure_ascii=False)
    contenido_sin_comentarios_espacios = guardar_sin_comentarios_espacios(contenido)

    return contenido_sin_comentarios_espacios

# Endpoint
@app.post("/crear-credenciales")
def api_crear_credenciales(
        data: CredencialesInput = Body(
                ...,
                example = {
                    "names": ["Nombre1 Apellido1", "Nombre2 Apellido2", "Nombre3 Apellido3", "Nombre4 Apellido4"],
                    "usernames": ["nombre1", "nombre2", "nombre3", "nombre4"],
                    "passwords": ["pass1", "pass2", "pass3", "pass4"]
                }
            )
        ):
    try:
        json_text = crear_credenciales(data.names, data.usernames, data.passwords)

        # Crear un archivo en memoria (BytesIO)
        buffer = io.BytesIO()
        buffer.write(json_text.encode('utf-8'))
        buffer.seek(0)

        # Devolver como archivo descargable
        return StreamingResponse(
            buffer,
            media_type="application/json",
            headers={
                "Content-Disposition": 'attachment; filename="credenciales.json"'
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))