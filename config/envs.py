import os
from dotenv import load_dotenv

#* -------------------- *#
#* VARIABLES DE ENTORNO *#
#* -------------------- *#
load_dotenv()

# Clase de configuracion de la aplicacion
class VariablesEntorno:
    def __init__(self):
        #? API DOCUMENTATION
        self.API_NAME = os.getenv("API_NAME", "DEFAULT")
        self.DESCRIPTION = os.getenv("DESCRIPTION", "DEFAULT")
        self.VERSION = os.getenv("VERSION", "DEFAULT")
        self.LICENSE = os.getenv("LICENSE", "DEFAULT")
        self.LICENSE_URL = os.getenv("LICENSE_URL", "DEFAULT")
        

vars = VariablesEntorno() #? Asignar las variables de entorno a la clase VariablesEntorno