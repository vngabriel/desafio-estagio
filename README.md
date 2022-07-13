# Desafio para o estágio na PontoTel

Para rodar a aplicação siga os seguintes passos:

1. Clone o projeto
2. Entre na pasta back-end
3. Instale as bibliotecas para o back-end em python com o seguinte comando:
```
    pip install -r requirements.txt
```
4. Faça uma cópia do arquivo .env.example e renomeie para .env, depois preencha os valores das variáveis de ambiente. Para essa aplicação se usa o SQLite, então para a variável DATABASE_URL, você pode colocar o seguinte valor:
```
    DATABASE_URL="sqlite:///./app.db"
```
5. Rode o seguinte comando para subir a aplicação:
```
    uvicorn src.main:app --reload
```
6. Agora entre na pasta front-end
7. Rode o seguinte comando:
```
    npm install
``` 
8. Rode o seguinte comando para subir o front-end:
```
    live-server
```
9. Agora a aplicação já deve está funcionando