## Post processing

1. Run `./post_processing` to generate wordclouds and collages. A directory named `collage_and_yearbook` is created and the collages are placed inside it in both .jpg and .pdf formats.  
Directory structure of `collage_and_yearbook`:
```
.
├── chemical
│   ├── 0
│   ├── 1
|   ...
│   └── collages
│       ├── out_0.jpg
│       ├── out_0.pdf
│       ├── out_1.jpg
│       └── out_1.pdf
|   ...
...
├── physics
│   ├── 0
|   ...
│   └── collages
│       ├── out_0.jpg
│       └── out_0.pdf
```  
2. Download the yearbook PDFs from the web portal and place them inside the corresponding department folder in `collage_and_yearbook` with the name `yearbook.pdf`. Also place the corresponding department picture with the name `department_pic.jpg`.  
Also add the front page as `frontpage.pdf` in `collage_and_yearbook` folder.
Now the directory structure of `collage_and_yearbook` is:
```
├── frontpage.pdf
.
├── chemical
│   ├── 0
│   ├── 1
|   ...
│   ├── collages
│   │   ├── out_0.jpg
│   │   ├── out_0.pdf
│   │   ├── out_1.jpg
│   │   └── out_1.pdf
│   ├── yearbook.pdf
│   └── department_pic.jpg
|   ...
...
├── physics
│   ├── 0
|   ...
│   ├── collages
│   │   ├── out_0.jpg
│   │   └── out_0.pdf
│   ├── yearbook.pdf
│   └── department_pic.jpg

```  
3. Run `python merge_pdfs.py` to convert `department_pic.jpg` to pdf format and then merge the yearbook, department_pic and the collages. This generates the `final_yearbook_<department>.pdf` inside the department folder. Note that this also removes the 'add group photo page' from the final pdf.