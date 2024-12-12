# GHFConverter
 
#Funcionalidades Principais
*Download de vídeos: A aplicação permite baixar vídeos de diversas plataformas (YouTube, Facebook, Instagram) com diferentes formatos e resoluções.
*Extração de informações: Antes do download, a aplicação extrai informações como título, thumbnail e formatos disponíveis do vídeo.
*Processamento assíncrono: O download dos vídeos é realizado em segundo plano para não bloquear a resposta ao usuário.
*Interface amigável: A aplicação possui uma interface web intuitiva para o usuário inserir a URL do vídeo e iniciar o download.
*Gerenciamento de arquivos: A aplicação gerencia a criação, armazenamento e remoção dos arquivos baixados, incluindo a limpeza automática após um determinado período.

Destaques do Código
*Uso de yt_dlp: A biblioteca yt_dlp é utilizada para extrair informações e baixar vídeos de diversas plataformas, incluindo YouTube e Facebook.
*Tratamento de erros: O código inclui tratamento de erros para lidar com situações como URLs inválidas, falhas no download, etc.
*Personalização de formatos: A aplicação permite ao usuário escolher o formato do vídeo a ser baixado.
*Otimização de desempenho: O uso de threads e tarefas assíncronas contribui para um melhor desempenho da aplicação.
*Segurança: A aplicação remove os arquivos baixados após um determinado período, contribuindo para a segurança e otimização do armazenamento.
