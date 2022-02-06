import subprocess
import re

class extractU():
    def __init__(self):
        super().__init__()
    
    def extraer(self):
        net = []
        netUS = subprocess.getoutput('net use')
        netUSl = re.findall('[A-Z]{1}[:]{1}', netUS)
        netUSr = re.findall('\\b\\\\\w+\w+\\b', netUS)

        return netUSl,netUSr