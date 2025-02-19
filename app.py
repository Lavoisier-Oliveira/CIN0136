import json, sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import games
import gemini
app = Flask(__name__)
CORS(app)

user_data_path = 'user_data.json'
try:
    with open(user_data_path, 'r') as file:
        user_data = json.load(file)
except Exception:
    user_data = {'game_library': {}, 'game_recommendations': {'High Priority': {}, 'Low Priority': {}}}

bot = gemini.GeminiModel()

# ROTA QUE RETORNA RESPOSTA DA IA E ADICIONA OS JOGOS QUE ELA RECOMENDOU AO USER_DATA.JSON
@app.get("/genai/<prompt>")
def test(prompt: str):
    reply = eval(bot.send_message(prompt))
   
    for command in reply:
        task = reply.get('command', "")
        titles = command.get('titles', [])
    
        for idx, title in enumerate(titles):
            game_result = games.search_game(title)
            
            if task == 'Recommend':
                if idx == 0:
                    user_data['game_recommendations']['High Priority'][title] = game_result
                else:
                    user_data['game_recommendations']['Low Priority'][title] = game_result
            
            elif task == 'Add':
                user_data['game_library'][title] = {'rating':'unrated', 'state':'unplayed', 'data':game_result}
                
            elif task == 'Rate':
                user_data['game_library'].get(title, {'rating':''})['rating'] = reply.get('ratings', ['10'] * idx)[idx]
                
            elif task == 'State':
                user_data['game_library'].get(title, {'state':''})['state'] = reply.get('ratings', ['unplayed'] * idx)[idx]
            
            elif task == 'Remove':
                user_data['game_library'].get(title, {'rating':''})['rating'] = reply.get('ratings', ['10'] * idx)[idx]
                
                        
    with open(user_data_path, 'w') as file:
        json.dump(user_data, file)
        
    return reply
            
"""
@app.route('/submit-message', methods=['POST'])

def submit_message():
    try:
        
        data = request.get_json()
        print("Received data:", data)
        message = data.get('message')
        if not message:
            return jsonify({'error':'Nenhuma mensagem encontrada'}), 400
        App = QApplication(sys.argv)
        window = MainWindow()
        window.ai_response(message)
        return jsonify({'status':'sucesso', 'message':'Mensagem recebida'}),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route ('/send-library', methods=['GET'])

def send_library():
    with open ("./user_data.json", 'r') as file:
        if not file:
            return jsonify({'status':'erro', 'message':'Json não aberto'})
        user_data = json.load(file)
    return jsonify(user_data)


"""
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    