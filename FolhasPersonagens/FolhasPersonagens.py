from PIL import Image, ImageDraw
import os

# --- CONFIGURAÇÕES INICIAIS ---
# Caminho do template da ficha
TEMPLATE_PATH = "ficha_template.png"  # Renomeie o arquivo do template com esse nome

# Coordenadas aproximadas dos testes de resistência (FOR, DES, etc.)
resistencia_coords = {
    "FOR": (37, 338),
    "DES": (88, 338),
    "CON": (139, 338),
    "INT": (190, 338),
    "SAB": (240, 338),
    "CAR": (290, 338)
}

# Coordenadas aproximadas das perícias
pericia_coords = {
    "Acrobacia": (16, 508),
    "Arcanismo": (16, 527),
    "Atletismo": (16, 546),
    "Atuação": (16, 564),
    "Blefar": (16, 582),
    "Furtividade": (16, 600),
    "História": (16, 618),
    "Intimidação": (16, 636),
    "Intuição": (16, 655),
    "Investigação": (16, 673),
    "Lidar com Animais": (16, 692),
    "Medicina": (16, 710),
    "Natureza": (16, 730),
    "Percepção": (16, 748),
    "Persuasão": (16, 766),
    "Prestidigitação": (16, 785),
    "Religião": (16, 803),
    "Sobrevivência": (16, 822)
}

# Coordenadas do centro do círculo do personagem
PERSONAGEM_POS = (425, 315)  # canto superior esquerdo
PERSONAGEM_SIZE = (450, 550)


# --- FUNÇÃO PRINCIPAL ---
def gerar_ficha(imagem_personagem_path, pericias, resistencias, saida="ficha_final.png"):
    # Carrega o template da ficha
    ficha = Image.open(TEMPLATE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(ficha)

    # Insere imagem do personagem
    personagem = Image.open(imagem_personagem_path).convert("RGBA")
    personagem = personagem.resize(PERSONAGEM_SIZE)
    ficha.paste(personagem, PERSONAGEM_POS, personagem)

    # Desenha bolinhas pretas nos testes de resistência
    for nome, marcado in resistencias.items():
        if marcado and nome in resistencia_coords:
            x, y = resistencia_coords[nome]
            draw.ellipse((x-6, y-6, x+6, y+6), fill="black")

    # Desenha bolinhas pretas nas perícias
    for nome, marcado in pericias.items():
        if marcado and nome in pericia_coords:
            x, y = pericia_coords[nome]
            draw.ellipse((x-6, y-6, x+6, y+6), fill="black")

    # Salva a imagem final
    ficha.save(saida)
    print(f"Ficha gerada e salva como: {saida}")


# --- EXEMPLO DE USO ---
if __name__ == "__main__":
    # Caminho da imagem do personagem fornecida pelo usuário
    imagem_personagem = input("Caminho da imagem do personagem (ex: personagem.png): ")

    # Exemplo de dicionário com perícias marcadas
    pericias_marcadas = {
        "Acrobacia": True,
        "Arcanismo": True,
        "Atletismo": True,
        "Atuação": True,
        "Blefar": True,
        "Furtividade": True,
        "História": True,
        "Intimidação": True,
        "Intuição": True,
        "Investigação": True,
        "Lidar com Animais": True,
        "Medicina": True,
        "Natureza": True,
        "Percepção": True,
        "Persuasão": True,
        "Prestidigitação": True,
        "Religião": True,
        "Sobrevivência": True
    }

    # Exemplo de dicionário com resistências marcadas
    resistencias_marcadas = {
        "FOR": True,
        "DES": True,
        "CON": True,
        "INT": True,
        "SAB": True,
        "CAR": True
    }

    gerar_ficha(imagem_personagem, pericias_marcadas, resistencias_marcadas)
