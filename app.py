import os
import time
import cv2
import pytesseract
from flask import Flask, render_template, request, url_for
from PIL import Image

from summarizer1 import summarize

UPLOAD_FOLDER = '/static/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


@app.route('/ocr', methods=['POST', 'GET'])
def upload_file():
    start = time.time()
    if request.method == "POST":
        file = request.files['file']

        f = os.path.join(app.config['UPLOAD_FOLDER'],'ocr_image.jpg')

        # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
        file.save(f)
        # print(file.filename)

        image = cv2.imread(UPLOAD_FOLDER + "/ocr_image.jpg")
        os.remove(UPLOAD_FOLDER + "ocr_image.jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        rawtext = pytesseract.image_to_string(Image.open('ocr_image.jpg'))

        final_summary = summarize(rawtext)
        final_summary_gensim = summarize(rawtext)
        # NLTK
        final_summary_nltk = summarize(rawtext)
        # Sumy
        final_summary_sumy = summarize(rawtext)
        end = time.time()
        final_time = end - start
        return render_template('index.html', ctext=rawtext, final_summary=final_summary,
                               final_summary_spacy=final_summary,
                               final_summary_gensim=final_summary_gensim, final_summary_nltk=final_summary_nltk,
                               final_summary_sumy=final_summary_sumy)

        # os.remove('ocr_image.jpg')


app.run(debug=True)
