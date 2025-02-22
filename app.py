from flask import Flask, render_template, request, send_file
from PIL import Image
from io import BytesIO
import exif

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        
        file = request.files['file']
        if file.filename == '':
            return "No file selected", 400
        
        # Open the image and remove metadata
        img = Image.open(file.stream)
        data = list(img.getdata())
        img_without_exif = Image.new(img.mode, img.size)
        img_without_exif.putdata(data)
        
        # Save the cleaned image to a BytesIO object
        cleaned_image = BytesIO()
        img_without_exif.save(cleaned_image, format=img.format)
        cleaned_image.seek(0)
        
        return send_file(cleaned_image, download_name=f"cleaned_{file.filename}", as_attachment=True)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
