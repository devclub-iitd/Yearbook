import os, errno
import sys
import shutil
import collage_maker
import img2pdf

ROOT_DIR = "media/collage_and_yearbook"
BATCH_SIZE = 8

dirs = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f))]

for current_dir in dirs:
    current_dir = os.path.join(ROOT_DIR, current_dir)

    img_names = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    folder_count = 0    
    while (img_names != []):
        folder_path = os.path.join(current_dir, str(folder_count))
        try : 
            os.makedirs(folder_path)
            print ("Folder created", folder_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            folder_count += 1
            continue
        img_names = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
        for i in range(BATCH_SIZE):
            try : 
                oldfilepath = os.path.join(current_dir,img_names[i])
                newfilepath = os.path.join(folder_path,img_names[i])
            except Exception as e : 
                print (e)
                break
            shutil.move(oldfilepath,newfilepath)

        folder_count += 1
        img_names = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]



for current_dir in dirs:
    current_dir = os.path.join(ROOT_DIR, current_dir)
    dir_names = [f for f in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, f))]
    for folder in dir_names:
        folder_path = os.path.join(current_dir, folder)
        args = {'folder':folder_path, 'width':850 , 'init_height':720, 'shuffle' : True , 'output' : os.path.join(current_dir,'out_'+folder+'.jpg')}
        collage_maker.prepare(args)

        # convert to pdf
        a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297)) # specify page size (A4)
        layout_fun = img2pdf.get_layout_fun(a4inpt)
        with open(os.path.join(current_dir,'out_'+folder+'.pdf'), "wb") as f:
            f.write(img2pdf.convert(os.path.join(current_dir,'out_'+folder+'.jpg'), layout_fun=layout_fun))
