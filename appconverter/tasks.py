from celery import shared_task
import yt_dlp
from yt_dlp.utils import DownloadError
import imageio_ffmpeg as ffmpeg
import os

@shared_task
def download_video_task(url, format_id, title):
    ydl_opts = {
        'format': f'{format_id}+bestaudio/best',
        'outtmpl': f'media/{title}.%(ext)s',
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'ffmpeg_location': ffmpeg.get_ffmpeg_exe(),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict).split('/')[-1]
            return filename
    except DownloadError as e:
        raise ValueError('Erro ao baixar o vídeo. Verifique a URL e o formato.')