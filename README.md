# GridSnap PDF Maker

**GridSnap PDF Maker** is a Python tool designed to convert PDF pages into images and arrange them into a grid layout in a new PDF file. It is highly customizable with options for cropping, padding, and grid configuration, making it perfect for creating clean, well-structured PDFs.

## Features

- **PDF Page to Image Conversion**: Converts PDF pages into images for easy manipulation.
- **Image Cropping**: Automatically crops images into squares based on user-defined offsets.
- **Grid Layout**: Arranges images into a customizable grid (rows and columns) in the output PDF.
- **Padding Control**: Allows control over padding between images and around the page edges.
- **Custom Output**: Set the output PDF filename or use an automatic naming convention based on the input PDF file name.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nggrjh/grid-pdf-images.git
   ```

2. Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the tool, run the following command:

```bash
python main.py input.pdf \
    [--crop_top_offset CROP_TOP_OFFSET] \
    [--crop_left_offset CROP_LEFT_OFFSET] \
    [--image_width IMAGE_WIDTH] \
    [--image_height IMAGE_HEIGHT] \
    [--grid_column GRID_COLUMN] \
    [--grid_row GRID_ROW] \
    [--padding_top PADDING_TOP] \
    [--padding_left PADDING_LEFT] \
    [--output OUTPUT]
```

### Arguments

| Argument              | Description                                                   |
| --------------------- | ------------------------------------------------------------- |
| `input`               | Path to the input PDF file. This is a mandatory argument.     |
| `--crop_top_offset`   | Crop offset from the top of the image. Default is 0.          |
| `--crop_left_offset`  | Crop offset from the left of the image. Default is 0.         |
| `--image_width`       | The width of the images in points. Default is 200.            |
| `--image_height`      | The height of the images in points. Default is 200.           |
| `--grid_column`       | Maximum number of columns per page in the PDF. Default is 3.  |
| `--grid_row`          | Maximum number of rows per page in the PDF. Default is 3.     |
| `--padding_top`       | Top margin padding in points. Default is 20.                  |
| `--padding_left`      | Left margin padding in points. Default is 20.                 |
| `--output`            | Full file path for the output PDF.                            |

### Example

To create a PDF with default settings, run:

```bash
python main.py document.pdf
```

This will generate a grid of images from `document.pdf` and save the result as a new PDF file

## License

© 2024 Linggar Juwita. All rights reserved.
