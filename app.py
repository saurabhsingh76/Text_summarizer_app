import time
from flask import Flask, render_template, request,url_for

from summarizer1 import summarize

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    global raw_text
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


app.run(debug=True)
