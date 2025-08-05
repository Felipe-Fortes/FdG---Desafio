@echo off
echo ====================================
echo Sistema de Formularios Dinamicos
echo ====================================
echo.

echo Verificando se o banco esta configurado...
python init_db.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO: Falha ao inicializar o banco de dados.
    echo Verifique se o PostgreSQL esta rodando e as configuracoes no arquivo .env estao corretas.
    pause
    exit /b 1
)

echo.
echo Iniciando a aplicacao...
echo A API estara disponivel em: http://127.0.0.1:8000
echo Documentacao disponivel em: http://127.0.0.1:8000/docs
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

python run.py
