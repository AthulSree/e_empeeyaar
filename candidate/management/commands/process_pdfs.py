import os
import fitz  # PyMuPDF #type: ignore
from django.core.management.base import BaseCommand #type: ignore

class Command(BaseCommand):
    help = 'Process and rename PDF files based on names found inside them'
    def add_arguments(self, parser):
        print(">>>>>>>>")
        parser.add_argument('pdf_folder', type=str, help='Path to the folder containing PDF files')

    def handle(self, *args, **options):
        print("<<<<<<")
        pdf_folder = options['pdf_folder']
        target_names = ['ATHUL', 'SREERAJ','NISANTH','SIMI','ANUJITH','VIMAL']

        for filename in os.listdir(pdf_folder):
            if filename.endswith('.pdf'):
                print("?????????")
                file_path = os.path.join(pdf_folder, filename)
                doc = fitz.open(file_path)
                text = ''
                for page in doc:
                    text += page.get_text()

                new_name = self.find_name_in_text(text, target_names)
                doc.close()
                if new_name:
                    new_filename = f"{new_name}.pdf"
                    os.rename(file_path, os.path.join(pdf_folder, new_filename))
                    self.stdout.write(self.style.SUCCESS(f'Renamed {filename} to {new_filename}'))

    def find_name_in_text(self, text, names):
        for name in names:
            if name in text:
                if 'Monthly Performance Report' in text:
                    return f"{name}_mpr"
                elif 'Leave Adjustment Certificate' in text:
                    return f"{name}_LAC"
        return None


# (py_env) D:\PythonProject\py_env\e-empeeyaar>python manage.py process_pdfs D:\pdfs