from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import OpcoesRespostas, OpcoesRespostasCreate, OpcoesRespostasUpdate
import app.crud as crud

router = APIRouter(prefix="/opcoes-respostas", tags=["opcoes-respostas"])


@router.get("/pergunta/{pergunta_id}", response_model=List[OpcoesRespostas])
def listar_opcoes_resposta(pergunta_id: int, db: Session = Depends(get_db)):
    """Lista todas as opções de resposta de uma pergunta"""
    # Verificar se a pergunta existe
    pergunta = crud.get_pergunta(db, pergunta_id=pergunta_id)
    if pergunta is None:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    
    return crud.get_opcoes_resposta_by_pergunta(db, pergunta_id=pergunta_id)


@router.post("/pergunta/{pergunta_id}", response_model=OpcoesRespostas)
def criar_opcao_resposta(
    pergunta_id: int,
    opcao: OpcoesRespostasCreate,
    db: Session = Depends(get_db)
):
    """Cria uma nova opção de resposta para uma pergunta"""
    # Verificar se a pergunta existe
    pergunta = crud.get_pergunta(db, pergunta_id=pergunta_id)
    if pergunta is None:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    
    return crud.create_opcao_resposta(db=db, pergunta_id=pergunta_id, opcao=opcao)


@router.put("/{opcao_id}", response_model=OpcoesRespostas)
def atualizar_opcao_resposta(
    opcao_id: int,
    opcao: OpcoesRespostasUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza uma opção de resposta existente"""
    db_opcao = crud.update_opcao_resposta(db, opcao_id=opcao_id, opcao=opcao)
    if db_opcao is None:
        raise HTTPException(status_code=404, detail="Opção de resposta não encontrada")
    return db_opcao


@router.delete("/{opcao_id}")
def deletar_opcao_resposta(opcao_id: int, db: Session = Depends(get_db)):
    """Deleta uma opção de resposta"""
    db_opcao = crud.delete_opcao_resposta(db, opcao_id=opcao_id)
    if db_opcao is None:
        raise HTTPException(status_code=404, detail="Opção de resposta não encontrada")
    return {"message": "Opção de resposta deletada com sucesso"}
