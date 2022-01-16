import sys
import os
sys.path.insert(0, 'app/YearbookRevampLibrary')
from YearbookRevampLibrary.AutoAlignerModule import auto_align


ROOT_DIR = "media"
dirs = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f))]

for current_dir in dirs:
    current_dir = os.path.join(ROOT_DIR, current_dir)
    auto_align(input_path=current_dir, output_path = current_dir)