document.getElementById('videoForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('/instagram-download/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Erro: ' + data.error);
        } else {
            document.getElementById('videoInfo').style.display = 'block';
            document.getElementById('videoTitle').innerText = data.title; // Atualiza o título do vídeo
            document.getElementById('downloadButton').dataset.videoUrl = data.video_url; // Armazena a URL do vídeo
            document.getElementById('downloadButton').dataset.videoTitle = data.title; // Armazena o título do vídeo
        }
    })
    .catch(error => {
        alert('Erro na solicitação: ' + error.message);
    });
});

document.getElementById('downloadButton').addEventListener('click', function() {
    const videoUrl = this.dataset.videoUrl;
    const videoTitle = this.dataset.videoTitle || 'video'; // Usa 'video' como fallback

    if (!videoUrl) {
        alert('URL do vídeo não disponível.');
        return;
    }

    const statusMessage = document.getElementById('statusMessage');
    statusMessage.innerHTML = '<div class="alert alert-info" role="alert"><strong>Informação:</strong> Seu download está sendo processado.</div>';
    statusMessage.style.display = 'block';

    fetch(videoUrl)
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            return response.json().then(data => {
                alert(data.error || 'Falha no download.');
            });
        }
    })
    .then(blob => {
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        
        // Processa o título para ser um nome de arquivo válido
        let fileName = videoTitle.replace(/[<>:"/\\|?*\x00-\x1F]/g, '_'); // Substitui caracteres inválidos por '_'
        fileName = fileName.substring(0, 30); // Limita o nome do arquivo a 30 caracteres
        a.download = fileName + '.mp4'; // Usa o título do vídeo como nome do arquivo
        
        a.click();
        
        // Atualiza o status para concluído após o download
        statusMessage.innerHTML = '<div class="alert alert-success" role="alert"><strong>Concluído:</strong> Download concluído!.</div>';
    })
    .catch(error => {
        statusMessage.innerHTML = '<div class="alert alert-danger" role="alert"><strong>Erro:</strong> Ocorreu um erro ao processar seu pedido.</div>';
    });
});
