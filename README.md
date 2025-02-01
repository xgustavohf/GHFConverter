# GHFConverter - Documentação Técnica

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-4.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-orange)

Aplicação web para download de vídeos e áudio de plataformas sociais com processamento assíncrono.

## Índice
1. [Visão Geral](#visão-geral)
2. [Funcionalidades](#funcionalidades)
3. [Tecnologias](#tecnologias)
4. [Instalação](#instalação)
5. [Arquitetura](#arquitetura)
6. [Fluxo de Trabalho](#fluxo-de-trabalho)
7. [Segurança e Otimização](#segurança-e-otimização)
8. [Tratamento de Erros](#tratamento-de-erros)
9. [Contribuição](#contribuição)
10. [Roadmap](#roadmap)

---

## Visão Geral <a name="visão-geral"></a>

Solução Django para download de conteúdo multimídia de:
- **YouTube**: MP3 (áudio) e MP4 (vídeo)
- **Facebook/Instagram**: MP4 (vídeo apenas)

**Objetivo Principal**: Fornecer interface intuitiva para conversão de mídias online com:
- Processamento em segundo plano
- Gerenciamento automatizado de arquivos
- Suporte multiplataforma

---

## Funcionalidades <a name="funcionalidades"></a>

| Funcionalidade       | Descrição                                  | Plataformas Suportadas       |
|----------------------|--------------------------------------------|------------------------------|
| Download MP4         | Vídeo em diversas resoluções              | YouTube, Facebook, Instagram |
| Download MP3         | Áudio em qualidade 128kbps                | YouTube                      |
| Pré-visualização     | Exibe título, thumbnail e duração         | Todas as plataformas         |
| Filas Assíncronas    | Processamento não-bloqueante usando threads | -                           |
| Auto-limpeza         | Remove arquivos após 24 horas             | -                           |

---

## Tecnologias <a name="tecnologias"></a>

### Backend
- Python 3.8+
- Django 4.0+
- yt-dlp (wrapper do youtube-dl)
- Celery (opcional para tarefas assíncronas)

### Frontend
- Bootstrap 5
- HTML5 Media APIs
- JavaScript Fetch API

### Armazenamento
- Sistema de arquivos local
- Configurável para AWS S3

---

## Instalação <a name="instalação"></a>

```bash
# Clonar repositório
git clone https://github.com/seu-usuario/GHFConverter.git
cd GHFConverter

# Ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar ambiente
cp .env.example .env
# Editar .env com suas credenciais

# Migrações
python manage.py migrate

# Executar
python manage.py runserver
