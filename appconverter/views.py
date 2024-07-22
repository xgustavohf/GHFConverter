from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from .forms import YouTubeDownloadForm
from .youtube_downloader import get_video_info, download_video
import os

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
            filename = download_video(url, format_id)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
            
            def remove_file():
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            # Use a background thread or a delayed call to remove the file after a short delay
            import threading
            threading.Timer(5.0, remove_file).start()  # Ajuste o tempo conforme necessário
            
            return response
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
