from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import formularios, perguntas, opcoes_respostas
import os
from dotenv import load_dotenv

load_dotenv()

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Formulários Dinâmicos",
    description="API para gerenciamento de formulários dinâmicos com perguntas cadastradas pelos usuários",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(formularios.router, prefix="/api/v1")
app.include_router(perguntas.router, prefix="/api/v1")
app.include_router(opcoes_respostas.router, prefix="/api/v1")


@app.get("/")
def root():
    """Endpoint raiz da API"""
    return {
        "message": "Sistema de Formulários Dinâmicos",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Endpoint para verificação de saúde da aplicação"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("API_DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug
    )
