from weasyprint import HTML

# Function to generate PDF from HTML template file
def generate_pdf_from_template(template_path, output_pdf):
    try:
        # Read HTML content from template file
        with open(template_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Generate PDF from HTML content
        HTML(string=html_content).write_pdf(output_pdf)
        print(f"PDF generated successfully: {output_pdf}")
    except Exception as e:
        print(f"Error generating PDF: {e}")

# Paths
template_path = 'headerrepeat.html'  # Path to your HTML template file
output_pdf = 'output.pdf'  # Output PDF file path

# Call function to generate PDF
generate_pdf_from_template(template_path, output_pdf)
