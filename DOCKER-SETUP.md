# Configuração Docker - FIAP Tech Challenger Fase 02

## Visão Geral

Este projeto consiste em uma aplicação distribuída com os seguintes serviços:

- **PostgreSQL Database** (porta 5433)
- **Products Service** - Backend FastAPI (porta 8000)
- **Optimizer Service** - Backend FastAPI para otimização (porta 8002)
- **Products Frontend** - Interface Streamlit (porta 8501)

## Configuração Inicial

### 1. Criar arquivos .env

Crie os seguintes arquivos `.env` em cada diretório de serviço:

#### products-service/.env
```bash
DATABASE_URL=postgresql://app_user:mysecretpassword@fiap-tech-challenger-fase2-db:5432/products_db
HOST=0.0.0.0
PORT=8000
```

#### optimizer-cargo-service/.env
```bash
HOST=0.0.0.0
PORT=8002
```

#### products-frontend/.env
```bash
PRODUCTS_API_URL=http://fiap-tech-challenger-fase2-products-service:8000/products
OPTIMIZER_URL=http://fiap-tech-challenger-fase2-optimizer-cargo-service:8002/optimize/
```

### 2. Executar o projeto

```bash
# Construir e iniciar todos os serviços
docker-compose up --build

# Executar em background
docker-compose up -d --build

# Parar todos os serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

## Acessos

Após a inicialização, você pode acessar:

- **Frontend**: http://localhost:8501
- **Products API**: http://localhost:8000
- **Optimizer API**: http://localhost:8002
- **Database**: localhost:5433

## Estrutura de Rede

O projeto usa uma rede Docker personalizada (`app-network`) para comunicação entre serviços:

- Todos os serviços estão na mesma rede
- Comunicação interna usa nomes de host dos containers
- Portas expostas para acesso externo

## Health Checks

Cada serviço possui health checks configurados:

- **Database**: Verifica se PostgreSQL está pronto
- **Products Service**: http://localhost:8000/health/
- **Optimizer Service**: http://localhost:8002/health/
- **Frontend**: http://localhost:8501/

## Dependências

A ordem de inicialização é controlada por dependências:

1. Database (com health check)
2. Products Service (depende do database)
3. Optimizer Service (depende do products service)
4. Frontend (depende de ambos os serviços)

## Troubleshooting

### Problemas comuns:

1. **Porta já em uso**: Verifique se as portas 5433, 8000, 8002, 8501 estão livres
2. **Erro de conexão com banco**: Aguarde o health check do database completar
3. **Serviços não iniciam**: Verifique os logs com `docker-compose logs [service-name]`
4. **Terminação de linha**: os arquivos entrypoint.sh devem usar terminação LF. Em IDE Windows mude de CRLF para LF.

### Comandos úteis:

```bash
# Ver logs de todos os serviços
docker-compose logs

# Ver logs de um serviço específico
docker-compose logs fiap-tech-challenger-fase2-products-service

# Reconstruir um serviço específico
docker-compose up --build fiap-tech-challenger-fase2-products-service

# Verificar status dos containers
docker-compose ps
```
