import os
from PyPDF2 import PdfFileMerger

ROOT_DIR = "collage_and_yearbook/"

dirs = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f))]

for current_dir in dirs:
    department = current_dir
    current_dir = os.path.join(ROOT_DIR, current_dir)
    yearbook_pdf = os.path.join(current_dir, 'yearbook.pdf')
    collage_dir = os.path.join(current_dir, 'collages')
    collage_pdfs = os.listdir(collage_dir)
    merger = PdfFileMerger()
    merger.append(yearbook_pdf)

    for collage in collage_pdfs:
        if collage.endswith('.pdf'):
            pdf = os.path.join(collage_dir, collage)
            merger.append(pdf)
    
    merger.write(os.path.join(current_dir, 'final_yearbook_' + department + '.pdf'))
    merger.close()