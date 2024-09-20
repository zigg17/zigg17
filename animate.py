import markdown
import imgkit

# Your markdown text

with open('asciicopy.txt', 'r') as file:
    file_content = file.read()

markdown_text = file_content

# Convert Markdown to HTML
html_text = markdown.markdown(markdown_text)

# Convert HTML to Image
imgkit.from_string(html_text, 'output.png')