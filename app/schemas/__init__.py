from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class TipoPerguntaEnum(str, Enum):
    SIM_NAO = "Sim_Nao"
    MULTIPLA_ESCOLHA = "multipla_escolha"
    UNICA_ESCOLHA = "unica_escolha"
    TEXTO_LIVRE = "texto_livre"
    INTEIRO = "Inteiro"
    NUMERO_DECIMAL = "Numero com duas casa decimais"


# Schemas para OpcoesRespostas
class OpcoesRespostasBase(BaseModel):
    resposta: str
    ordem: int
    resposta_aberta: bool = False


class OpcoesRespostasCreate(OpcoesRespostasBase):
    pass


class OpcoesRespostasUpdate(BaseModel):
    resposta: Optional[str] = None
    ordem: Optional[int] = None
    resposta_aberta: Optional[bool] = None


class OpcoesRespostas(OpcoesRespostasBase):
    id: int
    id_pergunta: int

    class Config:
        from_attributes = True


# Schemas para Pergunta
class PerguntaBase(BaseModel):
    titulo: str
    codigo: str
    orientacao_resposta: Optional[str] = None
    ordem: int
    obrigatoria: bool = False
    sub_pergunta: bool = False
    tipo_pergunta: TipoPerguntaEnum


class PerguntaCreate(PerguntaBase):
    id_formulario: int
    opcoes_respostas: Optional[List[OpcoesRespostasCreate]] = []


class PerguntaUpdate(BaseModel):
    titulo: Optional[str] = None
    codigo: Optional[str] = None
    orientacao_resposta: Optional[str] = None
    ordem: Optional[int] = None
    obrigatoria: Optional[bool] = None
    sub_pergunta: Optional[bool] = None
    tipo_pergunta: Optional[TipoPerguntaEnum] = None


class Pergunta(PerguntaBase):
    id: int
    id_formulario: int
    opcoes_respostas: List[OpcoesRespostas] = []

    class Config:
        from_attributes = True


# Schemas para Formulario
class FormularioBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    ordem: int


class FormularioCreate(FormularioBase):
    pass


class FormularioUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    ordem: Optional[int] = None


class Formulario(FormularioBase):
    id: int
    perguntas: List[Pergunta] = []

    class Config:
        from_attributes = True


class FormularioSummary(FormularioBase):
    id: int

    class Config:
        from_attributes = True


# Schemas para filtros e paginação
class PerguntaFilter(BaseModel):
    tipo_pergunta: Optional[TipoPerguntaEnum] = None
    obrigatoria: Optional[bool] = None
    sub_pergunta: Optional[bool] = None


class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 10
    order_by: str = "ordem"
    order_desc: bool = False
