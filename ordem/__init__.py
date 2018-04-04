from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
 
class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize
 

