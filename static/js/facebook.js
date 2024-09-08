document.getElementById('videoForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var statusMessage = document.getElementById('statusMessage');
    statusMessage.style.display = 'none';

    var formData = new FormData(this);
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(facebookUrl, {  // Use a variável que contém a URL
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            statusMessage.innerHTML = '<div class="alert alert-danger" role="alert"><strong>Erro:</strong> ' + data.error + '</div>';
            statusMessage.style.display = 'block';
        } else {
            document.getElementById('videoThumbnail').src = data.thumbnail_url;
            document.getElementById('videoTitle').textContent = data.title;
            document.getElementById('videoInfo').style.display = 'block';

            // Adiciona o scroll automático para a div 'videoInfo'
            document.getElementById('videoInfo').scrollIntoView({ behavior: 'smooth' });

            document.getElementById('urlInput').value = formData.get('url');
        }
    })
    .catch(error => {
        statusMessage.innerHTML = '<div class="alert alert-danger" role="alert"><strong>Erro:</strong> Ocorreu um erro ao buscar as informações do vídeo.</div>';
        statusMessage.style.display = 'block';
    });
});

document.getElementById('downloadButton').addEventListener('click', function() {
    var statusMessage = document.getElementById('statusMessage');
    statusMessage.innerHTML = '<div class="alert alert-info" role="alert"><strong>Informação:</strong> Seu download está sendo processado.</div>';
    statusMessage.style.display = 'block';

    var formData = new FormData();
    formData.append('url', document.getElementById('urlInput').value);
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(downloadUrl, {  // Use a variável que contém a URL
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            statusMessage.innerHTML = '<div class="alert alert-danger" role="alert"><strong>Erro:</strong> ' + data.error + '</div>';
        } else {
            var link = document.createElement('a');
            link.href = data.file_url;
            link.download = data.file_name || 'video.mp4';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            statusMessage.innerHTML = '<div class="alert alert-success" role="alert"><strong>Concluído:</strong> O vídeo foi baixado com sucesso.</div>';
        }
    })
    .catch(error => {
        statusMessage.innerHTML = '<div class="alert alert-danger" role="alert"><strong>Erro:</strong> Ocorreu um erro ao processar o download.</div>';
    });
});
