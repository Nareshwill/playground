from fpdf import FPDF
import os
# create a instance of fpdf
pdf = FPDF()
pdf.set_auto_page_break(0)

path = r'C:\Users\ahamm\Desktop\munseer'
img_list = [x for x in os.listdir(path)]

for img in img_list:
    image_path = os.path.join(path, img)
    if os.path.exists(image_path):
        pdf.add_page()
        pdf.image(image_path)

pdf.output(r"C:\Users\ahamm\Desktop\PROJECT\output\sample.pdf")