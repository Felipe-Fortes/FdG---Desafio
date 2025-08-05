from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import (
    Pergunta, PerguntaCreate, PerguntaUpdate, PerguntaFilter, TipoPerguntaEnum
)
import app.crud as crud

router = APIRouter(prefix="/perguntas", tags=["perguntas"])


@router.get("/formulario/{formulario_id}", response_model=List[Pergunta])
def listar_perguntas_formulario(
    formulario_id: int,
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(10, ge=1, le=100, description="Limite de registros por página"),
    order_by: str = Query("ordem", description="Campo para ordenação"),
    order_desc: bool = Query(False, description="Ordenação decrescente"),
    tipo_pergunta: Optional[TipoPerguntaEnum] = Query(None, description="Filtrar por tipo de pergunta"),
    obrigatoria: Optional[bool] = Query(None, description="Filtrar por obrigatoriedade"),
    sub_pergunta: Optional[bool] = Query(None, description="Filtrar por sub-pergunta"),
    db: Session = Depends(get_db)
):
    """
    Lista perguntas de um formulário específico com suporte a:
    - Filtros por tipo, obrigatoriedade, etc.
    - Ordenação
    - Paginação
    """
    # Verificar se o formulário existe
    formulario = crud.get_formulario(db, formulario_id=formulario_id)
    if formulario is None:
        raise HTTPException(status_code=404, detail="Formulário não encontrado")
    
    # Criar filtros
    filters = PerguntaFilter(
        tipo_pergunta=tipo_pergunta,
        obrigatoria=obrigatoria,
        sub_pergunta=sub_pergunta
    )
    
    perguntas = crud.get_perguntas_by_formulario(
        db,
        formulario_id=formulario_id,
        skip=skip,
        limit=limit,
        filters=filters,
        order_by=order_by,
        order_desc=order_desc
    )
    
    return perguntas


@router.get("/formulario/{formulario_id}/count")
def contar_perguntas_formulario(
    formulario_id: int,
    tipo_pergunta: Optional[TipoPerguntaEnum] = Query(None, description="Filtrar por tipo de pergunta"),
    obrigatoria: Optional[bool] = Query(None, description="Filtrar por obrigatoriedade"),
    sub_pergunta: Optional[bool] = Query(None, description="Filtrar por sub-pergunta"),
    db: Session = Depends(get_db)
):
    """Conta o número total de perguntas de um formulário com os filtros aplicados"""
    # Verificar se o formulário existe
    formulario = crud.get_formulario(db, formulario_id=formulario_id)
    if formulario is None:
        raise HTTPException(status_code=404, detail="Formulário não encontrado")
    
    # Criar filtros
    filters = PerguntaFilter(
        tipo_pergunta=tipo_pergunta,
        obrigatoria=obrigatoria,
        sub_pergunta=sub_pergunta
    )
    
    count = crud.count_perguntas_by_formulario(db, formulario_id=formulario_id, filters=filters)
    
    return {"total": count}


@router.get("/{pergunta_id}", response_model=Pergunta)
def obter_pergunta(pergunta_id: int, db: Session = Depends(get_db)):
    """Obtém uma pergunta específica por ID"""
    pergunta = crud.get_pergunta(db, pergunta_id=pergunta_id)
    if pergunta is None:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    return pergunta


@router.post("/", response_model=Pergunta)
def criar_pergunta(pergunta: PerguntaCreate, db: Session = Depends(get_db)):
    """Cria uma nova pergunta"""
    # Verificar se o formulário existe
    formulario = crud.get_formulario(db, formulario_id=pergunta.id_formulario)
    if formulario is None:
        raise HTTPException(status_code=404, detail="Formulário não encontrado")
    
    return crud.create_pergunta(db=db, pergunta=pergunta)


@router.put("/{pergunta_id}", response_model=Pergunta)
def atualizar_pergunta(
    pergunta_id: int,
    pergunta: PerguntaUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza uma pergunta existente"""
    db_pergunta = crud.update_pergunta(db, pergunta_id=pergunta_id, pergunta=pergunta)
    if db_pergunta is None:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    return db_pergunta


@router.delete("/{pergunta_id}")
def deletar_pergunta(pergunta_id: int, db: Session = Depends(get_db)):
    """Deleta uma pergunta"""
    db_pergunta = crud.delete_pergunta(db, pergunta_id=pergunta_id)
    if db_pergunta is None:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    return {"message": "Pergunta deletada com sucesso"}
