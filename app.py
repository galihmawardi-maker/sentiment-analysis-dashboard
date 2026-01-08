from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime

app = Flask(__name__)

# Konfigurasi
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Data global (akan di-load dari CSV)
df_data = None

def load_data():
    """Load data dari CSV jika ada"""
    global df_data
    try:
        if os.path.exists('data/dataset_labeled_final.csv'):
            df_data = pd.read_csv('data/dataset_labeled_final.csv')
            return True
    except Exception as e:
        print(f"Error loading data: {e}")
    return False

@app.route('/')
def index():
    """Halaman utama dashboard"""
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    """API untuk mendapatkan statistik data"""
    if df_data is None:
        return jsonify({'error': 'Data belum di-upload'}), 400
    
    try:
        # Statistik umum
        total_data = len(df_data)
        
        # Distribusi sentimen
        sentiment_dist = df_data['sentiment_label'].value_counts().to_dict()
        sentiment_pct = (df_data['sentiment_label'].value_counts(normalize=True) * 100).round(2).to_dict()
        
        # Distribusi per platform
        platform_dist = df_data.groupby(['platform', 'sentiment_label']).size().to_dict()
        
        # Statistik engagement
        avg_likes = df_data['likes'].mean()
        avg_retweets = df_data['retweets'].mean()
        avg_replies = df_data['replies'].mean()
        
        return jsonify({
            'total_data': total_data,
            'sentiment_distribution': sentiment_dist,
            'sentiment_percentage': sentiment_pct,
            'platform_distribution': platform_dist,
            'avg_engagement': {
                'likes': round(avg_likes, 2),
                'retweets': round(avg_retweets, 2),
                'replies': round(avg_replies, 2)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sentiment-chart')
def sentiment_chart():
    """API untuk chart distribusi sentimen"""
    if df_data is None:
        return jsonify({'error': 'Data belum di-upload'}), 400
    
    try:
        # Pie chart distribusi sentimen
        sentiment_counts = df_data['sentiment_label'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=0.3,
            marker_colors=['#EF4444', '#F59E0B', '#10B981']
        )])
        
        fig.update_layout(
            title='Distribusi Sentimen',
            showlegend=True,
            height=400
        )
        
        return jsonify(json.loads(fig.to_json()))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/platform-chart')
def platform_chart():
    """API untuk chart distribusi per platform"""
    if df_data is None:
        return jsonify({'error': 'Data belum di-upload'}), 400
    
    try:
        # Bar chart per platform
        platform_sentiment = df_data.groupby(['platform', 'sentiment_label']).size().reset_index(name='count')
        
        fig = px.bar(
            platform_sentiment,
            x='platform',
            y='count',
            color='sentiment_label',
            title='Distribusi Sentimen per Platform',
            color_discrete_map={
                'negative': '#EF4444',
                'neutral': '#F59E0B',
                'positive': '#10B981'
            },
            barmode='group'
        )
        
        fig.update_layout(height=400)
        
        return jsonify(json.loads(fig.to_json()))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/timeline-chart')
def timeline_chart():
    """API untuk chart timeline sentimen"""
    if df_data is None:
        return jsonify({'error': 'Data belum di-upload'}), 400
    
    try:
        # Parse timestamp dan buat timeline
        df_temp = df_data.copy()
        df_temp['date'] = pd.to_datetime(df_temp['timestamp']).dt.date
        
        timeline = df_temp.groupby(['date', 'sentiment_label']).size().reset_index(name='count')
        
        fig = px.line(
            timeline,
            x='date',
            y='count',
            color='sentiment_label',
            title='Timeline Sentimen',
            color_discrete_map={
                'negative': '#EF4444',
                'neutral': '#F59E0B',
                'positive': '#10B981'
            }
        )
        
        fig.update_layout(height=400)
        
        return jsonify(json.loads(fig.to_json()))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/wordcloud-data')
def wordcloud_data():
    """API untuk data word cloud"""
    if df_data is None:
        return jsonify({'error': 'Data belum di-upload'}), 400
    
    try:
        sentiment = request.args.get('sentiment', 'positive')
        
        # Filter berdasarkan sentimen
        filtered_df = df_data[df_data['sentiment_label'] == sentiment]
        
        # Gabungkan semua teks
        all_text = ' '.join(filtered_df['text_clean'].fillna('').astype(str))
        
        # Hitung frekuensi kata
        words = all_text.split()
        word_freq = pd.Series(words).value_counts().head(50)
        
        return jsonify({
            'words': word_freq.index.tolist(),
            'frequencies': word_freq.values.tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """API untuk upload file CSV"""
    global df_data
    
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Nama file kosong'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File harus CSV'}), 400
    
    try:
        # Baca CSV
        df_data = pd.read_csv(file)
        
        # Validasi kolom yang diperlukan
        required_cols = ['text_clean', 'sentiment_label', 'platform', 'timestamp', 'likes', 'retweets', 'replies']
        missing_cols = [col for col in required_cols if col not in df_data.columns]
        
        if missing_cols:
            return jsonify({'error': f'Kolom yang hilang: {", ".join(missing_cols)}'}), 400
        
        return jsonify({
            'success': True,
            'message': f'File berhasil di-upload. Total {len(df_data)} baris data.',
            'total_rows': len(df_data)
        })
    except Exception as e:
        return jsonify({'error': f'Error membaca file: {str(e)}'}), 500

@app.route('/api/model-comparison')
def model_comparison():
    """API untuk perbandingan akurasi model"""
    try:
        # Data akurasi model (sesuaikan dengan hasil dari notebook)
        models_data = {
            'models': ['Naive Bayes', 'SVM', 'Random Forest'],
            'accuracy': [0.6416, 0.6977, 0.6501],  # Contoh data
            'precision': [0.64, 0.70, 0.65],
            'recall': [0.64, 0.69, 0.65],
            'f1_score': [0.64, 0.69, 0.65]
        }
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Accuracy',
            x=models_data['models'],
            y=models_data['accuracy'],
            text=[f"{x:.2%}" for x in models_data['accuracy']],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Perbandingan Akurasi Model',
            yaxis_title='Accuracy',
            yaxis_range=[0, 1],
            height=400,
            showlegend=False
        )
        
        return jsonify(json.loads(fig.to_json()))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data-table')
def data_table():
    """API untuk tabel data"""
    if df_data is None:
        return jsonify({'error': 'Data belum di-upload'}), 400
    
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        sentiment_filter = request.args.get('sentiment', None)
        
        # Filter data
        filtered_df = df_data.copy()
        if sentiment_filter and sentiment_filter != 'all':
            filtered_df = filtered_df[filtered_df['sentiment_label'] == sentiment_filter]
        
        # Pagination
        total = len(filtered_df)
        start = (page - 1) * per_page
        end = start + per_page
        
        data_slice = filtered_df.iloc[start:end]
        
        # Konversi ke dictionary
        records = data_slice[['post_id', 'user_handle', 'text_clean', 'sentiment_label', 'platform', 'likes', 'retweets']].to_dict('records')
        
        return jsonify({
            'data': records,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load data saat startup
    load_data()
    
    # Jalankan aplikasi
    app.run(debug=True, host='0.0.0.0', port=5000)
