import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from rembg import remove
from io import BytesIO
import platform
import subprocess
import sys
import os

def recurso_absoluto(relativo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativo)
    return os.path.join(os.path.abspath("."), relativo)

TEMPLATE_PATH = recurso_absoluto("ficha_template.png")

PERSONAGEM_POS = (425, 315)
PERSONAGEM_SIZE = (450, 550)
SAIDA_IMAGEM = "ficha_final.png"


def abrir_imagem(caminho):
    sistema = platform.system()
    try:
        if sistema == "Windows":
            os.startfile(caminho)
        elif sistema == "Darwin":  # macOS
            subprocess.run(["open", caminho])
        else:  # Linux
            subprocess.run(["xdg-open", caminho])
    except Exception as e:
        print(f"Erro ao abrir imagem: {e}")


def gerar_ficha(imagem_personagem_path):
    ficha = Image.open(TEMPLATE_PATH).convert("RGBA")

    with open(imagem_personagem_path, 'rb') as f:
        input_image_bytes = f.read()
    output_image_bytes = remove(input_image_bytes)

    personagem = Image.open(BytesIO(output_image_bytes)).convert("RGBA")
    personagem = personagem.resize(PERSONAGEM_SIZE)
    ficha.paste(personagem, PERSONAGEM_POS, personagem)

    ficha.save(SAIDA_IMAGEM)

    # Mensagem de sucesso
    messagebox.showinfo("Concluído", "Ficha gerada com sucesso!")

    # Abre a imagem
    abrir_imagem(SAIDA_IMAGEM)


def selecionar_imagem():
    caminho = filedialog.askopenfilename(title="Selecione a imagem do personagem")
    if caminho:
        gerar_ficha(caminho)


# Criando interface
janela = tk.Tk()
janela.title("Gerador de Ficha RPG")
janela.geometry("320x100")

botao = tk.Button(janela, text="Selecionar imagem do personagem", command=selecionar_imagem)
botao.pack(pady=30)

janela.mainloop()
