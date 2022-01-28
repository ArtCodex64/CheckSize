from threading import Thread
import os
from pathlib import Path

class HiloGetSizeDirs(Thread):
    def __init__(self, directorio):
        Thread.__init__(self)
        self.directorio = directorio
        self.total = 0
    def getSizeDir(self, directorio):
        total = 0        
        try:
            for entry in os.scandir(self.directorio):
                if os.path.isfile(entry):
                    total += entry.stat().st_size
                elif os.path.isdir(entry):
                    total += self.getSizeDir(entry.path)
        except NotADirectoryError:
            return  os.path.getsize(directorio)
        except PermissionError:
            return 0
        return total

    def run(self):
        self.total = self.getSizeDir(self.directorio)
        
        

class HiloGetSizeFile(Thread):
    def __init__(self, file):
        Thread.__init__(self)
        self.file = file
        self.total = 0

    def run(self):
        self.total = Path(r"%s" % file).stat().st_size