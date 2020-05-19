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
2. Download the yearbook PDFs from the web portal and place them inside the corresponding department folder in `collage_and_yearbook` with the name `yearbook.pdf`.  
Now the directory structure of `collage_and_yearbook` is:
```
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
│   └── yearbook.pdf
|   ...
...
├── physics
│   ├── 0
|   ...
│   ├── collages
│   │   ├── out_0.jpg
│   │   └── out_0.pdf
│   └── yearbook.pdf

```  
3. Run `python merge_pdfs.py` to merge the yearbook and the collages. This generates the `final_yearbook_<department>.pdf` inside the department folders.