# Exemplos de Uso da API - Sistema de Formulários Dinâmicos

Este arquivo contém exemplos práticos de como usar a API do Sistema de Formulários Dinâmicos.

## URLs importantes

- **API Base**: http://127.0.0.1:8000
- **Documentação Swagger**: http://127.0.0.1:8000/docs
- **Documentação ReDoc**: http://127.0.0.1:8000/redoc

## Exemplos usando curl (Windows PowerShell)

### 1. Verificar se a API está funcionando
```powershell
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
```

### 2. Formulários

#### Listar todos os formulários
```powershell
curl http://127.0.0.1:8000/api/v1/formularios/
```

#### Obter formulário específico
```powershell
curl http://127.0.0.1:8000/api/v1/formularios/1
```

#### Criar novo formulário
```powershell
curl -X POST "http://127.0.0.1:8000/api/v1/formularios/" `
     -H "Content-Type: application/json" `
     -d '{
       "titulo": "Pesquisa de Satisfação",
       "descricao": "Formulário para avaliar a satisfação do cliente",
       "ordem": 2
     }'
```

#### Atualizar formulário
```powershell
curl -X PUT "http://127.0.0.1:8000/api/v1/formularios/1" `
     -H "Content-Type: application/json" `
     -d '{
       "titulo": "Formulário de Cadastro Atualizado",
       "descricao": "Descrição atualizada"
     }'
```

### 3. Perguntas

#### Listar perguntas de um formulário
```powershell
curl "http://127.0.0.1:8000/api/v1/perguntas/formulario/1"
```

#### Listar perguntas com filtros e paginação
```powershell
# Apenas perguntas obrigatórias
curl "http://127.0.0.1:8000/api/v1/perguntas/formulario/1?obrigatoria=true"

# Perguntas do tipo texto livre
curl "http://127.0.0.1:8000/api/v1/perguntas/formulario/1?tipo_pergunta=texto_livre"

# Com paginação (página 2, 5 itens por página)
curl "http://127.0.0.1:8000/api/v1/perguntas/formulario/1?skip=5&limit=5"

# Ordenar por título em ordem decrescente
curl "http://127.0.0.1:8000/api/v1/perguntas/formulario/1?order_by=titulo&order_desc=true"
```

#### Contar perguntas com filtros
```powershell
curl "http://127.0.0.1:8000/api/v1/perguntas/formulario/1/count?obrigatoria=true"
```

#### Criar nova pergunta
```powershell
curl -X POST "http://127.0.0.1:8000/api/v1/perguntas/" `
     -H "Content-Type: application/json" `
     -d '{
       "id_formulario": 1,
       "titulo": "Qual seu nível de escolaridade?",
       "codigo": "escolaridade",
       "orientacao_resposta": "Selecione seu nível de escolaridade",
       "ordem": 5,
       "obrigatoria": true,
       "sub_pergunta": false,
       "tipo_pergunta": "unica_escolha",
       "opcoes_respostas": [
         {
           "resposta": "Ensino Fundamental",
           "ordem": 1,
           "resposta_aberta": false
         },
         {
           "resposta": "Ensino Médio",
           "ordem": 2,
           "resposta_aberta": false
         },
         {
           "resposta": "Ensino Superior",
           "ordem": 3,
           "resposta_aberta": false
         },
         {
           "resposta": "Pós-graduação",
           "ordem": 4,
           "resposta_aberta": false
         }
       ]
     }'
```

### 4. Opções de Resposta

#### Listar opções de uma pergunta
```powershell
curl "http://127.0.0.1:8000/api/v1/opcoes-respostas/pergunta/3"
```

#### Adicionar nova opção de resposta
```powershell
curl -X POST "http://127.0.0.1:8000/api/v1/opcoes-respostas/pergunta/3" `
     -H "Content-Type: application/json" `
     -d '{
       "resposta": "Outro",
       "ordem": 5,
       "resposta_aberta": true
     }'
```

## Exemplos usando Python requests

```python
import requests
import json

base_url = "http://127.0.0.1:8000/api/v1"

# Listar formulários
response = requests.get(f"{base_url}/formularios/")
print("Formulários:", response.json())

# Criar novo formulário
novo_formulario = {
    "titulo": "Avaliação de Evento",
    "descricao": "Formulário para avaliar eventos",
    "ordem": 3
}
response = requests.post(f"{base_url}/formularios/", json=novo_formulario)
formulario_criado = response.json()
print("Formulário criado:", formulario_criado)

# Listar perguntas com filtros
params = {
    "obrigatoria": True,
    "tipo_pergunta": "unica_escolha",
    "limit": 10
}
response = requests.get(f"{base_url}/perguntas/formulario/1", params=params)
print("Perguntas filtradas:", response.json())
```

## Tipos de Pergunta Disponíveis

- `Sim_Nao`: Pergunta com resposta Sim/Não
- `multipla_escolha`: Múltipla escolha (várias respostas possíveis)
- `unica_escolha`: Escolha única (uma resposta apenas)
- `texto_livre`: Campo de texto livre
- `Inteiro`: Número inteiro
- `Numero com duas casa decimais`: Número decimal

## Cenários de Uso Comuns

### 1. Criar um formulário completo de pesquisa
1. Criar o formulário
2. Adicionar perguntas de diferentes tipos
3. Configurar opções para perguntas de múltipla escolha
4. Testar listagem com filtros

### 2. Gerenciar ordenação de perguntas
1. Listar perguntas ordenadas por ordem
2. Atualizar ordem das perguntas conforme necessário
3. Verificar se a ordenação está correta

### 3. Implementar paginação em frontend
1. Usar parâmetros `skip` e `limit`
2. Implementar contagem total com endpoint `/count`
3. Calcular número de páginas

## Dicas Importantes

1. **Validação**: A API valida automaticamente todos os dados de entrada
2. **Relacionamentos**: Ao deletar um formulário, todas as perguntas associadas são deletadas automaticamente
3. **Códigos únicos**: O campo `codigo` das perguntas deve ser único
4. **Ordenação**: Use o campo `ordem` para controlar a sequência de exibição
5. **Documentação**: Use `/docs` para testar interativamente todos os endpoints
