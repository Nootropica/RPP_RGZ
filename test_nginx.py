import requests
import json
from collections import Counter

def test_nginx_balancing():
    print("Тестирование балансировки нагрузки Nginx...")
    print("=" * 50)
    
    ports = []
    
    for i in range(1, 10):
        try:
            response = requests.get('http://localhost:80/health', timeout=2)
            data = response.json()
            port = data['port']
            ports.append(port)
            print(f"Запрос {i:2d} -> Flask порт: {port}")
        except Exception as e:
            print(f"Запрос {i:2d} -> Ошибка: {e}")
    
    print("=" * 50)
    print("Распределение запросов:")
    print("Порт   | Количество")
    print("-------+-----------")
    
    port_counts = Counter(ports)
    for port in sorted(port_counts.keys()):
        print(f"{port:6} | {port_counts[port]}")
    
    print("=" * 50)
    print(f"Всего запросов: {len(ports)}")
    print(f"Уникальных портов: {len(port_counts)}")

if __name__ == "__main__":
    test_nginx_balancing()