from PIL import Image
from flask import Flask, render_template

def img_to_ascii(img_path, output_width=100):
    ASCII_CHARS = "@%#*+=-:."
    img = Image.open(img_path)
    width, height = img.size
    aspect_ratio = height / width
    ascii_char_aspect_ratio = 0.5  # this is an approximation
    output_height = int(output_width * aspect_ratio * ascii_char_aspect_ratio)

    
    img = img.resize((output_width, output_height))
    img = img.convert('L')  # Convert to grayscale

    pixels = img.getdata()
    ascii_str = ''

    for pixel in pixels:
        ascii_str += ASCII_CHARS[(pixel * (len(ASCII_CHARS) - 1)) // 255]

    ascii_str_len = len(ascii_str)
    ascii_img = ""

    for i in range(0, ascii_str_len, output_width):
        ascii_img += ascii_str[i:i+output_width] + "\n"

    return ascii_img

app = Flask(__name__)

@app.route('/work')
def work():
    # Convert all 6 images to ASCII
    asciis = [img_to_ascii(f"static/assets/{i}.jpg", output_width=50) for i in range(1, 7)]

    # Pass the ASCII arts to the template
    return render_template('work.html', **{"ascii_"+str(i+1): asciis[i] for i in range(6)})

if __name__ == '__main__':
    app.run(debug=True)
