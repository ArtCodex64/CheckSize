# ------------------------------- #
#  INFORMACIÓN SOBRE EL PROGRAMA  #
# ------------------------------- #
#
# --------------------------------- #
#  Versión de Python: Python 3.10.1 #
# --------------------------------- #
#   
#
# -------------------- #
#  Fecha:  10-02-2022  #
# -------------------- #
#
# --------------------------- #
#  Autor:  ArtCodex64         #
# --------------------------- #
#
# ------------ #
# Descripción: # ----------------------------------------------------------------------------------------------------------------- #
#   Este programa sirve para listar las unidades de almacenamiento en red y borrar los archivos que no necesitemos.                #
#   También nos permite saber el peso de la unidad de almacenamiento Y.                                                            #
#   Podremos filtrar por diferentes extensiones de archivos (JPG, JPEG, PNG, TIFF, ...) y por su peso (Bytes, KB, MB, GB, TB)      #
#   Una vez obtenemos los archivos nos da la posibilidad de poder borrar el archivo o carpeta seleccionada.                        #
# -------------------------------------------------------------------------------------------------------------------------------- #
#
#
#
#
# --------------------- #
#  Librerias y módulos  #
# --------------------- #
#   Importamos las librerias y módulos necesarios para el correcto funcionamiento del programa en Python
import subprocess
import re

#CLASE EXTRAERUR
class extraerUR():
    def __init__(self):
        super().__init__()
    #Función EXTRAER
    def extraer(self):
        net = []
        #Extraemos las unidades (C:/, Y:/, Z:/, I:/...) con sus correspondientes nombres (GXXXXXXX, ...)
        netUS = subprocess.getoutput('net use')
        #Extraemos mediante una expresión regular todos lo valores que sea de la A-Z y contenga :
        netUSl = re.findall('[A-Z]{1}[:]{1}', netUS)
        #Extraemos mediante una expresión regular las dos palabars siguientes a los carácteres \\
        netUSr = re.findall('\\b\\\\\w+\w+\\b', netUS)
        #Retornamos los valores de NETUSL y NETUSR
        return netUSl,netUSr