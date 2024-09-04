document.getElementById('audioForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    // Esconder o statusMessage ao iniciar uma nova consulta
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.style.display = 'none';
    statusMessage.textContent = ''; // Limpa o conteúdo da mensagem

    fetch('', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Erro: ' + data.error);
        } else {
            document.getElementById('audioInfo').style.display = 'block';
            document.getElementById('thumbnail').src = data.thumbnail;
            document.getElementById('audioTitle').textContent = data.title;

            // Preenche as opções de qualidade no seletor
            const formatSelector = document.getElementById('formatSelector');
            formatSelector.innerHTML = ''; // Limpa as opções anteriores
            data.formats.forEach(format => {
                const option = document.createElement('option');
                option.value = format.url.split('/').pop(); // Apenas o nome do arquivo
                option.textContent = `${format.quality} (${format.bitrate} kbps)`;
                formatSelector.appendChild(option);
            });
        }
    })
    .catch(error => {
        alert('Erro ao processar a solicitação.');
        console.error('Erro:', error);
    });
});

document.getElementById('downloadButton').addEventListener('click', function() {
    console.log('Download button clicked');
    const selectedFormatUrl = document.getElementById('formatSelector').value;
    const statusMessage = document.getElementById('statusMessage');
    if (selectedFormatUrl) {
        statusMessage.style.display = 'block';
        statusMessage.textContent = 'Realizando download, por favor, aguarde...';

        // Verificar o status do download
        const statusUrl = `/check_download_status/${encodeURIComponent(selectedFormatUrl)}`;
        fetch(statusUrl)
            .then(response => response.json())
            .then(data => {
                if (data.ready) {
                    const downloadUrl = `/download/${encodeURIComponent(selectedFormatUrl)}`;
                    fetch(downloadUrl)
                        .then(response => {
                            if (response.ok) {
                                return response.blob();
                            }
                            throw new Error('Erro ao fazer o download.');
                        })
                        .then(blob => {
                            const url = window.URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = selectedFormatUrl;
                            a.click();
                            window.URL.revokeObjectURL(url);
                            statusMessage.textContent = 'Download concluído!';
                        })
                        .catch(error => {
                            statusMessage.textContent = 'Erro ao baixar o arquivo de áudio.';
                            console.error('Erro:', error);
                        });
                } else {
                    statusMessage.textContent = 'O download está em andamento. Por favor, aguarde alguns segundos e tente clicar em "Baixar" novamente.';
                }
            })
            .catch(error => {
                statusMessage.textContent = 'Erro ao verificar o status do download.';
                console.error('Erro:', error);
            });
    } else {
        alert('Por favor, selecione uma qualidade para baixar.');
    }
});
