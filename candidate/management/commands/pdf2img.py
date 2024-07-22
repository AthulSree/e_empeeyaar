import os
from django.core.management.base import BaseCommand
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from fuzzywuzzy import fuzz

class Command(BaseCommand):
    help = 'Process and rename PDFs containing specific keywords in a directory'

    def handle(self, *args, **kwargs):
        directory = '/home/athul/Pictures/AEO_LOGIC/Scanned_pdfs'
        target_names = ['ATHUL', 'SREERAJ','NISANTH','SIMI','ANUJITH','VIMAL']

        for filename in os.listdir(directory):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(directory, filename)
                output_dir = os.path.dirname(pdf_path)
                doc = fitz.open(pdf_path)

                text_found = False
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)                                                                          # calculating the no. of pages
                    pix = page.get_pixmap()                                                                                 # finding the pixmap of the page
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text = pytesseract.image_to_string(img)                                                                 # extract text from the page

                    for det_name in target_names:
                        if (self.fuzzy_match(det_name, text) and self.fuzzy_match('Monthly Performance Report', text)):
                            new_name = os.path.join(output_dir, det_name+'_MPR.pdf')
                            os.rename(pdf_path, new_name)
                        elif (self.fuzzy_match(det_name, text) and self.fuzzy_match('Leave Adjustment Certificate', text)):
                            new_name = os.path.join(output_dir, det_name+'_LAC.pdf')
                            os.rename(pdf_path, new_name)
                            

        self.stdout.write("PDF processing completed.")


    def fuzzy_match(self, keyword, text, threshold=60):        # matching the texts with the keyword for approximate match. Increasing the threshold value increases the accuracy of matching . here only 60 is applied bcoz the text detected may not be accurate 
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if fuzz.partial_ratio(keyword, line) > threshold:
                return True
        return False


#  python3 manage.py pdf2img


# def process_pdfs(request):
#     s_mprformonth = request.session['mprformonth']
#     if request.method == 'POST':
#         pdf_folder = 'D:\pdfs'
#         target_names = ['ATHUL', 'SREERAJ','NISANTH','SIMI','ANUJITH','VIMAL']
#         # renamed_files = []

#         try:
#             for filename in os.listdir(pdf_folder):
#                 if filename.endswith('.pdf'):
#                     file_path = os.path.join(pdf_folder, filename)
#                     doc = fitz.open(file_path)
#                     text = ''
#                     for page in doc:
#                         text += page.get_text()

#                     new_name = find_name_in_text(text, target_names,s_mprformonth)
#                     doc.close()
#                     if new_name:
#                         new_filename = f"{new_name}.pdf"
#                         os.rename(file_path, os.path.join(pdf_folder, new_filename))
#                         # renamed_files.append(new_filename)
            
#             return JsonResponse({'status': 200})
#         except Exception as e:
#             return HttpResponse({'status': 300,'msg':str(e)})

#     return HttpResponse({'status': 300,'msg':str(e)})

# def find_name_in_text( text, names, s_mprformonth):
#     for name in names:
#         if name in text:
#             if 'Monthly Performance Report' in text:
#                 return f"{name}_MPR_"+s_mprformonth
#             elif 'Leave Adjustment Certificate' in text:
#                 return f"{name}_LAC_"+s_mprformonth
#     return None
