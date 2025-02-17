import os
import sys
# from pytube import YouTube
from pytubefix import YouTube
import requests

def main():
    # Solicita a URL do vídeo
    url = input("Digite a URL do vídeo do YouTube: ")
    
    # Valores de visitorData e po_token
    visitor_data = ""
    po_token = ""

    # Configura os cabeçalhos da solicitação
    headers = {
        "visitorData": visitor_data,
        "po_token": po_token
    }

    # Tenta criar o objeto YouTube
    try:
        yt = YouTube(url, use_po_token=True)
        yt.request = requests.Session()
        yt.request.headers.update(headers)
    except Exception as e:
        print("Erro ao conectar ao YouTube:", e)
        sys.exit(1)

    print("Título:", yt.title)

    # Seleciona a melhor stream de vídeo (apenas vídeo) em mp4
    video_stream = yt.streams.filter(adaptive=True, mime_type="video/mp4")\
                             .order_by("resolution")\
                             .desc()\
                             .first()

    # Seleciona a melhor stream de áudio
    audio_stream = yt.streams.filter(only_audio=True, mime_type="audio/mp4")\
                             .order_by("abr")\
                             .desc()\
                             .first()

    if not video_stream or not audio_stream:
        print("Não foi possível encontrar streams adequadas para vídeo e áudio.")
        sys.exit(1)

    # Baixa o vídeo
    print(f"Baixando vídeo em {video_stream.resolution}...")
    try:
        video_file = video_stream.download(filename_prefix="video_")
    except Exception as e:
        print("Erro ao baixar o vídeo:", e)
        sys.exit(1)

    # Baixa o áudio
    print("Baixando áudio...")
    try:
        audio_file = audio_stream.download(filename_prefix="audio_")
    except Exception as e:
        print("Erro ao baixar o áudio:", e)
        sys.exit(1)

    # Cria um nome seguro para o arquivo final (remove caracteres problemáticos)
    safe_title = "".join(c for c in yt.title if c.isalnum() or c in " ._-")
    merged_file = f"{safe_title}.mp4"

    # Mescla vídeo e áudio utilizando ffmpeg (certifique-se que o ffmpeg está no PATH)
    print("Mesclando vídeo e áudio com ffmpeg...")
    merge_command = f'ffmpeg -y -i "{video_file}" -i "{audio_file}" -c copy "{merged_file}"'
    result = os.system(merge_command)
    if result != 0:
        print("Erro ao mesclar os arquivos com ffmpeg.")
        sys.exit(1)
    
    print("Download concluído!")
    print("Arquivo final:", merged_file)

if __name__ == "__main__":
    main()
