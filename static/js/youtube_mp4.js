document.getElementById('videoForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const url = document.querySelector('input[name="url"]').value.trim();

    if (!url) {
        alert('Por favor, insira uma URL válida.');
        return;
    }

    const formData = new FormData(this);
    document.getElementById('statusMessage').style.display = 'block';
    document.getElementById('statusMessage').innerText = 'Buscando informações do vídeo...';

    fetch('', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('statusMessage').innerText = data.error;
            return;
        }

        document.getElementById('videoInfo').style.display = 'block';
        document.getElementById('thumbnail').src = data.thumbnail;
        document.getElementById('videoTitle').innerText = data.title;

        const formatSelector = document.getElementById('formatSelector');
        formatSelector.innerHTML = '';
        data.formats.forEach(format => {
            const option = document.createElement('option');
            option.value = format.format_id;
            const filesizeMB = (format.filesize / (1024 * 1024)).toFixed(2); 
            option.textContent = `${format.format_note} - ${filesizeMB} MB`;
            formatSelector.appendChild(option);
        });

        document.getElementById('statusMessage').innerText = 'Selecione a qualidade e clique em Baixar.';

        // Scroll automático para o elemento videoInfo
        document.getElementById('videoInfo').scrollIntoView({ behavior: 'smooth' });

        document.getElementById('downloadButton').addEventListener('click', function() {
            const formatId = formatSelector.value;
            document.getElementById('statusMessage').innerText = 'Iniciando o download...';

            fetch('/download/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
                },
                body: new URLSearchParams({url: url, format_id: formatId})
            })
            .then(response => {
                if (response.ok) {
                    return response.blob();
                } else {
                    return response.json().then(data => {
                        document.getElementById('statusMessage').innerText = data.error || 'Falha no download.';
                    });
                }
            })
            .then(blob => {
                const a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = `${data.title}.mp4`; 
                a.click();
                document.getElementById('statusMessage').innerText = 'Download concluído!';
            });
        });
    })
    .catch(error => {
        document.getElementById('statusMessage').innerText = 'Erro ao buscar informações do vídeo.';
    });
});
