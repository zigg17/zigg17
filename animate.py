import svgwrite

def txt_to_svg(input_file, output_file):
    # Read text from file
    with open(input_file, 'r') as file:
        text = file.read()

    # Create an SVG drawing
    dwg = svgwrite.Drawing(output_file, profile='tiny')
    dwg.add(dwg.text(text, insert=(10, 20), font_size="16px", font_family="Arial"))

    # Save the drawing
    dwg.save()

txt_to_svg('asciicopy.txt', 'output.svg')
 

import cairosvg

def convert_svg_to_png(svg_file_path, output_file_path):
    cairosvg.svg2png(url=svg_file_path, write_to=output_file_path)

# Replace 'input.svg' with your SVG file path and 'output.png' with your desired output file name
convert_svg_to_png('output.svg', 'output.png')
