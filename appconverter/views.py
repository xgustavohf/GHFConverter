from django.http import HttpResponse, FileResponse, JsonResponse, Http404
from django.shortcuts import render
from django.conf import settings
from .forms import YouTubeDownloadForm
from .tasks import download_video_task
from django.views.decorators.csrf import csrf_exempt
from .youtube_downloader import get_video_info, download_video
from .facebook_downloader import download_facebook_video, get_facebook_video_info
import instaloader
import requests
import threading
import yt_dlp
import time
import tempfile
import re
import unicodedata
import os


def termos_uso(request):
    return render(request, 'termos.html')  

def politica_privacidade(request):
    return render(request, 'politica_privacidade.html')  

def contato(request):
    return render(request, 'contato.html')  

def facebook(request):
    return render(request, 'facebook.html')  

def youtube(request):
    return render(request, 'youtube.html')

def index(request):
    if request.method == 'POST':
        form = YouTubeDownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                info = get_video_info(url)
                return JsonResponse(info)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
    else:
        form = YouTubeDownloadForm()
    
    return render(request, 'download.html', {'form': form})


def remove_file_later(file_path, delay=60):
    """Remove o arquivo após um certo atraso."""
    def remove_file():
        time.sleep(delay)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    thread = threading.Thread(target=remove_file)
    thread.start()


#===============YOUTUBE===============#

def youtube(request):
    if request.method == 'POST':
        form = YouTubeDownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                info = get_video_info(url)
                return JsonResponse(info)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
    else:
        form = YouTubeDownloadForm()
    
    return render(request, 'youtube.html', {'form': form})


def download_video_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        format_id = request.POST.get('format_id')
        
        if not url or not format_id:
            return JsonResponse({'error': 'URL ou formato inválido.'}, status=400)
        
        try:
            info = get_video_info(url)
            title = info.get('title', 'video').replace(' ', '_')  # Pega o título e remove espaços
            filename = download_video(url, format_id, title)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
            
            def remove_file():
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            import threading
            threading.Timer(5.0, remove_file).start()
            
            return response
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        

def download_progress(request, task_id):
    task = download_video_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Download pendente...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('status', ''),
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'status': str(task.info),
        }
    return JsonResponse(response)


#===============INSTAGRAM===============#

def instagram_page(request):
    return render(request, 'instagram.html')

def instagram_download_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            return JsonResponse({'error': 'URL não fornecida'}, status=400)

        loader = instaloader.Instaloader()

        # Configurando o User-Agent diretamente na sessão de requests do Instaloader
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        loader.context._session.headers.update({'User-Agent': user_agent})

        try:
            shortcode = url.split('/')[-2]
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            video_url = post.video_url
            title = post.caption  # Use 'caption' para a descrição do vídeo

            # Limite o título a 30 caracteres
            if len(title) > 30:
                title = title[:30] + '...'  # Adiciona '...' se o título for truncado

            thumbnail_url = post.url  # Ajuste para obter a thumbnail correta

            return JsonResponse({'title': title, 'thumbnail': thumbnail_url, 'video_url': video_url})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


#===============FACEBOOK===============#

def facebook(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            return JsonResponse({'error': 'URL não fornecida'}, status=400)
        
        try:
            # Obtém as informações do vídeo (URL, título e thumbnail)
            video_url, title, thumbnail_url = get_facebook_video_info(url)
            
            return JsonResponse({'title': title, 'thumbnail_url': thumbnail_url})
        
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'facebook.html')


def download_video_facebook(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        try:
            filename = download_facebook_video(url)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            if os.path.exists(file_path):
                file_url = request.build_absolute_uri(settings.MEDIA_URL + filename)
                remove_file_later(file_path)
                return JsonResponse({'file_url': file_url, 'file_name': filename})
            else:
                return JsonResponse({'error': 'Arquivo não encontrado'}, status=404)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)



#===============YOUTUBE MP3===============#

def youtube_audio(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        if not url:
            return JsonResponse({'error': 'URL não fornecida'}, status=400)

        # Obter informações do vídeo sem fazer o download
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Iniciar o download em segundo plano
                download_thread = threading.Thread(target=download_and_save_audio, args=(url, info['id'], info.get('title')))
                download_thread.start()

                # Preparar a resposta com informações do vídeo
                formats = [{
                    'url': f'/download/{sanitize_filename(info["title"])}.mp3',
                    'quality': 'alta',
                    'bitrate': '192'
                }]
                return JsonResponse({
                    'title': info.get('title'),
                    'thumbnail': info.get('thumbnail'),
                    'formats': formats
                })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'youtube_audio.html')


def sanitize_filename(filename):
    # Remove caracteres não ASCII e substitui espaços e caracteres especiais por _
    filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('ASCII')
    filename = re.sub(r'[^\w\s-]', '', filename).strip()
    filename = re.sub(r'[-\s]+', '_', filename)
    return filename


def download_and_save_audio(url, video_id, title):
    sanitized_title = sanitize_filename(title)
    outtmpl = os.path.join(settings.MEDIA_ROOT, f'{sanitized_title}.%(ext)s')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': outtmpl,
        'noplaylist': True,
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Erro ao baixar o áudio: {str(e)}")


def serve_audio(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')
        remove_file_later(file_path)  # Remover o arquivo após o download
        return response
    else:
        print(f"Arquivo não encontrado: {file_path}")  # Para depuração
        raise Http404("Arquivo não encontrado")

def check_download_status(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    file_exists = os.path.exists(file_path)
    return JsonResponse({'ready': file_exists})