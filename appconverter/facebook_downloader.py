import os
import requests
from bs4 import BeautifulSoup
import yt_dlp

MAX_FILENAME_LENGTH = 100

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
            title = info.get('description') or info.get('title', 'facebook_video')

            title = title[:30] + "..." if len(title) > 30 else title
            
            thumbnail_url = info.get('thumbnail')

            if video_url and title and thumbnail_url:
                return video_url, title, thumbnail_url
            else:
                raise ValueError('Não foi possível encontrar todas as informações do vídeo no URL fornecido.')
    except Exception as e:
        raise ValueError(f'Erro ao extrair o vídeo do Facebook: {str(e)}')


def download_facebook_video(facebook_url):
    video_url, title, _ = get_facebook_video_info(facebook_url)
    response = requests.get(video_url, stream=True)
    
    if response.status_code == 200:
        safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_', '-')])
        
        if len(safe_title) > MAX_FILENAME_LENGTH:
            safe_title = safe_title[:MAX_FILENAME_LENGTH]
        
        filename = f'{safe_title}.mp4'
        file_path = os.path.join('media', filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return filename
    else:
        raise ValueError('Erro ao baixar o vídeo do Facebook.')

