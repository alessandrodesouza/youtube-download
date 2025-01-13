from pytubefix import YouTube

def download(url, caminho_destino="."):
    try:
        # Cria o objeto YouTube
        yt = YouTube(url)

        # Seleciona o stream com a maior resolução
        video_stream = yt.streams.get_highest_resolution()
        # video_stream = yt.streams[2]

        print(f"Baixando: {yt.title}")
        print(f"Resolução: {video_stream.resolution}")
        
        # Faz o download do vídeo
        video_stream.download(output_path=caminho_destino)
        
        print("Download concluído!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# URL do vídeo do YouTube
url_video = input("Digite a URL do vídeo do YouTube: ")

# Caminho onde o vídeo será salvo (padrão: pasta atual)
caminho = input("Digite o caminho para salvar o vídeo (ou pressione Enter para salvar na pasta atual): ")

# Faz o download
download(url_video, caminho or ".")
