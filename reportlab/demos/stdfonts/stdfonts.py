#copyright ReportLab Inc. 2000
#see license.txt for license details
#history http://cvs.sourceforge.net/cgi-bin/cvsweb.cgi/reportlab/demos/stdfonts/stdfonts.py?cvsroot=reportlab
#$Header: /tmp/reportlab/reportlab/demos/stdfonts/stdfonts.py,v 1.7 2000/10/25 08:57:45 rgbecker Exp $
__version__=''' $Id: stdfonts.py,v 1.7 2000/10/25 08:57:45 rgbecker Exp $ '''
__doc__="""
This generates tables showing the 14 standard fonts in both
WinAnsi and MacRoman encodings, and their character codes.
Supply an argument of 'hex' or 'oct' to get code charts
in those encodings; octal is what you need for \\n escape
sequences in Python literals.

usage: standardfonts.py [dec|hex|oct]
"""
import sys
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
import string

label_formats = {'dec':('%d=', 'Decimal'),
                 'oct':('%o=','Octal'),
                 'hex':('0x%x=', 'Hexadecimal')}

def run(mode):

    label_formatter, caption = label_formats[mode]
    
    for enc in ['MacRoman', 'WinAnsi']:
        canv = canvas.Canvas(
                'StandardFonts_%s.pdf' % enc,
                encoding=enc
                )
        canv.setPageCompression(0)
        
        for fontname in pdfmetrics.StandardEnglishFonts:
            if fontname in ['Symbol', 'ZapfDingbats']:
                encLabel = 'only available as MacRoman'
            else:
                encLabel = enc
            canv.setFont('Times-Bold', 18)
            canv.drawString(80, 744, fontname + '-' + encLabel)
            canv.setFont('Times-BoldItalic', 12)
            canv.drawRightString(515, 744, 'Labels in ' + caption)
            
            
            #for dingbats, we need to use another font for the numbers.
            #do two parallel text objects.
            if fontname == 'ZapfDingbats':
                labelfont = 'Helvetica'
            else:
                labelfont = fontname
            for byt in range(32, 256):
                col, row = divmod(byt - 32, 32)
                x = 72 + (66*col)
                y = 720 - (18*row)
                canv.setFont(labelfont, 14)
                canv.drawString(x, y, label_formatter % byt)
                canv.setFont(fontname, 14)
                canv.drawString(x + 44, y , chr(byt))
            canv.showPage()            
        canv.save()

if __name__ == '__main__':
    if len(sys.argv)==2:
        mode = string.lower(sys.argv[1])
        if mode not in ['dec','oct','hex']:
            print __doc__
            
    elif len(sys.argv) == 1:
        mode = 'dec'
        run(mode)
    else:
        print __doc__
    
