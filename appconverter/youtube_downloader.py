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
            
            desired_resolutions = {'144p', '240p', '360p', '480p', '720p', '1080p'}
            formats = [
                {
                    'format_id': f.get('format_id'),
                    'format_note': f.get('format_note'),
                    'filesize': f.get('filesize', 0)  # Tamanho do arquivo em bytes
                }
                for f in info_dict.get('formats', [])
                if f.get('ext') == 'mp4' and f.get('format_note') in desired_resolutions
            ]
            info_dict['formats'] = formats
            return info_dict
    except DownloadError as e:
        raise ValueError('Erro ao extrair informações do vídeo. Verifique a URL.')

def download_video(url, format_id, title):
    ydl_opts = {
        'format': f'{format_id}+bestaudio/best',
        'outtmpl': f'media/{title}.%(ext)s',  # Salvar na pasta media com o título do vídeo
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'ffmpeg_location': ffmpeg.get_ffmpeg_exe(),
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict).split('/')[-1]
            return filename  # Retorna o nome do arquivo
    except DownloadError as e:
        raise ValueError('Erro ao baixar o vídeo. Verifique a URL e o formato.')