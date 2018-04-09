from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from django.contrib.auth.models import User 
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
from ordem.models import ordens
import time

class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    def print_users(self, ordem_id):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=1,
                                bottomMargin=72,
                                pagesize=self.pagesize)
 
        # Our container for 'Flowable' objects
        elements = []
        formatted_time = time.ctime()
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        ptext = '<font size=12>%s</font>' % formatted_time
 
        elements.append(Paragraph(ptext, styles["Normal"]))
        elements.append(Spacer(1, 12))
        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        ordem_obj = ordens.objects.filter(id=ordem_id).get()
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        users = User.objects.all()
        im = Image("imagem.png", 0, 0)
        data = ordem_obj.data_abertura.strftime('%d/%m/%Y')
        elements.append(im)
        elements.append(Paragraph('<b>Ordem de Serviço</b>     N°: '+str(ordem_obj.id)+'            Data: '+str(data)+'', styles['Heading2']))
        elements.append(Paragraph('Nome: '+str(ordem_obj.cliente_ordem)+'   Telefone: '+str(ordem_obj.cliente_ordem.telefone)+'   Celular: '+str(ordem_obj.cliente_ordem.celular)+'', styles['Heading4']))
        elements.append(Paragraph('E-mail: '+str(ordem_obj.cliente_ordem.email)+'', styles['Heading4']))
        elements.append(Paragraph('Serviços:', styles['Heading2']))
        

        doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer,
                  canvasmaker=NumberedCanvas)
 
        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    

    @staticmethod
    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        elements = []

        # Header
 
        # Footer
        footer = Paragraph('Rodão Borracharia agradece a preferência e confiança.   ', styles['Heading2'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
 
        # Release the canvas
        canvas.restoreState()

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
 
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
 
    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(211 * mm, 3 * mm + (0.2 * inch),
                             "Page %d of %d" % (self._pageNumber, page_count))