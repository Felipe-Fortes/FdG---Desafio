"""
Script para inicializar o banco de dados com tabelas e dados de exemplo
"""
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base, SessionLocal
from app.models import Formulario, Pergunta, OpcoesRespostas


def create_tables():
    """Cria todas as tabelas no banco de dados"""
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")


def create_sample_data():
    """Cria dados de exemplo no banco"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem dados
        existing_formulario = db.query(Formulario).first()
        if existing_formulario:
            print("Dados de exemplo já existem no banco.")
            return
        
        print("Criando dados de exemplo...")
        
        # Criar formulário de exemplo
        formulario = Formulario(
            titulo="Formulário de Cadastro",
            descricao="Formulário para cadastro de usuários",
            ordem=1
        )
        db.add(formulario)
        db.commit()
        db.refresh(formulario)
        
        # Criar perguntas de exemplo
        perguntas_exemplo = [
            {
                "titulo": "Nome completo",
                "codigo": "nome_completo",
                "orientacao_resposta": "Digite seu nome completo",
                "ordem": 1,
                "obrigatoria": True,
                "sub_pergunta": False,
                "tipo_pergunta": "texto_livre"
            },
            {
                "titulo": "Idade",
                "codigo": "idade",
                "orientacao_resposta": "Digite sua idade em anos",
                "ordem": 2,
                "obrigatoria": True,
                "sub_pergunta": False,
                "tipo_pergunta": "Inteiro"
            },
            {
                "titulo": "Gênero",
                "codigo": "genero",
                "orientacao_resposta": "Selecione seu gênero",
                "ordem": 3,
                "obrigatoria": True,
                "sub_pergunta": False,
                "tipo_pergunta": "unica_escolha"
            },
            {
                "titulo": "Possui experiência em programação?",
                "codigo": "experiencia_programacao",
                "orientacao_resposta": "Informe se possui experiência",
                "ordem": 4,
                "obrigatoria": True,
                "sub_pergunta": False,
                "tipo_pergunta": "Sim_Nao"
            }
        ]
        
        for pergunta_data in perguntas_exemplo:
            pergunta = Pergunta(
                id_formulario=formulario.id,
                **pergunta_data
            )
            db.add(pergunta)
            db.commit()
            db.refresh(pergunta)
            
            # Adicionar opções para pergunta de gênero
            if pergunta.codigo == "genero":
                opcoes = [
                    {"resposta": "Masculino", "ordem": 1, "resposta_aberta": False},
                    {"resposta": "Feminino", "ordem": 2, "resposta_aberta": False},
                    {"resposta": "Não binário", "ordem": 3, "resposta_aberta": False},
                    {"resposta": "Prefiro não informar", "ordem": 4, "resposta_aberta": False}
                ]
                
                for opcao_data in opcoes:
                    opcao = OpcoesRespostas(
                        id_pergunta=pergunta.id,
                        **opcao_data
                    )
                    db.add(opcao)
            
            # Adicionar opções para pergunta Sim/Não
            elif pergunta.codigo == "experiencia_programacao":
                opcoes = [
                    {"resposta": "Sim", "ordem": 1, "resposta_aberta": False},
                    {"resposta": "Não", "ordem": 2, "resposta_aberta": False}
                ]
                
                for opcao_data in opcoes:
                    opcao = OpcoesRespostas(
                        id_pergunta=pergunta.id,
                        **opcao_data
                    )
                    db.add(opcao)
        
        db.commit()
        print("Dados de exemplo criados com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar dados de exemplo: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Inicializando banco de dados...")
    create_tables()
    create_sample_data()
    print("Inicialização concluída!")
