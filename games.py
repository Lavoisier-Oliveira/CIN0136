from dotenv import load_dotenv
import requests
import os

load_dotenv()

api_key = os.environ['GIANT_BOMB_API']

def search_game(game_name, API_KEY=api_key):
    """
    game_name (string): Nome do jogo a ser pesquisado
    return games (list): Lista de resultados de pesquisa, cada resultado é um dicionário de informações sobre um jogo com as seguintes keys:
    ['aliases', 'api_detail_url', 'date_added', 'date_last_updated', 'deck', 'description', 'guid', 'id', 'image', 'image_tags', 'name', 'site_detail_url', 'resource_type']
    image é também um dicionário com as keys: ['icon_url', 'medium_url', 'screen_url', 'screen_large_url', 'small_url', 'super_url', 'thumb_url', 'tiny_url', 'original_url', 'image_tags']
    """

    url = f'https://www.giantbomb.com/api/search/?api_key={API_KEY}&format=JSON&query={game_name}'
    response = requests.get(url, headers={'user-agent':'newcoder'})
    
    if response.status_code == 200:
        search_results = response.json().get("results", [])
        games = [game for game in search_results if game.get('resource_type') == 'game']
        return games
    else:
        return []
