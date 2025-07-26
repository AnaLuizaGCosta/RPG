from enum import Enum

class CorClasse(Enum):
    PALADINO = "#3A6FA9"   # Azul
    CLERIGO = "#D5A021"    # Amarelo
    BRUXO = "#3F2B63"      # Roxo escuro
    MAGO = "#1B5E9E"       # Azul petróleo
    DRUIDA = "#4C9B47"     # Verde
    BARDO = "#B74B9C"      # Rosa escuro
    GUERREIRO = "#A32C2C"  # Vermelho escuro
    LADINO = "#333333"     # Cinza
    FEITICEIRO = "#660099" # Violeta
    PATRULHEIRO = "#2C6E49" # Verde escuro
    MONJE = "#C87C41"      # Marrom claro

    @staticmethod
    def cor_para(classe_nome):
        classe_maiuscula = classe_nome.upper().replace("Í", "I").replace("É", "E")
        return CorClasse.__members__.get(classe_maiuscula, "#3A6FA9")  # padrão: azul
