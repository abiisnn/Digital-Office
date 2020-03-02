from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
 
def draw_paragraph(self, text, max_width, max_height, style):
        if not text:
            text = ''
        if not isinstance(text, str):
            text = str(text)
        text = text.strip(string.whitespace)
        text = text.replace('\n', "<br/>")
        p = Paragraph(text, style)
        used_width, used_height = p.wrap(max_width, max_height)
        line_widths = p.getActualLineWidths0()
        number_of_lines = len(line_widths)
        if number_of_lines > 1:
            actual_width = used_width
        elif number_of_lines == 1:
            actual_width = min(line_widths)
            used_width, used_height = p.wrap(actual_width + 0.1, max_height)
        else:
            return 0, 0
        p.drawOn(self.canvas, self.cursor.x, self.cursor.y - used_height)
        return used_width, used_height 

canvas = canvas.Canvas("idDocument.pdf", pagesize=letter)
canvas.setLineWidth(.3)
# canvas.setFont('Helvetica', 12)

# canvas.drawString(30,500,'Issue:')
# canvas.drawString(120,703,"Put Issue from bd")
  
# canvas.drawString(30,703,'Date:')
# canvas.line(120,700,580,700)
# canvas.drawString(120,703,"Put date")
 

canvas.save()