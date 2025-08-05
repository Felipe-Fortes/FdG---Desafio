from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Formulario(Base):
    __tablename__ = "formulario"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column("descrição", Text)  # Mapear para coluna com ç no banco
    ordem = Column(Integer, nullable=False)
    
    # Relacionamento com perguntas
    perguntas = relationship("Pergunta", back_populates="formulario", cascade="all, delete-orphan")


class Pergunta(Base):
    __tablename__ = "pergunta"
    
    id = Column(Integer, primary_key=True, index=True)
    id_formulario = Column(Integer, ForeignKey("formulario.id"), nullable=False)
    titulo = Column(String(255), nullable=False)
    codigo = Column(String(100), nullable=False, unique=True)
    orientacao_resposta = Column(Text)
    ordem = Column(Integer, nullable=False)
    obrigatoria = Column(Boolean, default=False)
    sub_pergunta = Column(Boolean, default=False)
    tipo_pergunta = Column(String(50), nullable=False)  # Sim_Nao, multipla_escolha, unica_escolha, texto_livre, Inteiro, Numero com duas casa decimais
    
    # Relacionamentos
    formulario = relationship("Formulario", back_populates="perguntas")
    opcoes_resposta_pergunta = relationship("OpcoesRespostaPergunta", back_populates="pergunta", cascade="all, delete-orphan")
    opcoes_respostas = relationship("OpcoesRespostas", back_populates="pergunta", cascade="all, delete-orphan")


class OpcoesRespostaPergunta(Base):
    __tablename__ = "opcoes_resposta_pergunta"
    
    id = Column(Integer, primary_key=True, index=True)
    id_opcao_resposta = Column(Integer, ForeignKey("opcoes_respostas.id"), nullable=False)
    id_pergunta = Column(Integer, ForeignKey("pergunta.id"), nullable=False)
    
    # Relacionamentos
    pergunta = relationship("Pergunta", back_populates="opcoes_resposta_pergunta")
    opcao_resposta = relationship("OpcoesRespostas", back_populates="opcoes_resposta_pergunta")


class OpcoesRespostas(Base):
    __tablename__ = "opcoes_respostas"
    
    id = Column(Integer, primary_key=True, index=True)
    id_pergunta = Column(Integer, ForeignKey("pergunta.id"), nullable=False)
    resposta = Column(Text, nullable=False)
    ordem = Column(Integer, nullable=False)
    resposta_aberta = Column(Boolean, default=False)
    
    # Relacionamentos
    pergunta = relationship("Pergunta", back_populates="opcoes_respostas")
    opcoes_resposta_pergunta = relationship("OpcoesRespostaPergunta", back_populates="opcao_resposta", cascade="all, delete-orphan")
