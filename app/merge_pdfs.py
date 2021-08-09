import os
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
import img2pdf

ROOT_DIR = "media/collage_and_yearbook/"

dirs = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f))]

for current_dir in dirs:
    department = current_dir
    current_dir = os.path.join(ROOT_DIR, current_dir)
    yearbook_pdf = os.path.join(current_dir, 'yearbook.pdf')
    collage_dir = os.path.join(current_dir, 'collages')
    collage_pdfs = os.listdir(collage_dir)
    # frontpage_pdf = os.path.join(ROOT_DIR, 'frontpage.pdf')
    
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297)) # specify page size (A4)
    layout_fun = img2pdf.get_layout_fun(a4inpt)

    # convert department pic 1 to pdf
    department_pic1_pdf = os.path.join(current_dir,'department_pic1.pdf')
    department_pic1 = os.path.join(current_dir,'department_pic1.jpg')
    if os.path.exists(department_pic1):
        with open(department_pic1_pdf, "wb") as f:
            f.write(img2pdf.convert(department_pic1, layout_fun=layout_fun))

    # convert department pic 2 to pdf
    department_pic2_pdf = os.path.join(current_dir,'department_pic2.pdf')
    department_pic2 = os.path.join(current_dir,'department_pic2.jpg')
    if os.path.exists(department_pic2):
        with open(department_pic2_pdf, "wb") as f:
            f.write(img2pdf.convert(department_pic2, layout_fun=layout_fun))

    merger = PdfFileMerger()
    # merger.append(frontpage_pdf)
    merger.append(yearbook_pdf)
    
    for collage in collage_pdfs:
        if collage.endswith('.pdf'):
            pdf = os.path.join(collage_dir, collage)
            merger.append(pdf)
    
    temp_yearbook = os.path.join(current_dir, 'temp_yearbook_' + department + '.pdf')
    merger.write(temp_yearbook)
    merger.close()

    # # delete the 'add offcial group photo' page
    # pages_to_delete = [1,3,4,5] # Change this according to the temp yearbook pdf generated
    # infile = PdfFileReader(temp_yearbook, 'rb')
    # output = PdfFileWriter()

    # for i in range(infile.getNumPages()):
    #     if i not in pages_to_delete:
    #         p = infile.getPage(i)
    #         output.addPage(p)

    # temp_yearbook2 = os.path.join(current_dir, 'temp_yearbook2_' + department + '.pdf')
    # with open(temp_yearbook2, 'wb') as f:
    #     output.write(f)

    # add department pics
    merger2 = PdfFileMerger()
    merger2.append(temp_yearbook)
    if os.path.exists(department_pic1_pdf):
    	merger2.merge(2, department_pic1_pdf)

    if os.path.exists(department_pic2_pdf):
    	merger2.merge(3, department_pic2_pdf)

    final_yearbook = os.path.join(current_dir, 'final_yearbook_' + department + '.pdf')
    merger2.write(final_yearbook)
    merger2.close()