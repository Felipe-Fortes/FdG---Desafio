from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import List, Optional
from app.models import Formulario, Pergunta, OpcoesRespostas
from app.schemas import (
    FormularioCreate, FormularioUpdate,
    PerguntaCreate, PerguntaUpdate, PerguntaFilter,
    OpcoesRespostasCreate, OpcoesRespostasUpdate,
    TipoPerguntaEnum
)


# CRUD para Formulario
def get_formulario(db: Session, formulario_id: int):
    return db.query(Formulario).filter(Formulario.id == formulario_id).first()


def get_formularios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Formulario).offset(skip).limit(limit).all()


def create_formulario(db: Session, formulario: FormularioCreate):
    db_formulario = Formulario(**formulario.dict())
    db.add(db_formulario)
    db.commit()
    db.refresh(db_formulario)
    return db_formulario


def update_formulario(db: Session, formulario_id: int, formulario: FormularioUpdate):
    db_formulario = db.query(Formulario).filter(Formulario.id == formulario_id).first()
    if db_formulario:
        update_data = formulario.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_formulario, field, value)
        db.commit()
        db.refresh(db_formulario)
    return db_formulario


def delete_formulario(db: Session, formulario_id: int):
    db_formulario = db.query(Formulario).filter(Formulario.id == formulario_id).first()
    if db_formulario:
        db.delete(db_formulario)
        db.commit()
    return db_formulario


# CRUD para Pergunta
def get_pergunta(db: Session, pergunta_id: int):
    return db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()


def get_perguntas_by_formulario(
    db: Session,
    formulario_id: int,
    skip: int = 0,
    limit: int = 10,
    filters: Optional[PerguntaFilter] = None,
    order_by: str = "ordem",
    order_desc: bool = False
):
    query = db.query(Pergunta).filter(Pergunta.id_formulario == formulario_id)
    
    # Aplicar filtros
    if filters:
        if filters.tipo_pergunta:
            query = query.filter(Pergunta.tipo_pergunta == filters.tipo_pergunta.value)
        if filters.obrigatoria is not None:
            query = query.filter(Pergunta.obrigatoria == filters.obrigatoria)
        if filters.sub_pergunta is not None:
            query = query.filter(Pergunta.sub_pergunta == filters.sub_pergunta)
    
    # Aplicar ordenação
    if hasattr(Pergunta, order_by):
        order_column = getattr(Pergunta, order_by)
        if order_desc:
            query = query.order_by(desc(order_column))
        else:
            query = query.order_by(asc(order_column))
    
    return query.offset(skip).limit(limit).all()


def count_perguntas_by_formulario(
    db: Session,
    formulario_id: int,
    filters: Optional[PerguntaFilter] = None
):
    query = db.query(Pergunta).filter(Pergunta.id_formulario == formulario_id)
    
    # Aplicar filtros
    if filters:
        if filters.tipo_pergunta:
            query = query.filter(Pergunta.tipo_pergunta == filters.tipo_pergunta.value)
        if filters.obrigatoria is not None:
            query = query.filter(Pergunta.obrigatoria == filters.obrigatoria)
        if filters.sub_pergunta is not None:
            query = query.filter(Pergunta.sub_pergunta == filters.sub_pergunta)
    
    return query.count()


def create_pergunta(db: Session, pergunta: PerguntaCreate):
    # Criar pergunta
    pergunta_data = pergunta.dict(exclude={"opcoes_respostas"})
    db_pergunta = Pergunta(**pergunta_data)
    db.add(db_pergunta)
    db.commit()
    db.refresh(db_pergunta)
    
    # Criar opções de resposta se fornecidas
    if pergunta.opcoes_respostas:
        for opcao in pergunta.opcoes_respostas:
            db_opcao = OpcoesRespostas(
                id_pergunta=db_pergunta.id,
                **opcao.dict()
            )
            db.add(db_opcao)
        db.commit()
        db.refresh(db_pergunta)
    
    return db_pergunta


def update_pergunta(db: Session, pergunta_id: int, pergunta: PerguntaUpdate):
    db_pergunta = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
    if db_pergunta:
        update_data = pergunta.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_pergunta, field, value)
        db.commit()
        db.refresh(db_pergunta)
    return db_pergunta


def delete_pergunta(db: Session, pergunta_id: int):
    db_pergunta = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
    if db_pergunta:
        db.delete(db_pergunta)
        db.commit()
    return db_pergunta


# CRUD para OpcoesRespostas
def get_opcoes_resposta_by_pergunta(db: Session, pergunta_id: int):
    return db.query(OpcoesRespostas).filter(OpcoesRespostas.id_pergunta == pergunta_id).all()


def create_opcao_resposta(db: Session, pergunta_id: int, opcao: OpcoesRespostasCreate):
    db_opcao = OpcoesRespostas(id_pergunta=pergunta_id, **opcao.dict())
    db.add(db_opcao)
    db.commit()
    db.refresh(db_opcao)
    return db_opcao


def update_opcao_resposta(db: Session, opcao_id: int, opcao: OpcoesRespostasUpdate):
    db_opcao = db.query(OpcoesRespostas).filter(OpcoesRespostas.id == opcao_id).first()
    if db_opcao:
        update_data = opcao.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_opcao, field, value)
        db.commit()
        db.refresh(db_opcao)
    return db_opcao


def delete_opcao_resposta(db: Session, opcao_id: int):
    db_opcao = db.query(OpcoesRespostas).filter(OpcoesRespostas.id == opcao_id).first()
    if db_opcao:
        db.delete(db_opcao)
        db.commit()
    return db_opcao
