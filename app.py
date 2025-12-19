from flask import Flask, request, jsonify
from collections import Counter
import re
import sys

app = Flask(__name__)

def analyze_text(text):
    # Очистка текста и разделение на слова
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Подсчет общего количества слов
    total_words = len(words)
    
    # Определение самых частотных слов
    word_counts = Counter(words)
    top_words = word_counts.most_common(10)  # топ 10 слов
    
    return total_words, top_words

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    total_words, top_words = analyze_text(text)
    
    # Форматируем результат
    top_words_formatted = [{'word': word, 'count': count} for word, count in top_words]
    
    return jsonify({
        'total_words': total_words,
        'top_words': top_words_formatted,
        'processed_by': f"instance_{port}"
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Берем порт из аргументов или используем 5001 по умолчанию
    port = 5001
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    
    print(f"Запуск Flask приложения на порте {port}")
    app.run(debug=False, host='127.0.0.1', port=port)