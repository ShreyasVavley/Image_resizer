from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import zipfile
import io

app = Flask(__name__, template_folder='pages')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('images')
        width = int(request.form['width'])
        quality = int(request.form['quality'])
        grayscale = 'grayscale' in request.form
        format_ext = request.form.get('format', 'JPEG')
        watermark_text = request.form.get('watermark', '')

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for file in files:
                img = Image.open(file).convert("RGB")
                
                # Resize
                img = img.resize((width, int(width * img.height / img.width)))
                
                # Pro Feature: Grayscale
                if grayscale:
                    img = img.convert('L')
                
                # Pro Feature: Watermark
                if watermark_text:
                    draw = ImageDraw.Draw(img)
                    draw.text((10, 10), watermark_text, fill="white")

                # Save to Buffer
                img_io = io.BytesIO()
                img.save(img_io, format=format_ext, optimize=True, quality=quality)
                img_io.seek(0)
                
                zip_file.writestr(f"pro_{file.filename.split('.')[0]}.{format_ext.lower()}", img_io.getvalue())

        zip_buffer.seek(0)
        return send_file(zip_buffer, as_attachment=True, download_name="pro_images.zip")
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)