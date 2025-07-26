from fastapi import FastAPI
from fastapi.responses import FileResponse
import CriarSpellCard
from Magias import Magia
from typing import List

app = FastAPI()

@app.post('/CriarCartas')
def create_cards(magias: List[Magia]):
    magias_dict = [m.dict() for m in magias]

    CriarSpellCard.gerar_cartas_para_lista(magias_dict)
    caminho_pdf = CriarSpellCard.gerar_pdf_com_fpdf()

    return FileResponse(
        path=caminho_pdf,
        filename="cartas_paladino.pdf",
        media_type='application/pdf'
    )