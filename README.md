# Analisis Sentimen Calon Presiden Indonesia 2024 di Twitter

Proyek ini bertujuan untuk menganalisis sentimen terkait tiga calon presiden Indonesia yang potensial pada pemilihan presiden tahun 2024: Prabowo Subianto, Ganjar Pranowo, dan Anies Baswedan. Analisis sentimen dilakukan terhadap tweet yang dikumpulkan dari Twitter selama bulan Oktober 2022.

## Alur Program

### 1. Perencanaan (Planning)

- **Tujuan Utama Proyek**: Menganalisis sentimen terkait tiga calon presiden potensial.
- **Pengumpulan Data**: Menggunakan Twitter API untuk mengumpulkan tweet dari bulan Oktober 2022 yang mencakup ketiga calon presiden.
- **Calon Presiden yang Dianalisis**: Prabowo Subianto, Ganjar Pranowo, Anies Baswedan.
- **Periode Waktu**: Oktober 2022.
- **Metode Analisis Sentimen**: Menggunakan TF-IDF dan naive Bayes.

### 2. Pengumpulan Data (Data Collection)

- Menggunakan Twitter API untuk mengumpulkan tweet yang sesuai dengan periode dan calon presiden yang ditentukan.
- Data tweet disimpan dalam format yang sesuai untuk analisis selanjutnya.

### 3. Preprocessing Data

- Data tweet dibersihkan dari elemen tidak penting seperti tautan, karakter khusus, dan bahasa gaul.
- Normalisasi teks digunakan untuk mengatasi perbedaan ejaan dan format.
- Data duplikat dihapus jika ditemukan.

### 4. Labeling Sentimen (Sentiment Labeling)

- Kamus leksikon bahasa Indonesia digunakan untuk memberikan label sentimen (positif, negatif, netral) pada setiap tweet.
- Parameter ditentukan untuk menentukan sentimen berdasarkan nilai TF-IDF dan naive Bayes.

### 5. Analisis Sentimen (Sentiment Analysis)

- Skor sentimen dihitung untuk setiap calon presiden berdasarkan tweet yang terkait.
- Hasil analisis sentimen divisualisasikan dalam bentuk grafik atau diagram untuk mempresentasikan temuan.

## Penggunaan

1. Instal semua dependensi yang diperlukan dengan menjalankan perintah berikut:

```bash
pip install -r requirements.txt
