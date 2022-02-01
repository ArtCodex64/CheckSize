import subprocess
import re

class extractU():
    def __init__(self):
        super().__init__()
    
    def extraer(self):
        netUS = subprocess.getoutput('net use')
        sp = re.search('CENTCS01SRV05(.+D?)Micro', netUS).group(1)
        return sp