from flask import Flask, render_template, request
import csv
import string
import nltk
from nltk.corpus import stopwords
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import os
import glob
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import time


app = Flask(__name__)
app.secret_key = 'secret_key'
nltk.download('stopwords')
stop_words = stopwords.words('indonesian')


def clean_text(text):

    # Menghapus kata-kata yang diawali dengan "@" kecuali jika mengandung @aniesbaswedan, @ganjarpranowo, atau @prabowo
    text = re.sub(r"(?<!@aniesbaswedan)(?<!@ganjarpranowo)(?<!@prabowo)@\S+", "", text)

    # Menghapus tanda baca
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Case folding
    text = text.lower()
    # Menghapus kata-kata yang diawali dengan "http" atau "https"
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"https\S+", "", text)
    # Stopword removal bahasa Indonesia
    stopwords_ind = stopwords.words('indonesian')
    words = text.split()
    if words:
        words = [word for word in words if word not in stopwords_ind]
        # Slang word normalization bahasa Indonesia
        with open('slang_words.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            slang_dict = dict(reader)
        words = [slang_dict[word] if word in slang_dict else word for word in words]
       # Stemming bahasa Indonesia
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    words = [stemmer.stem(word) for word in words]
    # Menggabungkan kata kembali
    text = " ".join(words)
    return text


@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    # ambil file CSV dari form dan simpan di direktori uploads
    file = request.files['file']
    if not file:
        return "Tidak ada file yang diupload"
    file.save('uploads/' + file.filename)

    # buka file CSV yang diunggah dan baca isinya
    with open('uploads/' + file.filename,encoding="ISO-8859-1",  newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\n', quotechar='"')
        data_before = []
        data_after = []
        count = 1
        for row in reader:
           # preprocessing data
            cleaned_row = []
            for col in row:
                cleaned_col = clean_text(col)
                cleaned_row.append(cleaned_col)
            # simpan data sebelum dan setelah preprocessing
            row_with_count = [count] + row
            data_before.append(row_with_count)
            row_with_count = [count] + cleaned_row
            data_after.append(row_with_count)
            count += 1

    
    # simpan file hasil preprocessing ke direktori "preprocessing"
    with open('preprocessing/' + file.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(data_after)

    # kirim data ke template HTML untuk ditampilkan
    return render_template('result.html', data_before=data_before,data_after=data_after, count=count,len=len)


@app.route('/label',methods=['POST'])

def label():
       # cari file csv terbaru di direktori preprocessing
    list_of_files = glob.glob('preprocessing/*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)

    #baca kamus
    lexicon_file = 'label.csv'

    # Mendapatkan path direktori dari file Python yang dieksekusi
    current_dir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(current_dir, lexicon_file), 'r', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        lexicon = list(reader)
    
     # Mengubah kamus pelabelan menjadi dictionary
    lexicon_dict = {}
    for row in lexicon:
        lexicon_dict[row[0]] = float(row[1])

    # baca file csv dan lakukan labeling
    with open(latest_file, encoding="ISO-8859-1", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        data = list(reader)

    # Melakukan pelabelan sentimen
    results = []
    for row in data:
        score = 0
        for word in clean_text(row[0]).split():
            if word in lexicon_dict:
                score += lexicon_dict[word]
        if score < 0:
            sentiment = 'negatif'
        elif score >= 0:
            sentiment = 'positif'
        
        row[0] = re.sub(r'^\d+\s*', '', row[0])
        results.append((row[0], sentiment,score))

    os.makedirs("labeled", exist_ok=True)
    os.makedirs("anies", exist_ok=True)
    with open('labeled/labeled_data.csv', 'w', newline='') as f:
             writer = csv.writer(f, delimiter=';')
             writer.writerows([[result[0], result[1]] for result in results])

    with open('label.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        data_csv = [row for row in reader]
    
    # simpan data yang mengandung kata "anies"
    with open('anies/anies_labeled_data.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows([result for result in results if 'anies' in result[0].lower()])

    # simpan data yang mengandung kata "ganjar"
    with open('ganjar/ganjar_labeled_data.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows([result for result in results if 'ganjar' in result[0].lower()])

    # simpan data yang mengandung kata "prabowo"
    with open('prabowo/prabowo_labeled_data.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows([result for result in results if 'prabowo' in result[0].lower()])
    
    
    return render_template('label.html', results=results,len=len,data=data,data_csv=data_csv)

# Ini program TF-IDF belum saatnya dieksekusi
@app.route('/figure',methods=['POST'])
def figure ():
    time.sleep(5)

    # Cari file CSV terbaru di direktori anies
    list_of_files = glob.glob('anies/*.csv')
    latest_anies_file = max(list_of_files, key=os.path.getctime)

    # Baca file CSV dan simpan data dalam list
    with open(latest_anies_file, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        anies_data = list(reader)

    # Cari file CSV terbaru di direktori ganjar
    list_of_files = glob.glob('ganjar/*.csv')
    latest_ganjar_file = max(list_of_files, key=os.path.getctime)

    # Baca file CSV dan simpan data dalam list
    with open(latest_ganjar_file, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        ganjar_data = list(reader)

    # Cari file CSV terbaru di direktori prabowo
    list_of_files = glob.glob('prabowo/*.csv')
    latest_prabowo_file = max(list_of_files, key=os.path.getctime)

    # Baca file CSV dan simpan data dalam list
    with open(latest_prabowo_file, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        prabowo_data = list(reader)

    return render_template('figure.html',anies_data=anies_data,ganjar_data=ganjar_data,prabowo_data=prabowo_data)

if __name__ == '__main__':
    app.run(debug=True)
