# Sistema de Formulários Dinâmicos

API desenvolvida em FastAPI para gerenciamento de formulários dinâmicos com perguntas cadastradas pelos próprios usuários.

## 🚀 Funcionalidades

- **CRUD completo de Formulários**: Criar, listar, atualizar e deletar formulários
- **CRUD completo de Perguntas**: Gerenciar perguntas associadas aos formulários
- **CRUD de Opções de Resposta**: Gerenciar opções para perguntas de múltipla escolha
- **Filtros avançados**: Filtrar perguntas por tipo, obrigatoriedade, etc.
- **Ordenação**: Ordenar perguntas por diferentes campos
- **Paginação**: Suporte completo à paginação em todas as listagens
- **Documentação automática**: Swagger UI e ReDoc integrados

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e de alta performance
- **SQLAlchemy**: ORM para interação com banco de dados
- **PostgreSQL**: Banco de dados relacional
- **Pydantic**: Validação de dados e serialização
- **Uvicorn**: Servidor ASGI para execução da aplicação

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL 12+
- pip (gerenciador de pacotes Python)

## ⚙️ Configuração do Ambiente

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd FdG\ -\ Desafio
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados PostgreSQL

Certifique-se de que o PostgreSQL esteja instalado e rodando. Crie um banco de dados chamado `postgres` (ou configure conforme suas preferências no arquivo `.env`).

### 5. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:
```bash
copy .env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
# Configurações do Banco de Dados PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=12345

# Configurações da API
API_HOST=127.0.0.1
API_PORT=8000
API_DEBUG=True
```

### 6. Inicialize o banco de dados

Execute o script para criar as tabelas e dados de exemplo:
```bash
python init_db.py
```

## 🚀 Executando a Aplicação

### Opção 1: Usando o script de execução
```bash
python run.py
```

### Opção 2: Usando uvicorn diretamente
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

A aplicação estará disponível em:
- **API**: http://127.0.0.1:8000
- **Documentação Swagger**: http://127.0.0.1:8000/docs
- **Documentação ReDoc**: http://127.0.0.1:8000/redoc

## 📚 Documentação da API

### Endpoints Principais

#### Formulários
- `GET /api/v1/formularios/` - Lista formulários com paginação
- `GET /api/v1/formularios/{id}` - Obtém formulário específico
- `POST /api/v1/formularios/` - Cria novo formulário
- `PUT /api/v1/formularios/{id}` - Atualiza formulário
- `DELETE /api/v1/formularios/{id}` - Deleta formulário

#### Perguntas
- `GET /api/v1/perguntas/formulario/{formulario_id}` - Lista perguntas de um formulário com filtros, ordenação e paginação
- `GET /api/v1/perguntas/formulario/{formulario_id}/count` - Conta perguntas com filtros aplicados
- `GET /api/v1/perguntas/{id}` - Obtém pergunta específica
- `POST /api/v1/perguntas/` - Cria nova pergunta
- `PUT /api/v1/perguntas/{id}` - Atualiza pergunta
- `DELETE /api/v1/perguntas/{id}` - Deleta pergunta

#### Opções de Resposta
- `GET /api/v1/opcoes-respostas/pergunta/{pergunta_id}` - Lista opções de uma pergunta
- `POST /api/v1/opcoes-respostas/pergunta/{pergunta_id}` - Cria nova opção
- `PUT /api/v1/opcoes-respostas/{id}` - Atualiza opção
- `DELETE /api/v1/opcoes-respostas/{id}` - Deleta opção

### Filtros Disponíveis para Perguntas

- `tipo_pergunta`: Filtra por tipo (Sim_Nao, multipla_escolha, unica_escolha, texto_livre, Inteiro, Numero com duas casa decimais)
- `obrigatoria`: Filtra por obrigatoriedade (true/false)
- `sub_pergunta`: Filtra por sub-pergunta (true/false)

### Parâmetros de Paginação e Ordenação

- `skip`: Número de registros para pular (padrão: 0)
- `limit`: Limite de registros por página (padrão: 10, máximo: 100)
- `order_by`: Campo para ordenação (padrão: "ordem")
- `order_desc`: Ordenação decrescente (padrão: false)

## 🗃️ Estrutura do Banco de Dados

O sistema utiliza as seguintes tabelas:

- **formulario**: Armazena os formulários
- **pergunta**: Armazena as perguntas associadas aos formulários
- **opcoes_respostas**: Armazena as opções de resposta para perguntas
- **opcoes_resposta_pergunta**: Tabela de relacionamento (conforme modelo original)

## 📁 Estrutura do Projeto

```
FdG - Desafio/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação FastAPI principal
│   ├── database.py          # Configuração do banco de dados
│   ├── models/
│   │   └── __init__.py      # Modelos SQLAlchemy
│   ├── schemas/
│   │   └── __init__.py      # Schemas Pydantic
│   ├── crud/
│   │   └── __init__.py      # Operações CRUD
│   └── routers/
│       ├── __init__.py
│       ├── formularios.py   # Endpoints de formulários
│       ├── perguntas.py     # Endpoints de perguntas
│       └── opcoes_respostas.py # Endpoints de opções
├── .env                     # Variáveis de ambiente
├── .env.example            # Exemplo de variáveis de ambiente
├── requirements.txt        # Dependências Python
├── init_db.py             # Script de inicialização do banco
├── run.py                 # Script para executar a aplicação
├── main.py                # Arquivo original (mantido)
├── estrutura.png          # Diagrama do banco de dados
└── README.md              # Este arquivo
```

## 🧪 Testando a API

### Usando a documentação interativa (Swagger)
1. Acesse http://127.0.0.1:8000/docs
2. Explore e teste os endpoints diretamente na interface

### Exemplo de uso com curl

**Criar um formulário:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/formularios/" \
     -H "Content-Type: application/json" \
     -d '{
       "titulo": "Pesquisa de Satisfação",
       "descricao": "Formulário para avaliar a satisfação do cliente",
       "ordem": 1
     }'
```

**Listar perguntas com filtros:**
```bash
curl "http://127.0.0.1:8000/api/v1/perguntas/formulario/1?tipo_pergunta=texto_livre&obrigatoria=true&skip=0&limit=5"
```

## 🔧 Solução de Problemas

### Erro de conexão com banco de dados
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no arquivo `.env`
- Certifique-se de que o banco de dados existe

### Erro de importação de módulos
- Verifique se o ambiente virtual está ativado
- Reinstale as dependências: `pip install -r requirements.txt`

### Porta já em uso
- Altere a porta no arquivo `.env` (variável `API_PORT`)
- Ou mate o processo que está usando a porta 8000

## 📝 Notas Adicionais

- O sistema não possui autenticação implementada, conforme especificado nos requisitos
- Os dados de exemplo são criados automaticamente ao executar `init_db.py`
- A aplicação está configurada para recarregar automaticamente durante o desenvolvimento
- Todos os endpoints possuem validação de dados e tratamento de erros adequados

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

Desenvolvido como parte do desafio técnico para a posição de desenvolvedor.
