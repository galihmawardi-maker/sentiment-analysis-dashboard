# 🚀 Panduan Deployment Dashboard Analisis Sentimen

Panduan lengkap untuk men-deploy dashboard analisis sentimen ke berbagai platform.

## 📋 Daftar Isi

1. [Deployment Lokal (Development)](#1-deployment-lokal-development)
2. [Deployment ke Render (Gratis)](#2-deployment-ke-render-gratis)
3. [Deployment ke Railway](#3-deployment-ke-railway)
4. [Deployment ke PythonAnywhere (Gratis)](#4-deployment-ke-pythonanywhere-gratis)
5. [Deployment ke Heroku](#5-deployment-ke-heroku)
6. [Deployment ke VPS (DigitalOcean, AWS EC2)](#6-deployment-ke-vps)

---

## 1. 💻 Deployment Lokal (Development)

### Prerequisites
- Python 3.8+
- pip
- Git

### Langkah-langkah:

```bash
# 1. Clone repository
git clone https://github.com/galihmawardi-maker/sentiment-analysis-dashboard.git
cd sentiment-analysis-dashboard

# 2. Buat virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac  
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data
python -c "import nltk; nltk.download('stopwords')"

# 5. (Optional) Siapkan data
mkdir data
# Copy dataset_labeled_final.csv ke folder data/

# 6. Jalankan aplikasi
python app.py

# 7. Buka browser
# http://localhost:5000
```

---

## 2. 🌐 Deployment ke Render (Gratis)

**Render** menyediakan free tier yang bagus untuk Flask apps.

### Langkah-langkah:

#### A. Persiapan File

1. **Buat file `render.yaml`** di root project:

```yaml
services:
  - type: web
    name: sentiment-dashboard
    env: python
    buildCommand: pip install -r requirements.txt && python -c "import nltk; nltk.download('stopwords')"
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
```

2. **Tambahkan `gunicorn` ke `requirements.txt`**:

```txt
Flask==3.0.0
pandas==2.1.3
numpy==1.26.2
plotly==5.18.0
scikit-learn==1.3.2
Sastrawi==1.0.1
nltk==3.8.1
gunicorn==21.2.0
```

3. **Update `app.py`** - Ganti baris terakhir:

```python
if __name__ == '__main__':
    # Load data saat startup
    load_data()
    
    # Jalankan aplikasi
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

#### B. Deploy ke Render

1. Buat akun di [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect GitHub repository Anda
4. Pilih repository `sentiment-analysis-dashboard`
5. Konfigurasi:
   - **Name**: sentiment-dashboard
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python -c "import nltk; nltk.download('stopwords')"`
   - **Start Command**: `gunicorn app:app`
6. Click "Create Web Service"
7. Wait for deployment (5-10 menit)
8. Dashboard akan tersedia di `https://sentiment-dashboard.onrender.com`

**Free Tier Limits**:
- ✅ Gratis selamanya
- ⚠️ Sleep after 15 menit inactivity
- ⚠️ Cold start ~30 detik

---

## 3. 🚄 Deployment ke Railway

**Railway** sangat mudah dan fast.

### Langkah-langkah:

1. Buat file `Procfile`:

```
web: gunicorn app:app
```

2. Tambahkan `gunicorn` ke `requirements.txt`

3. Deploy:
   - Buat akun di [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Pilih repository
   - Railway auto-detect Python dan deploy
   - Generate domain

4. Environment Variables (Optional):
   - `PYTHON_VERSION=3.9`

**Free Tier**:
- $5 credit/month gratis
- Sleep tidak otomatis

---

## 4. 🐍 Deployment ke PythonAnywhere (Gratis)

**PythonAnywhere** ideal untuk Python apps.

### Langkah-langkah:

1. **Buat akun** di [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Open Bash console**:

```bash
# Clone repo
git clone https://github.com/galihmawardi-maker/sentiment-analysis-dashboard.git
cd sentiment-analysis-dashboard

# Buat virtual environment
mkvirtualenv --python=/usr/bin/python3.9 dashboard-env

# Install dependencies
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords')"
```

3. **Setup Web App**:
   - Click "Web" tab
   - "Add a new web app"
   - Choose "Manual configuration"
   - Python 3.9

4. **Configure WSGI file** (`/var/www/yourusername_pythonanywhere_com_wsgi.py`):

```python
import sys
import os

path = '/home/yourusername/sentiment-analysis-dashboard'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

5. **Set virtualenv path**:
```
/home/yourusername/.virtualenvs/dashboard-env
```

6. **Reload web app**

**Free Tier**:
- ✅ Gratis selamanya  
- ⚠️ yourusername.pythonanywhere.com domain
- ⚠️ Limited CPU/bandwidth

---

## 5. ☁️ Deployment ke Heroku

### Langkah-langkah:

1. **Buat file `Procfile`**:

```
web: gunicorn app:app
```

2. **Buat file `runtime.txt`**:

```
python-3.9.18
```

3. **Install Heroku CLI** dan login:

```bash
heroku login
```

4. **Deploy**:

```bash
# Buat app baru
heroku create sentiment-dashboard-app

# Push ke Heroku
git push heroku main

# Download NLTK data
heroku run python -c "import nltk; nltk.download('stopwords')"

# Open app
heroku open
```

**Note**: Heroku free tier sudah dihapus sejak November 2022. Minimum $5/bulan.

---

## 6. 🖥️ Deployment ke VPS (Production)

### A. DigitalOcean / AWS EC2

#### 1. Setup Server

```bash
# SSH ke server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Python
apt install python3 python3-pip python3-venv nginx -y
```

#### 2. Deploy Aplikasi

```bash
# Clone repo
cd /var/www
git clone https://github.com/galihmawardi-maker/sentiment-analysis-dashboard.git
cd sentiment-analysis-dashboard

# Setup venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords')"
```

#### 3. Setup Gunicorn Service

Buat file `/etc/systemd/system/dashboard.service`:

```ini
[Unit]
Description=Sentiment Dashboard
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/sentiment-analysis-dashboard
Environment="PATH=/var/www/sentiment-analysis-dashboard/venv/bin"
ExecStart=/var/www/sentiment-analysis-dashboard/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable dan start:

```bash
systemctl enable dashboard
systemctl start dashboard
systemctl status dashboard
```

#### 4. Setup Nginx

Buat file `/etc/nginx/sites-available/dashboard`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /var/www/sentiment-analysis-dashboard/static;
    }
}
```

Enable site:

```bash
ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 5. Setup SSL (Optional)

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

---

## 📊 Perbandingan Platform

| Platform | Gratis? | Sleep? | Setup | Best For |
|----------|---------|--------|-------|----------|
| **Render** | ✅ | ✅ (15 min) | Easy | Demo/Testing |
| **Railway** | 💰 ($5/month) | ❌ | Very Easy | Small Projects |
| **PythonAnywhere** | ✅ | ❌ | Medium | Student Projects |
| **Heroku** | ❌ ($5+) | ❌ | Easy | Production |
| **VPS** | ❌ ($5-20+) | ❌ | Hard | Production |

---

## 🔐 Tips Production

### 1. Environment Variables

Jangan hardcode sensitive data. Gunakan environment variables:

```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
DATABASE_URL = os.environ.get('DATABASE_URL')
```

### 2. Disable Debug Mode

```python
app.run(debug=False)
```

### 3. Use Gunicorn

Jangan pakai Flask development server di production.

### 4. Setup Logging

```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 5. Add Health Check Endpoint

```python
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

---

## 🆘 Troubleshooting

### Error: Module not found
```bash
pip install -r requirements.txt
```

### Error: NLTK data not found
```bash
python -c "import nltk; nltk.download('stopwords')"
```

### Port already in use
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Cold start too slow (Render)
Upgrade to paid tier atau gunakan cron job untuk keep-alive.

---

## 📞 Support

Jika ada masalah:
1. Check logs
2. Buka issue di GitHub
3. Email: [your-email]

---

**Happy Deploying!** 🚀
