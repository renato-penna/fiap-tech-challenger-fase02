#!/bin/bash

# Script de teste para verificar a configuração do Docker Compose

echo "=== Teste de Configuração Docker Compose ==="
echo ""

# Verificar se o Docker está rodando
echo "1. Verificando se o Docker está rodando..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker e tente novamente."
    exit 1
fi
echo "✅ Docker está rodando"

# Verificar se o docker-compose está disponível
echo ""
echo "2. Verificando docker-compose..."
if ! docker-compose --version > /dev/null 2>&1; then
    echo "❌ docker-compose não está disponível"
    exit 1
fi
echo "✅ docker-compose está disponível"

# Verificar se os arquivos .env existem
echo ""
echo "3. Verificando arquivos .env..."
if [ ! -f "products-service/.env" ]; then
    echo "⚠️  products-service/.env não encontrado. Criando..."
    echo "DATABASE_URL=postgresql://app_user:mysecretpassword@fiap-tech-challenger-fase2-db:5432/products_db" > products-service/.env
    echo "HOST=0.0.0.0" >> products-service/.env
    echo "PORT=8000" >> products-service/.env
fi

if [ ! -f "optimizer-cargo-service/.env" ]; then
    echo "⚠️  optimizer-cargo-service/.env não encontrado. Criando..."
    echo "HOST=0.0.0.0" > optimizer-cargo-service/.env
    echo "PORT=8002" >> optimizer-cargo-service/.env
fi

if [ ! -f "products-frontend/.env" ]; then
    echo "⚠️  products-frontend/.env não encontrado. Criando..."
    echo "PRODUCTS_API_URL=http://fiap-tech-challenger-fase2-products-service:8000/products" > products-frontend/.env
    echo "OPTIMIZER_URL=http://fiap-tech-challenger-fase2-optimizer-cargo-service:8002/optimize/" >> products-frontend/.env
fi
echo "✅ Arquivos .env verificados/criados"

# Verificar se as portas estão livres
echo ""
echo "4. Verificando portas..."
PORTS=(5433 8000 8002 8501)
for port in "${PORTS[@]}"; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  Porta $port está em uso"
    else
        echo "✅ Porta $port está livre"
    fi
done

# Testar build das imagens
echo ""
echo "5. Testando build das imagens..."
if docker-compose build --no-cache > /dev/null 2>&1; then
    echo "✅ Build das imagens bem-sucedido"
else
    echo "❌ Erro no build das imagens"
    echo "Execute 'docker-compose build' para ver os detalhes do erro"
    exit 1
fi

echo ""
echo "=== Configuração verificada com sucesso! ==="
echo ""
echo "Para iniciar os serviços, execute:"
echo "  make up"
echo ""
echo "Para ver os logs:"
echo "  make logs"
echo ""
echo "Para verificar o status:"
echo "  make health" 