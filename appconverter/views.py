from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from .forms import YouTubeDownloadForm
from .tasks import download_video_task
from django.views.decorators.csrf import csrf_exempt
from .youtube_downloader import get_video_info, download_video
from .facebook_downloader import download_facebook_video
import instaloader
import requests
import threading
import yt_dlp
import time
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

def instagram_page(request):
    return render(request, 'instagram.html')

def instagram_download_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            return JsonResponse({'error': 'URL não fornecida'}, status=400)

        loader = instaloader.Instaloader()
        try:
            shortcode = url.split('/')[-2]
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            video_url = post.video_url
            title = post.caption  # Use 'caption' para a descrição do vídeo
            thumbnail_url = post.url  # Ajuste para obter a thumbnail correta

            return JsonResponse({'title': title, 'thumbnail': thumbnail_url, 'video_url': video_url})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


def remove_file_later(file_path, delay=5):
    """Remove o arquivo após um certo atraso."""
    def remove_file():
        time.sleep(delay)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    thread = threading.Thread(target=remove_file)
    thread.start()

def facebook(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            return JsonResponse({'error': 'URL não fornecida'}, status=400)
        
        try:
            filename = download_facebook_video(url)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            
            if os.path.exists(file_path):
                file_url = request.build_absolute_uri(settings.MEDIA_URL + filename)
                
                # Inicia a thread para remover o arquivo após um atraso
                remove_file_later(file_path)
                
                return JsonResponse({'file_url': file_url, 'file_name': filename})
            else:
                return JsonResponse({'error': 'Arquivo não encontrado'}, status=404)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'facebook.html')
