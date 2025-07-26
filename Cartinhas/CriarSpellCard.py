from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from fpdf import FPDF

from CorClasse import CorClasse


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if draw.textlength(test_line, font=font) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def gerar_cartinha(magia):
    cor_principal = CorClasse.cor_para(magia["classe"]).value
    cor_texto = "black"

    largura, altura = 744, 1039
    img = Image.new("RGBA", (largura, altura), color=cor_principal)
    draw = ImageDraw.Draw(img)

    try:
        fonte_titulo = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
        fonte_sub = ImageFont.truetype("DejaVuSans.ttf", 22)
        fonte_texto = ImageFont.truetype("DejaVuSans.ttf", 20)
        fonte_negrito = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
    except:
        fonte_titulo = fonte_sub = fonte_texto = fonte_negrito = ImageFont.load_default()

    border_radius = 40
    mask = Image.new("L", (largura, altura), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, largura, altura], radius=border_radius, fill=255)

    # Bordas laterais azuis
    draw.rectangle([0, 0, 30, altura], fill=cor_principal)
    draw.rectangle([largura - 30, 0, largura, altura], fill=cor_principal)

    # Cabeçalho azul
    draw.rectangle([30, 0, largura - 30, 130], fill=cor_principal)
    draw.text((50, 20), magia["nome"], font=fonte_titulo, fill="white")
    draw.text((50, 80), magia["nivel_tipo"], font=fonte_sub, fill="white")

    box_y = 130
    box_height = 100
    col_width = (largura - 60) // 2

    # Campos principais (quebrando retângulo branco indesejado)
    # Apenas os quadros brancos individuais serão desenhados abaixo

    draw.rounded_rectangle([30, box_y, 30 + col_width, box_y + box_height], radius=15, outline=cor_principal, width=3, fill="white")
    draw.rounded_rectangle([30 + col_width, box_y, largura - 30, box_y + box_height], radius=15, outline=cor_principal, width=3, fill="white")
    draw.rounded_rectangle([30, box_y + box_height, 30 + col_width, box_y + 2 * box_height], radius=15, outline=cor_principal, width=3, fill="white")
    draw.rounded_rectangle([30 + col_width, box_y + box_height, largura - 30, box_y + 2 * box_height], radius=15, outline=cor_principal, width=3, fill="white")

    draw.text((40, box_y + 10), "TEMPO DE CON.", font=fonte_sub, fill=cor_principal)
    draw.text((40, box_y + 40), magia["tempo"], font=fonte_texto, fill=cor_texto)
    draw.text((40 + col_width, box_y + 10), "ALCANCE", font=fonte_sub, fill=cor_principal)
    draw.text((40 + col_width, box_y + 40), magia["alcance"], font=fonte_texto, fill=cor_texto)

    draw.text((40, box_y + box_height + 10), "COMPONENTES", font=fonte_sub, fill=cor_principal)
    componentes_lines = wrap_text(draw, magia["componentes"], fonte_texto, col_width - 20)
    for i, line in enumerate(componentes_lines):
        draw.text((40, box_y + box_height + 40 + i * 22), line, font=fonte_texto, fill=cor_texto)

    draw.text((40 + col_width, box_y + box_height + 10), "DURAÇÃO", font=fonte_sub, fill=cor_principal)
    draw.text((40 + col_width, box_y + box_height + 40), magia["duracao"], font=fonte_texto, fill=cor_texto)

    # Fundo branco arredondado para a descrição
    desc_y = box_y + 2 * box_height + 30
    desc_bottom = altura - 60  # até o rodapé
    draw.rounded_rectangle(
        [30, desc_y - 20, largura - 30, desc_bottom - 10],
        radius=30,
        fill="white"
    )

    # Parâmetros de texto
    max_desc_height = 730
    linha_altura = fonte_texto.getbbox("Ag")[3] + 6
    descricao = magia["descricao"]

    if ":" in descricao:
        parte_negrito, parte_normal = descricao.split(":", 1)
        parte_negrito += ":"
        draw.text((40, desc_y), parte_negrito.strip(), font=fonte_negrito, fill=cor_texto)
        negrito_largura = draw.textlength(parte_negrito.strip(), font=fonte_negrito) + 5

        largura_disponivel = largura - 60 - negrito_largura
        palavras = parte_normal.strip().split()
        linha_atual = ""
        linhas_descricao = []
        for palavra in palavras:
            teste = linha_atual + (" " if linha_atual else "") + palavra
            if draw.textlength(teste, font=fonte_texto) <= largura_disponivel:
                linha_atual = teste
            else:
                linhas_descricao.append(linha_atual)
                linha_atual = palavra
        if linha_atual:
            linhas_descricao.append(linha_atual)

        draw.text((40 + negrito_largura, desc_y), linhas_descricao[0], font=fonte_texto, fill=cor_texto)

        for i in range(1, len(linhas_descricao)):
            y_linha = desc_y + i * linha_altura
            if y_linha > max_desc_height:
                break
            draw.text((40, y_linha), linhas_descricao[i], font=fonte_texto, fill=cor_texto)
    else:
        linhas = textwrap.wrap(descricao, width=70)
        for i, linha in enumerate(linhas):
            y = desc_y + i * linha_altura
            if y > max_desc_height:
                break
            draw.text((40, y), linha, font=fonte_texto, fill=cor_texto)

    # Rodapé
    rodape_y = altura - 60
    draw.rectangle([30, rodape_y, largura - 30, altura], fill=cor_principal)
    draw.text((50, rodape_y + 10), magia["classe"].upper(), font=fonte_sub, fill="white")

    img.putalpha(mask)
    return img

def gerar_cartas_para_lista(magias, pasta_saida="cartas_magia"):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    for magia in magias:
        imagem = gerar_cartinha(magia)
        nome_arquivo = magia['nome'].lower().replace(" ", "_") + ".png"
        imagem.save(os.path.join(pasta_saida, nome_arquivo))

def gerar_pdf_com_fpdf(pasta_imagens="cartas_magia", nome_arquivo="cartas_paladino.pdf"):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(False)

    cartas = sorted([f for f in os.listdir(pasta_imagens) if f.endswith(".png")])

    largura_carta = 62  # ⬅️ AJUSTADO
    altura_carta = 95
    margem_x = 5         # ⬅️ AJUSTADO
    margem_y = 10
    espacamento_x = 6    # ⬅️ AJUSTADO
    espacamento_y = 5

    colunas = 3
    linhas = 2
    por_pagina = colunas * linhas

    for i, nome_carta in enumerate(cartas):
        if i % por_pagina == 0:
            pdf.add_page()

        coluna = i % colunas
        linha = (i % por_pagina) // colunas

        x = margem_x + coluna * (largura_carta + espacamento_x)
        y = margem_y + linha * (altura_carta + espacamento_y)

        caminho = os.path.join(pasta_imagens, nome_carta)
        pdf.image(caminho, x=x, y=y, w=largura_carta, h=altura_carta)

    pdf.output(nome_arquivo)
    print(f"PDF gerado com sucesso: {nome_arquivo}")
    return nome_arquivo
