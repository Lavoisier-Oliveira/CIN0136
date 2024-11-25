import requests

# API Keys
GIANT_BOMB_API = "PLACEHOLDER" # Games database
TMDB_API = "PLACEHOLDER" # Movies database

# Função para pesquisar nomes de filmes no TMDB 
def get_movie_data(movie_name, API_KEY=TMDB_API):
    """
    param: movie_name (string): Nome do filme a ser pesquisado
    return: movies (list): Lista de resultados de pesquisa, cada resultado é um dicionário de informações sobre um filme com as seguintes keys:
    ['adult', 'backdrop_path', 'genre_ids', 'id', 'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 'release_date', 'title', 'video', 'vote_average', 'vote_count']
    """

    url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(url, headers=headers)
    movies = response.json().get("results", [])
    return movies


# Função para pesquisar nomes de jogos no GiantBomb 
def get_game_data(game_name, API_KEY=GIANT_BOMB_API):
    """
    param: game_name (string): Nome do jogo a ser pesquisado
    return: games (list): Lista de resultados de pesquisa, cada resultado é um dicionário de informações sobre um jogo com as seguintes keys:
    ['aliases', 'api_detail_url', 'date_added', 'date_last_updated', 'deck', 'description', 'guid', 'id', 'image', 'image_tags', 'name', 'site_detail_url', 'resource_type']
    image_tags é também um dicionário com as keys: ['icon_url', 'medium_url', 'screen_url', 'screen_large_url', 'small_url', 'super_url', 'thumb_url', 'tiny_url', 'original_url', 'image_tags']
    """

    url = f'https://www.giantbomb.com/api/search/?api_key={API_KEY}&format=JSON&query={game_name}'
    response = requests.get(url, headers={'user-agent':'newcoder'})
    search_results = response.json().get("results", [])
    games = [game for game in search_results if game.get('resource_type') == 'game']
    return games

def url_to_png(mode, data, file_name):
    if mode == 'movie':
        path = data.get('poster_path')
        url = f'https://image.tmdb.org/t/p/original/{path}' 
    elif mode == 'game':
        url = data.get('image', {}).get('original_url')
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'caching/images_cache/{mode}/{file_name}.png', 'wb') as file:
            file.write(response.content)

