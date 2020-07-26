import os
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
import img2pdf

ROOT_DIR = "collage_and_yearbook/"

dirs = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f))]

for current_dir in dirs:
    department = current_dir
    current_dir = os.path.join(ROOT_DIR, current_dir)
    yearbook_pdf = os.path.join(current_dir, 'yearbook.pdf')
    collage_dir = os.path.join(current_dir, 'collages')
    collage_pdfs = os.listdir(collage_dir)
    
    # convert department pic to pdf
    department_pic_pdf = os.path.join(current_dir,'department_pic.pdf')
    if os.path.exists(department_pic_pdf):
        a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297)) # specify page size (A4)
        layout_fun = img2pdf.get_layout_fun(a4inpt)
        with open(department_pic_pdf, "wb") as f:
            f.write(img2pdf.convert(os.path.join(current_dir,'department_pic.jpg'), layout_fun=layout_fun))

    merger = PdfFileMerger()
    merger.append(yearbook_pdf)
    if os.path.exists(department_pic_pdf):
        merger.merge(2, department_pic_pdf) # add department_pic as 3rd page

    for collage in collage_pdfs:
        if collage.endswith('.pdf'):
            pdf = os.path.join(collage_dir, collage)
            merger.append(pdf)
    
    temp_yearbook = os.path.join(current_dir, 'temp_yearbook_' + department + '.pdf')
    merger.write(temp_yearbook)
    merger.close()

    # delete the 'add offcial group photo' page
    pages_to_delete = [3] # Change this according to the temp yearbook pdf generated
    infile = PdfFileReader(temp_yearbook, 'rb')
    output = PdfFileWriter()

    for i in range(infile.getNumPages()):
        if i not in pages_to_delete:
            p = infile.getPage(i)
            output.addPage(p)

    final_yearbook = os.path.join(current_dir, 'final_yearbook_' + department + '.pdf')
    with open(final_yearbook, 'wb') as f:
        output.write(f)