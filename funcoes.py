from datetime import datetime, timezone, timedelta
import requests
import locale
import pygame

def converter_hora_string(hora):
    hora_convertida = datetime.strptime(hora, "%H:%M").time()
    return hora_convertida

def acessar_hora_web():
    try:
        resposta = requests.get("https://time.google.com", timeout=5)
        if resposta.status_code == 200: #Verifica se houve uma resposta válida e há comunicação
            hora = datetime.fromisoformat(resposta.text)
            return hora
    except Exception as ex:
        pass #Não faz nada
    return None

def acessar_data():
    data_atual = datetime.now()
    data_formatada = data_atual.strftime("%d%m%Y")
    return data_formatada

def converter_para_padrao_brasil(data_hora):
    data_mysql = datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
    data_brasil = data_mysql.strftime("%d/%m/%Y %H:%M:%S")
    return data_brasil

def tocar_som(caminho):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except pygame.error as e:
        print("Erro ao reproduzir o MP3:", e)

    finally:
        pygame.quit()
