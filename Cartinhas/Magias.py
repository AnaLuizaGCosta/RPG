from pydantic import BaseModel
from typing import Optional

class Magia(BaseModel):
    nome: str
    nivel_tipo: str
    tempo: str
    alcance: str
    componentes: str
    duracao: str
    descricao: str
    classe: str
    cor: Optional[str] = None
    pagina_phb: Optional[int] = None