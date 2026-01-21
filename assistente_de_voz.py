import os
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import openai
from gTTS import gTTS
import pygame
import time

# --- CONFIGURAÇÃO DE SEGURANÇA ---
# Se você tiver a chave no sistema, ele usa. Se não, usa o que você digitar aqui.
# PARA O GITHUB: DEIXE 'TODO'
os.environ['OPENAI_API_KEY'] = 'TODO' 
openai.api_key = os.environ.get('OPENAI_API_KEY')

def assistente_voz():
    idioma = 'pt'
    arquivo_audio = "usuario.wav"
    arquivo_resposta = "resposta.mp3"
    
    # 1. GRAVAÇÃO
    print("Ouvindo...")
    fs = 44100
    segundos = 5
    gravacao = sd.rec(int(segundos * fs), samplerate=fs, channels=1)
    sd.wait()
    write(arquivo_audio, fs, gravacao)

    # 2. TRANSCRIÇÃO (WHISPER)
    print("Traduzindo voz para texto...")
    modelo = whisper.load_model("small")
    # 
    resultado = modelo.transcribe(arquivo_audio, fp16=False, language=idioma)
    texto_usuario = resultado["text"]
    print(f"Você: {texto_usuario}")

    # 3. CHATGPT (OPENAI)
    if openai.api_key == 'TODO':
        print("ERRO: Você precisa de uma API Key para usar o GPT-4.")
        return

    print("Consultando GPT-4...")
    # 
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": texto_usuario}]
    )
    resposta_gpt = response.choices[0].message.content
    print(f"GPT: {resposta_gpt}")

    # 4. VOZ (gTTS)
    voz = gTTS(text=resposta_gpt, lang=idioma)
    voz.save(arquivo_resposta)

    # 5. REPRODUÇÃO LOCAL
    pygame.mixer.init()
    pygame.mixer.music.load(arquivo_resposta)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()

if __name__ == "__main__":
    assistente_voz()