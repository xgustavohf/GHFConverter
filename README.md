# GHFConverter 🎥➡️📁

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Django Version](https://img.shields.io/badge/django-4.0%2B-green)
![License](https://img.shields.io/badge/license-MIT-red)

Aplicação web para conversão e download de conteúdo multimídia de plataformas sociais.

## 📌 Índice
- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Arquitetura](#-arquitetura)
- [Fluxo de Trabalho](#-fluxo-de-trabalho)
- [Segurança](#-segurança)
- [Contribuição](#-contribuição)
- [Roadmap](#-roadmap)

---

## 🌐 Visão Geral

Solução Django para download de conteúdo de:
- **YouTube**: MP3 (128kbps) e MP4 (até 4K)
- **Facebook/Instagram**: MP4 (qualidade original)

**Recursos Principais**:
✅ Processamento assíncrono  
✅ Pré-visualização de vídeos  
✅ Auto-limpeza de arquivos  
✅ Interface responsiva  

---

## 🚀 Funcionalidades

| Plataforma   | Formatos Suportados | Resoluções          |
|--------------|---------------------|---------------------|
| YouTube      | MP3, MP4           | 144p a 4K           |
| Facebook     | MP4                | Original            |
| Instagram    | MP4                | Até 1080p           |

**Features Adicionais**:
- Seleção de qualidade manual
- Geração de thumbnail
- Tempo estimado de download
- Histórico de conversões

---

## 💻 Tecnologias

**Backend**:
- Python 3.10
- Django 4.2
- yt-dlp 2023.7.6
- Celery 5.3.1 (Redis broker)

**Frontend**:
- Bootstrap 5.3
- HTMX 1.9.4
- MediaElement.js

**Infra**:
- Nginx
- Docker
- PostgreSQL

---

## 📥 Instalação

### Pré-requisitos
- Python 3.8+
- FFmpeg
- Redis Server

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/GHFConverter.git
cd GHFConverter

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
nano .env  # Edite com suas credenciais

# Execute as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver
```
## 🏗 Arquitetura

sequenceDiagram
    participant Usuário
    participant Frontend
    participant Backend
    participant yt-dlp
    participant Armazenamento
    
    Usuário->>Frontend: Submete URL
    Frontend->>Backend: POST /api/process
    Backend->>yt-dlp: Extrai metadados
    yt-dlp-->>Backend: Retorna info
    Backend->>Frontend: Opções de download
    Usuário->>Frontend: Seleciona formato
    Frontend->>Backend: POST /api/download
    Backend->>Celery: Inicia task
    Celery->>yt-dlp: Processa download
    yt-dlp->>Armazenamento: Salva arquivo
    Backend-->>Frontend: Link temporário
    Frontend-->>Usuário: Download disponível

## 🔒 Segurança

**Medidas Implementadas:**
- Validação de URL com regex
- Sanitização de inputs
- Rate limiting (10 requests/min)
- Timeout de 5 minutos para downloads
- Arquivos temporários com hash SHA-256
- Exclusão automática após 24h

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch descritiva:
   > git checkout -b feat/nova-funcionalidade
3. Commit suas mudanças:
   > git commit -m "feat: Adiciona suporte ao Vimeo"
4. Push para a branch
   > git push origin feat/nova-funcionalidade
5. Abra um Pull Request  
