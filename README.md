# 📊 Dashboard Analisis Sentimen

Dashboard interaktif berbasis web untuk analisis sentimen menggunakan IndoBERT, Naive Bayes, SVM, dan Random Forest. Dashboard ini dibuat dari kode notebook Google Colab untuk preprocessing dan analisis sentimen data dari Twitter dan TikTok.

## ✨ Fitur Utama

- 📈 **Visualisasi Interaktif**: Pie chart, bar chart, dan timeline sentimen menggunakan Plotly
- 🤖 **Multiple ML Models**: Perbandingan akurasi Naive Bayes, SVM, dan Random Forest
- 📊 **Statistik Real-time**: Card statistics untuk total data dan distribusi sentimen
- 🔍 **Data Table**: Preview data dengan filtering berdasarkan sentimen
- 📱 **Responsive Design**: UI modern dengan Tailwind CSS
- 📂 **Upload CSV**: Upload file dataset langsung dari browser

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, Tailwind CSS, Plotly.js, Axios
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, Sastrawi, NLTK
- **Visualisasi**: Plotly

## 📁 Struktur Project

```
sentiment-analysis-dashboard/
│
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── README.md              # Dokumentasi
│
├── templates/
│   └── index.html         # Dashboard HTML template
│
├── data/                  # Folder untuk dataset (optional)
│   └── dataset_labeled_final.csv
│
└── uploads/               # Folder untuk upload file
```

## 🚀 Instalasi

### Prerequisites

- Python 3.8 atau lebih baru
- pip (Python package manager)

### Langkah Instalasi

1. **Clone repository**
   ```bash
   git clone https://github.com/galihmawardi-maker/sentiment-analysis-dashboard.git
   cd sentiment-analysis-dashboard
   ```

2. **Buat virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data (sekali saja)**
   ```python
   python -c "import nltk; nltk.download('stopwords')"
   ```

5. **(Optional) Siapkan data**
   
   Jika Anda memiliki file `dataset_labeled_final.csv` dari hasil notebook, letakkan di folder `data/`:
   ```bash
   mkdir data
   # Copy file dataset_labeled_final.csv ke folder data/
   ```

## 💻 Cara Menjalankan

1. **Jalankan Flask server**
   ```bash
   python app.py
   ```

2. **Buka browser**
   
   Akses dashboard di: `http://localhost:5000` atau `http://0.0.0.0:5000`

3. **Upload Data CSV**
   
   Klik tombol "Upload Data CSV" dan pilih file CSV yang sudah diproses dengan kolom:
   - `post_id`
   - `user_handle`
   - `platform`
   - `search_query`
   - `timestamp`
   - `likes`
   - `retweets`
   - `replies`
   - `text_raw`
   - `text_clean`
   - `sentiment_label`

## 📊 Format Data CSV

File CSV harus memiliki kolom-kolom berikut:

| Kolom | Deskripsi |
|-------|----------|
| `post_id` | ID unik posting |
| `user_handle` | Username/handle user |
| `text_clean` | Teks yang sudah dibersihkan |
| `sentiment_label` | Label sentimen (positive/neutral/negative) |
| `platform` | Platform sumber data (twitter/tiktok) |
| `timestamp` | Waktu posting |
| `likes` | Jumlah likes |
| `retweets` | Jumlah retweets/shares |
| `replies` | Jumlah replies/comments |

## 🔌 API Endpoints

| Endpoint | Method | Deskripsi |
|----------|--------|----------|
| `/` | GET | Halaman utama dashboard |
| `/api/stats` | GET | Statistik data sentimen |
| `/api/sentiment-chart` | GET | Data untuk pie chart sentimen |
| `/api/platform-chart` | GET | Data untuk bar chart per platform |
| `/api/timeline-chart` | GET | Data untuk timeline chart |
| `/api/model-comparison` | GET | Data perbandingan model ML |
| `/api/data-table` | GET | Data untuk tabel dengan pagination |
| `/api/upload` | POST | Upload file CSV |
| `/api/wordcloud-data` | GET | Data untuk word cloud |

## 🎨 Screenshot

Dashboard menampilkan:
- **Stats Cards**: Total data, jumlah positive, neutral, dan negative
- **Pie Chart**: Distribusi sentimen
- **Bar Chart**: Sentimen per platform (Twitter/TikTok)
- **Timeline**: Tren sentimen dari waktu ke waktu
- **Model Comparison**: Akurasi Naive Bayes vs SVM vs Random Forest
- **Data Table**: Preview data dengan filter sentimen

## 📝 Catatan Penggunaan

1. **Upload Data**: Pastikan file CSV Anda sesuai format yang ditentukan
2. **Performance**: Untuk dataset besar (>10K rows), loading mungkin membutuhkan waktu
3. **Memory**: Dashboard memuat seluruh dataset ke memory, sesuaikan ukuran data dengan RAM server

## 🔧 Development

### Modifikasi Model Akurasi

Edit nilai akurasi model di `app.py`:

```python
@app.route('/api/model-comparison')
def model_comparison():
    models_data = {
        'models': ['Naive Bayes', 'SVM', 'Random Forest'],
        'accuracy': [0.6416, 0.6977, 0.6501],  # Ganti dengan hasil aktual
        # ...
    }
```

### Menambah Fitur Baru

1. Tambahkan route baru di `app.py`
2. Tambahkan fungsi JavaScript di `templates/index.html`
3. Tambahkan elemen HTML untuk visualisasi

## 🐛 Troubleshooting

### Error: "Data belum di-upload"
- **Solusi**: Upload file CSV melalui tombol "Upload Data CSV"

### Error: Module tidak ditemukan
- **Solusi**: Pastikan semua dependencies terinstall: `pip install -r requirements.txt`

### Port sudah digunakan
- **Solusi**: Ganti port di `app.py`: `app.run(port=5001)`

### Data tidak muncul
- **Solusi**: Periksa console browser (F12) untuk error JavaScript
- Periksa terminal untuk error Flask

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:
1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 License

Project ini dibuat untuk keperluan akademis dan pembelajaran.

## 👤 Author

**Galih Mawardi**
- GitHub: [@galihmawardi-maker](https://github.com/galihmawardi-maker)

## 🙏 Acknowledgments

- Dataset dari Twitter dan TikTok
- IndoBERT untuk sentiment classification
- Sastrawi untuk Indonesian text processing
- Flask framework
- Plotly untuk visualisasi interaktif
- Tailwind CSS untuk styling

---

⭐ Jika project ini membantu, jangan lupa kasih star!
