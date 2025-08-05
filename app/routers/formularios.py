from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import (
    Formulario, FormularioCreate, FormularioUpdate, FormularioSummary
)
import app.crud as crud

router = APIRouter(prefix="/formularios", tags=["formularios"])


@router.get("/", response_model=List[FormularioSummary])
def listar_formularios(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(10, ge=1, le=100, description="Limite de registros por página"),
    db: Session = Depends(get_db)
):
    """Lista todos os formulários com paginação"""
    formularios = crud.get_formularios(db, skip=skip, limit=limit)
    return formularios


@router.get("/{formulario_id}", response_model=Formulario)
def obter_formulario(formulario_id: int, db: Session = Depends(get_db)):
    """Obtém um formulário específico por ID"""
    formulario = crud.get_formulario(db, formulario_id=formulario_id)
    if formulario is None:
        raise HTTPException(status_code=404, detail="Formulário não encontrado")
    return formulario


@router.post("/", response_model=Formulario)
def criar_formulario(formulario: FormularioCreate, db: Session = Depends(get_db)):
    """Cria um novo formulário"""
    return crud.create_formulario(db=db, formulario=formulario)


@router.put("/{formulario_id}", response_model=Formulario)
def atualizar_formulario(
    formulario_id: int,
    formulario: FormularioUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um formulário existente"""
    db_formulario = crud.update_formulario(db, formulario_id=formulario_id, formulario=formulario)
    if db_formulario is None:
        raise HTTPException(status_code=404, detail="Formulário não encontrado")
    return db_formulario


@router.delete("/{formulario_id}")
def deletar_formulario(formulario_id: int, db: Session = Depends(get_db)):
    """Deleta um formulário"""
    db_formulario = crud.delete_formulario(db, formulario_id=formulario_id)
    if db_formulario is None:
        raise HTTPException(status_code=404, detail="Formulário não encontrado")
    return {"message": "Formulário deletado com sucesso"}
