import os
import time
# import cv2
import pytesseract
from flask import Flask, render_template, request, url_for
from PIL import Image
# from werkzeug.utils import secure_filename

from summarizer1 import summarize

app = Flask(__name__)


# UPLOAD_FOLDER = '/static/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    global rawtext
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_summary = summarize(rawtext)
        final_summary_gensim = summarize(rawtext)
        # NLTK
        final_summary_nltk = summarize(rawtext)
        # Sumy
        final_summary_sumy = summarize(rawtext)
        end = time.time()
        final_time = end - start
    return render_template('index.html', ctext=rawtext, final_summary=final_summary, final_summary_spacy=final_summary,
                           final_summary_gensim=final_summary_gensim, final_summary_nltk=final_summary_nltk,
                           final_summary_sumy=final_summary_sumy)


def ocr_core(filename):
    # """
    # This function will handle the core OCR processing of images.
    # """
    # print("hoooooooooo rhaaaaa hai")
    # print(filename)
    pytesseract.pytesseract.tesseract_cmd = r'OCRLIB\\tesseract.exe'
    text = pytesseract.image_to_string(Image.open(filename))
    # print("hooooo gyaaaaaaaaaaaaaaaaaaa")
    return text


@app.route('/ocr', methods=['POST', 'GET'])
def upload_file():
    start = time.time()
    if request.method == "POST":
        file = request.files['file']
        # filename = secure_filename(file.filename)
        # f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        #
        # # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
        # file.save(f)
        # # print(file.filename)
        #
        # image = cv2.imread(UPLOAD_FOLDER + "/"+file.filename)
        # # os.remove(UPLOAD_FOLDER + "ocr_image.jpg")
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # f = os.path.join(app.config['UPLOAD_FOLDER'],'ocr_image.jpg')
        # file.save(secure_filename('ocr_image.jpg'))

        rawtext = ocr_core(file)

        final_summary = summarize(rawtext)

        final_summary_gensim = 'Coming Soon'
        # NLTK
        final_summary_nltk = 'Coming Soon'
        # Sumy
        final_summary_sumy = 'Coming Soon'
        end = time.time()
        final_time = end - start
        return render_template('index.html', ctext=rawtext, final_summary=final_summary,
                               final_summary_spacy=final_summary,
                               final_summary_gensim=final_summary_gensim, final_summary_nltk=final_summary_nltk,
                               final_summary_sumy=final_summary_sumy)

        # os.remove('ocr_image.jpg')


if __name__ == "__main__":
    app.run(debug=True)
