import os
import requests
from bs4 import BeautifulSoup
import yt_dlp

def get_facebook_video_info(facebook_url):
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'best',
            'noplaylist': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(facebook_url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'facebook_video')
            if video_url:
                return video_url, title
            else:
                raise ValueError('Não foi possível encontrar o vídeo no URL fornecido.')
    except Exception as e:
        raise ValueError(f'Erro ao extrair o vídeo do Facebook: {str(e)}')

def download_facebook_video(facebook_url):
    video_url, title = get_facebook_video_info(facebook_url)
    response = requests.get(video_url, stream=True)
    
    if response.status_code == 200:
        # Limpar o título para criar um nome de arquivo seguro
        safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_', '-')])
        filename = f'{safe_title}.mp4'
        file_path = os.path.join('media', filename)  # Use `os.path.join` para maior compatibilidade
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return filename
    else:
        raise ValueError('Erro ao baixar o vídeo do Facebook.')
