from flask import Flask, render_template, request, jsonify
from sumarizador import processar_texto
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sumarizar', methods=['POST'])
def sumarizar():
    try:
        # Verifica se os dados são JSON
        if not request.is_json:
            return jsonify({'erro': 'Content-Type deve ser application/json'}), 400
        
        data = request.get_json()
        texto = data.get('texto', '').strip()
        
        if not texto:
            return jsonify({'erro': 'Texto não pode estar vazio'}), 400
        
        resultado = processar_texto(texto)
        
        # Garante que o resultado sempre tenha a estrutura esperada
        if 'erro' in resultado:
            return jsonify({'erro': resultado['erro']}), 400
        
        return jsonify({
            'texto_original': resultado.get('texto_original', ''),
            'resumo': resultado.get('resumo', ''),
            'palavras_original': resultado.get('palavras_original', 0),
            'palavras_resumo': resultado.get('palavras_resumo', 0)
        })
    
    except Exception as e:
        return jsonify({'erro': f'Erro interno no servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)