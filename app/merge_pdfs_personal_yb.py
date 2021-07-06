import os
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
import img2pdf

ROOT_DIR = "collage_and_yearbook_personal/"
FRONT_PAGE = "myapp/static/myapp/pdf/Yearbook21GTA.pdf"

dirs = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f))]

for current_dir in dirs:
    student_name = current_dir
    current_dir = os.path.join(ROOT_DIR, current_dir)
    yearbook_pdf = os.path.join(current_dir, 'yearbook.pdf')
    collage_dir = os.path.join(current_dir, 'collages')
    collage_pdfs = os.listdir(collage_dir)
    # frontpage_pdf = os.path.join(ROOT_DIR, 'frontpage.pdf')
    
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297)) # specify page size (A4)
    layout_fun = img2pdf.get_layout_fun(a4inpt)

    merger = PdfFileMerger()
    merger.append(FRONT_PAGE)
    merger.append(yearbook_pdf)
    
    for collage in collage_pdfs:
        if collage.endswith('.pdf'):
            pdf = os.path.join(collage_dir, collage)
            merger.append(pdf)
    
    merger.write(os.path.join(current_dir, 'final_yearbook_' + student_name + '.pdf'))
    merger.close()