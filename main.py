import os
import re
import argparse
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from fpdf import FPDF
from PIL import Image
import tempfile

# Set up argument parser
def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert PDF pages to images and arrange them in a grid PDF with optional cropping.")
    parser.add_argument('input', type=str, help='Path to the input PDF file.')
    parser.add_argument('--crop_top_offset', type=int, default=0, help='Offset to crop from the top of the image (default: 0).')
    parser.add_argument('--crop_left_offset', type=int, default=0, help='Offset to crop from the left of the image (default: 0).')
    parser.add_argument('--image_width', type=float, default=200, help='Width of the image in points (default: 200).')
    parser.add_argument('--image_height', type=float, default=200, help='Height of the image in points (default: 200).')
    parser.add_argument('--grid_row', type=int, default=3, help='Maximum number of rows per page (default: 3).')
    parser.add_argument('--grid_column', type=int, default=3, help='Maximum number of columns per page (default: 3).')
    parser.add_argument('--padding_top', type=float, default=20, help='Padding for the top margin in points (default: 20).')
    parser.add_argument('--padding_left', type=float, default=20, help='Padding for the left margin in points (default: 20).')
    parser.add_argument('--output', type=str, default=None, help='Output path for the generated PDF (default: input_filename_grid.pdf).')
    return parser.parse_args()

# Set output filename
def set_output_filename(input_path, output_filename):
    if output_filename is None:
        input_filename = os.path.splitext(os.path.basename(input_path))[0]
        return f"Result_{input_filename}.pdf"
    return output_filename

def clean_filename(text, max_length=50):
    """Clean and limit the text to be used in filenames."""
    text = re.sub(r'[^\w\s]', '', text)  # Remove non-alphanumeric characters
    text = re.sub(r'\s+', '_', text)  # Replace spaces with underscores
    return text[:max_length]  # Limit filename length

def crop_image(image, crop_top_offset, crop_left_offset):
    """Crop the image to a square based on specified offsets."""
    width, height = image.size
    size = min(width, height)

    left = crop_left_offset
    upper = crop_top_offset
    right = min(left + size, width)
    lower = min(upper + size, height)

    return image.crop((left, upper, right, lower))

def extract_text_from_pdf(input_path):
    """Extract text from each page of the PDF."""
    reader = PdfReader(input_path)
    page_texts = [page.extract_text() for page in reader.pages]
    return page_texts

def create_pdf(images, output_path):
    """Create a PDF file with images arranged in a grid."""
    pdf = FPDF(unit='pt', format='A3')
    pdf.add_page()

    x_offset = args.padding_left
    y_offset = args.padding_top
    current_row = 0
    current_col = 0  # Track the current column index

    for image, _ in images:  # We don't need the filename here, just the image
        with tempfile.NamedTemporaryFile(delete=True, suffix='.png') as temp_image_file:
            image.save(temp_image_file, format='PNG')
            temp_image_file.seek(0)

            # Check if we need to move to the next column
            if current_col >= args.grid_column:
                x_offset = args.padding_left
                y_offset += args.image_height
                current_row += 1
                current_col = 0  # Reset column counter

            # Check if we need to add a new page
            if current_row >= args.grid_row:
                pdf.add_page()
                current_row = 0
                y_offset = args.padding_top  # Reset y_offset for new page
                x_offset = args.padding_left  # Reset x_offset for new page

            # Add image to PDF
            pdf.image(temp_image_file.name, x=x_offset, y=y_offset, w=args.image_width, h=args.image_height)
            pdf.set_draw_color(0, 0, 0)
            pdf.set_line_width(2)
            pdf.rect(x_offset, y_offset, args.image_width, args.image_height)

            current_col += 1
            x_offset += args.image_width

    pdf.output(output_path)
    print(f"PDF saved as {output_path}")

def pdf_to_images(input_path, crop_top_offset, crop_left_offset):
    """Convert PDF pages to images and create a grid in a PDF."""
    images = convert_from_path(input_path)
    page_texts = extract_text_from_pdf(input_path)
    cropped_images = []

    for image, text in zip(images, page_texts):
        cropped_image = crop_image(image, crop_top_offset, crop_left_offset)
        sanitized_text = clean_filename(text.strip() or "page")  # Use sanitized text or fallback to "page"
        cropped_images.append((cropped_image, sanitized_text))

    # Sort cropped images by the sanitized filename
    cropped_images.sort(key=lambda x: x[1])  # Sort by the second item in the tuple (sanitized filename)

    return cropped_images

if __name__ == "__main__":
    args = parse_arguments()
    args.output = set_output_filename(args.input, args.output)
    cropped_images = pdf_to_images(args.input, args.crop_top_offset, args.crop_left_offset)
    create_pdf(cropped_images, args.output)
