from fastapi import FastAPI
from app.routers import product_router # Importa o roteador de produtos

# Cria a instância da aplicação FastAPI
app = FastAPI(title="Gerenciamento de Produtos Backend")

# Inclui o roteador de produtos na aplicação
app.include_router(product_router.router, prefix="/products", tags=["products"])

@app.get("/")
async def root():
    """
    Endpoint raiz para verificar se o serviço está funcionando.
    """
    return {"message": "Serviço de Gerenciamento de Produtos está online!"}