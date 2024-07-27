import yt_dlp
from yt_dlp.utils import DownloadError
import os
import imageio_ffmpeg as ffmpeg

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'noplaylist': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            
            desired_resolutions = {'240p', '360p', '480p', '720p', '1080p'}
            formats = [f for f in info_dict.get('formats', []) if f.get('ext') == 'mp4' and f.get('format_note') in desired_resolutions]
            info_dict['formats'] = formats
            return info_dict
    except DownloadError as e:
        raise ValueError('Erro ao extrair informações do vídeo. Verifique a URL.')

def download_video(url, format_id):
    ydl_opts = {
        'format': f'{format_id}+bestaudio/best',  # Baixar o melhor áudio disponível
        'outtmpl': 'media/%(title)s.%(ext)s',  # Salvar na pasta media
        'noplaylist': True,
        'merge_output_format': 'mp4',  # Garantir que o arquivo resultante seja em formato mp4
        'ffmpeg_location': ffmpeg.get_ffmpeg_exe(),  # Usar o ffmpeg embutido
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            # Pega o nome do arquivo da pasta 'media'
            filename = ydl.prepare_filename(ydl.extract_info(url, download=False))
            return filename.split('/')[-1]  # Retorna o nome do arquivo
    except DownloadError as e:
        raise ValueError('Erro ao baixar o vídeo. Verifique a URL e o formato.')
