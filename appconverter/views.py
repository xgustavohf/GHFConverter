from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from .forms import YouTubeDownloadForm
from .tasks import download_video_task
from django.views.decorators.csrf import csrf_exempt
from .youtube_downloader import get_video_info, download_video
import instaloader
import requests
import yt_dlp
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

        # Lógica para baixar vídeo do Instagram
        loader = instaloader.Instaloader()
        try:
            shortcode = url.split('/')[-2]
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            video_url = post.video_url

            # Download do vídeo
            video_response = requests.get(video_url, stream=True)
            if video_response.status_code == 200:
                response = HttpResponse(video_response.content, content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename="video.mp4"'
                return response
            else:
                return JsonResponse({'error': 'Não foi possível baixar o vídeo'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método não permitido'}, status=405)