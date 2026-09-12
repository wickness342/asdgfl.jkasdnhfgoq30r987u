import os
import uuid
import subprocess
from functools import wraps
from pathlib import Path
from flask import (
    Flask, request, render_template, send_file, jsonify,
    session, redirect, url_for
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "troque-esta-chave-antes-de-usar")

# Senha de acesso ao site. Em produção, defina isso como variável de
# ambiente APP_PASSWORD na plataforma de hospedagem — não deixe o
# valor padrão abaixo.
APP_PASSWORD = os.environ.get("APP_PASSWORD", "changeme")

BASE_DIR = Path(__file__).parent
DOWNLOAD_DIR = BASE_DIR / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

COOKIES_FILE = BASE_DIR / "cookies.txt"


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == APP_PASSWORD:
            session["logged_in"] = True
            session.permanent = True
            return redirect(url_for("index"))
        error = "Senha incorreta."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
@login_required
def download():
    url = request.form.get("url", "").strip()
    mode = request.form.get("mode", "video")  # "video" ou "audio"

    if not url:
        return jsonify({"error": "Informe uma URL."}), 400

    job_id = uuid.uuid4().hex[:10]
    output_template = str(DOWNLOAD_DIR / f"{job_id}.%(ext)s")

    cmd = [
        "yt-dlp",
        url,
        "-o", output_template,
        "--no-playlist",
    ]

    if mode == "audio":
        cmd += ["-x", "--audio-format", "mp3", "--audio-quality", "0"]
    else:
        cmd += ["-f", "bestvideo+bestaudio/best", "--merge-output-format", "mp4"]

    if COOKIES_FILE.exists():
        cmd += ["--cookies", str(COOKIES_FILE)]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=900)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Falha ao baixar:\n{e.stderr[-1500:]}"}), 500
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Tempo excedido ao baixar."}), 500
    except FileNotFoundError:
        return jsonify({
            "error": "yt-dlp não encontrado. Verifique se está no requirements.txt"
        }), 500

    matches = sorted(DOWNLOAD_DIR.glob(f"{job_id}.*"))
    if not matches:
        return jsonify({"error": "Download concluído mas arquivo não localizado."}), 500

    file_path = matches[-1]
    response = send_file(file_path, as_attachment=True, download_name=file_path.name)

    # Limpa o arquivo do servidor depois de enviado, para não acumular
    # espaço em disco no host (a maioria dos planos gratuitos é pequena).
    @response.call_on_close
    def cleanup():
        try:
            file_path.unlink(missing_ok=True)
        except Exception:
            pass

    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
