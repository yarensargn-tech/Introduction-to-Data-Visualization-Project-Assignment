"""
Akıllı Şebeke Stres Analiz Sistemi
Smart Grid Stress Analysis System

Bu sistem elektrik şebekesinin gerçek zamanlı olarak izlenmesi, stres durumlarının
tespit edilmesi ve Ollama LLM kullanılarak operatörlere akıllı öneriler sunulması
için tasarlanmıştır.

Author: Veri Görselleştirme Dersi Projesi
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import datetime
from modules.grid_simulator import GridSimulator
from modules.stress_analyzer import StressAnalyzer
from modules.llm_advisor import LLMAdvisor
from modules.data_logger import DataLogger

app = Flask(__name__)
CORS(app)

# Ana bileşenleri başlat
simulator = GridSimulator()
analyzer = StressAnalyzer()
llm_advisor = LLMAdvisor()
logger = DataLogger()


@app.route('/')
def index():
    """Ana dashboard sayfası"""
    return render_template('index.html')


@app.route('/api/grid/snapshot')
def grid_snapshot():
    """Şebeke anlık durumu - tüm sensörlerin son verileri"""
    snapshot = simulator.get_current_snapshot()
    stress_data = analyzer.analyze_snapshot(snapshot)
    
    response = {
        'timestamp': datetime.datetime.now().isoformat(),
        'substations': snapshot['substations'],
        'transmission_lines': snapshot['transmission_lines'],
        'overall_stress': stress_data['overall_stress'],
        'stress_level': stress_data['stress_level'],
        'critical_components': stress_data['critical_components'],
        'metrics': {
            'total_load_mw': snapshot['total_load_mw'],
            'total_generation_mw': snapshot['total_generation_mw'],
            'frequency_hz': snapshot['frequency_hz'],
            'avg_voltage_kv': snapshot['avg_voltage_kv'],
            'system_losses_percent': snapshot['system_losses_percent']
        }
    }
    
    # Veriyi logla
    logger.log_snapshot(response)
    
    return jsonify(response)


@app.route('/api/grid/history')
def grid_history():
    """Geçmiş veri - grafikler için"""
    minutes = request.args.get('minutes', 60, type=int)
    history = logger.get_history(minutes)
    return jsonify(history)


@app.route('/api/grid/inject_stress', methods=['POST'])
def inject_stress():
    """Manüel stres testi - belirli bileşene yük bindir"""
    data = request.json
    component_id = data.get('component_id')
    stress_amount = data.get('stress_amount', 30)
    duration = data.get('duration', 60)
    
    simulator.inject_stress(component_id, stress_amount, duration)
    
    return jsonify({
        'status': 'success',
        'message': f'{component_id} bileşenine {stress_amount}% stres uygulandı',
        'duration': duration
    })


@app.route('/api/grid/scenario', methods=['POST'])
def run_scenario():
    """Senaryo çalıştır - örn: 'kış pik yükü', 'yaz klima yükü'"""
    data = request.json
    scenario = data.get('scenario', 'normal')
    
    simulator.set_scenario(scenario)
    
    return jsonify({
        'status': 'success',
        'scenario': scenario,
        'message': f'{scenario} senaryosu aktif edildi'
    })


@app.route('/api/llm/analyze', methods=['POST'])
def llm_analyze():
    """LLM ile derinlemesine analiz - operatöre öneri sun"""
    data = request.json
    context = data.get('context', {})
    question = data.get('question', '')
    
    # Eğer context boşsa, mevcut sistem durumunu al
    if not context:
        snapshot = simulator.get_current_snapshot()
        stress_data = analyzer.analyze_snapshot(snapshot)
        context = {
            'snapshot': snapshot,
            'stress': stress_data
        }
    
    # LLM'den analiz iste
    analysis = llm_advisor.analyze(context, question)
    
    return jsonify(analysis)


@app.route('/api/llm/recommend')
def llm_recommend():
    """Mevcut durum için otomatik öneri - operatör paneli için"""
    snapshot = simulator.get_current_snapshot()
    stress_data = analyzer.analyze_snapshot(snapshot)
    
    recommendation = llm_advisor.get_recommendation(snapshot, stress_data)
    
    return jsonify(recommendation)


@app.route('/api/llm/chat', methods=['POST'])
def llm_chat():
    """Operatör asistan sohbet API'si"""
    data = request.json
    message = data.get('message', '')
    history = data.get('history', [])
    
    # Mevcut sistem durumunu da context olarak ekle
    snapshot = simulator.get_current_snapshot()
    stress_data = analyzer.analyze_snapshot(snapshot)
    
    response = llm_advisor.chat(message, history, snapshot, stress_data)
    
    return jsonify(response)


@app.route('/api/statistics/summary')
def statistics_summary():
    """İstatistiksel özet - geçmiş verilerden"""
    stats = logger.get_statistics()
    return jsonify(stats)


@app.route('/api/anomalies')
def get_anomalies():
    """Tespit edilen anomalileri döndür"""
    anomalies = analyzer.get_recent_anomalies()
    return jsonify(anomalies)


@app.route('/api/health')
def health_check():
    """Sistem sağlık kontrolü"""
    ollama_status = llm_advisor.check_connection()
    return jsonify({
        'status': 'healthy',
        'ollama_connected': ollama_status['connected'],
        'ollama_model': ollama_status.get('model', 'N/A'),
        'simulator_running': simulator.is_running(),
        'timestamp': datetime.datetime.now().isoformat()
    })


@app.route('/api/components')
def get_components():
    """Tüm şebeke bileşenlerinin listesi"""
    return jsonify(simulator.get_all_components())


if __name__ == '__main__':
    print("=" * 60)
    print("  AKILLI ŞEBEKE STRES ANALİZ SİSTEMİ")
    print("  Smart Grid Stress Analysis System")
    print("=" * 60)
    print(f"  Başlatılıyor: http://localhost:5000")
    print(f"  Ollama bağlantısı kontrol ediliyor...")
    
    health = llm_advisor.check_connection()
    if health['connected']:
        print(f"  ✓ Ollama bağlı - Model: {health.get('model', 'unknown')}")
    else:
        print(f"  ⚠ Ollama bağlı değil - LLM özellikleri sınırlı çalışacak")
        print(f"    Çözüm: 'ollama serve' komutunu çalıştırın")
    
    print("=" * 60)
    
    simulator.start()
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
