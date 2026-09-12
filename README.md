# Downloader Pessoal (YouTube / TikTok / Instagram)

Site protegido por senha, para uso pessoal via navegador (celular ou
qualquer dispositivo). Usa o [yt-dlp](https://github.com/yt-dlp/yt-dlp)
por baixo dos panos.

⚠️ **Uso pessoal apenas.** Mesmo hospedado, esse site é só seu — não
compartilhe a URL nem a senha com mais ninguém, e não redistribua o
conteúdo baixado. Baixar conteúdo dessas plataformas costuma
contrariar os Termos de Serviço delas.

## Arquivos do projeto

- `app.py` — backend Flask
- `templates/index.html` — página principal
- `templates/login.html` — tela de senha
- `Dockerfile` — para hospedar em qualquer plataforma que aceite Docker
- `requirements.txt` — dependências Python

## Deploy (recomendado: Railway)

O Railway detecta o Dockerfile automaticamente e cuida do ffmpeg pra
você. Passo a passo:

1. Crie um repositório no GitHub com esses arquivos (pode ser
   privado).
2. Crie uma conta em https://railway.app (dá para logar com GitHub).
3. "New Project" → "Deploy from GitHub repo" → selecione o repositório.
4. Em **Variables**, adicione:
   - `APP_PASSWORD` → escolha uma senha forte, só sua
   - `SECRET_KEY` → qualquer texto aleatório longo (ex: gere em
     https://randomkeygen.com)
5. O Railway builda a imagem Docker e te dá uma URL pública (algo como
   `seuapp.up.railway.app`).
6. Acesse essa URL pelo navegador do celular, digite a senha em
   `APP_PASSWORD` e use normalmente.

Alternativas equivalentes, mesmo processo (Dockerfile + variáveis de
ambiente): **Render.com** (Web Service → Docker) e **Fly.io**.

Evite hospedagem sem suporte a Docker (tipo PythonAnywhere free), pois
elas costumam bloquear as conexões que o yt-dlp precisa fazer.

## Rodando localmente (para testar antes de subir)

```
pip install -r requirements.txt
# instale o ffmpeg: brew install ffmpeg (mac) / apt install ffmpeg (linux) / ffmpeg.org (windows)
APP_PASSWORD=minhasenha SECRET_KEY=qualquercoisa python app.py
```
Abra http://127.0.0.1:5000, use a senha definida em `APP_PASSWORD`.

## Conteúdo privado ou com restrição (Instagram principalmente)

Se o host começar a ser bloqueado pelo Instagram/TikTok (IPs de
serviços de hospedagem levam bloqueio com mais frequência que uma
conexão residencial), exporte os cookies do seu navegador logado
(extensão "Get cookies.txt") e suba o arquivo como `cookies.txt` na
raiz do projeto (ou como secret file, dependendo da plataforma). O
app usa esse arquivo automaticamente se ele existir.

## Sobre marca d'água (TikTok)

O yt-dlp tenta pegar a versão sem marca d'água quando o TikTok
disponibiliza esse link internamente. Isso pode parar de funcionar de
vez em quando (o TikTok muda a API com frequência) — nesse caso,
atualize o yt-dlp no `requirements.txt` para a versão mais recente e
faça um novo deploy.

## Manutenção

De tempos em tempos, atualize a versão do yt-dlp no
`requirements.txt` e faça um novo deploy — essas plataformas mudam
constantemente e o yt-dlp recebe correções com frequência.
