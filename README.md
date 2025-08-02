# Sistema de Gerenciamento de Produtos com Otimização de Carga

Um sistema completo de gerenciamento de produtos com otimização de carga usando algoritmos genéticos, construído com FastAPI, Streamlit e PostgreSQL.

## 🏗️ Arquitetura

O sistema é composto por três microserviços principais:

### 📦 **Products Service** (Backend)
- **Tecnologia**: FastAPI + SQLAlchemy + PostgreSQL
- **Porta**: 8000
- **Função**: CRUD de produtos, API REST
- **Endpoints**: `/products/` (GET, POST, PUT, DELETE)

### 🧬 **Optimizer Service** (Backend)
- **Tecnologia**: FastAPI + Algoritmo Genético
- **Porta**: 8002
- **Função**: Otimização de carga usando algoritmos genéticos
- **Endpoints**: `/optimize/` (POST)

### 🎨 **Products Frontend** (Frontend)
- **Tecnologia**: Streamlit + Requests
- **Porta**: 8501
- **Função**: Interface web para gerenciamento e otimização
- **Páginas**: Gerenciamento de Produtos, Controle de Carga

### 🗄️ **Database** (PostgreSQL)
- **Porta**: 5433
- **Função**: Armazenamento persistente de produtos

## 🚀 Instalação e Execução

### Pré-requisitos
- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento local)

### Configuração Inicial
```bash
# Clone o repositório
git clone <repository-url>
cd fiap-tech-challenger-fase02

# Testar a configuração
./test-setup.sh

# Ou usar o Makefile para configurar automaticamente
make setup-env
```

### Execução Rápida
```bash
# Iniciar todos os serviços
make up

# Verificar o status
make health

# Ver logs
make logs
```

### Comandos Disponíveis
```bash
# Configuração
make setup-env       # Criar arquivos .env
make build           # Construir imagens

# Execução
make up              # Iniciar em background
make up-dev          # Iniciar em modo desenvolvimento
make down            # Parar serviços
make restart         # Reiniciar serviços

# Monitoramento
make logs            # Ver logs de todos os serviços
make logs-[service]  # Ver logs de um serviço específico
make health          # Verificar status dos serviços
make status          # Ver status dos containers

# Limpeza
make clean           # Parar e remover tudo
```

## 📊 Funcionalidades

### Gerenciamento de Produtos
- ✅ **CRUD Completo**: Criar, ler, atualizar, deletar produtos
- ✅ **Validação**: Dados validados com Pydantic
- ✅ **Persistência**: Armazenamento em PostgreSQL
- ✅ **API REST**: Endpoints padronizados

### Otimização de Carga
- ✅ **Algoritmo Genético**: Otimização automática
- ✅ **Parâmetros Configuráveis**: Tamanho da população, gerações, taxa de mutação
- ✅ **Restrições de Espaço**: Respeita limites de carga
- ✅ **Maximização de Valor**: Encontra melhor combinação

### Interface Web
- ✅ **Streamlit**: Interface moderna e responsiva
- ✅ **Gerenciamento Visual**: Grid interativo para produtos
- ✅ **Otimização Interativa**: Configuração e execução via web
- ✅ **Resultados Detalhados**: Relatórios de otimização

## 🔧 Configuração

### Variáveis de Ambiente
```bash
# Database
POSTGRES_DB=products_db
POSTGRES_USER=app_user
POSTGRES_PASSWORD=mysecretpassword

# API URLs (Frontend)
PRODUCTS_API_URL=http://fiap-tech-challenger-fase2-products-service:8000/products
OPTIMIZER_API_URL=http://fiap-tech-challenger-fase2-optimizer-cargo-service:8002/optimize/
```

### Estrutura de Dados
```sql
-- Tabela de Produtos
CREATE TABLE products (
    id VARCHAR PRIMARY KEY,
    nome VARCHAR NOT NULL,
    espaco FLOAT NOT NULL,
    valor FLOAT NOT NULL
);
```

## 🧪 Testes

### Testes de API
```bash
# Testar Products API
curl http://localhost:8000/products/

# Testar Optimizer API
curl -X POST http://localhost:8002/optimize/ \
  -H "Content-Type: application/json" \
  -d '{"products": [...], "limit": 10.0}'
```

### Testes de Interface
- Acesse: http://localhost:8501
- Navegue pelas páginas de gerenciamento e otimização

## 📈 Monitoramento

### Health Checks
```bash
# Verificar status dos serviços
make health
```

### Métricas
- **Products API**: Endpoint `/products/`
- **Optimizer API**: Endpoint `/optimize/`
- **Frontend**: Interface web em http://localhost:8501

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Portas já em uso
```bash
# Verificar portas em uso
lsof -i :5433
lsof -i :8000
lsof -i :8002
lsof -i :8501

# Parar serviços que estejam usando as portas
docker-compose down
```

#### 2. Erro de conexão com banco de dados
```bash
# Verificar se o banco está rodando
docker-compose logs fiap-tech-challenger-fase2-db

# Aguardar o health check do banco
docker-compose ps
```

#### 3. Serviços não iniciam
```bash
# Ver logs detalhados
make logs

# Reconstruir imagens
make build

# Limpar tudo e recomeçar
make clean
make up
```

#### 4. Arquivos .env ausentes
```bash
# Criar arquivos .env automaticamente
make setup-env
```

### Comandos de Diagnóstico
```bash
# Verificar status dos containers
docker-compose ps

# Ver logs de um serviço específico
docker-compose logs fiap-tech-challenger-fase2-products-service

# Verificar rede Docker
docker network ls
docker network inspect fiap-tech-challenger-fase02_app-network

# Verificar volumes
docker volume ls
```

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
fiap-tech-challenger-fase02/
├── products-service/                    # Backend de produtos (FastAPI + PostgreSQL)
│   ├── app/
│   │   ├── controllers/                # Lógica de negócio e validações
│   │   │   └── product_controller.py   # Controlador principal de produtos
│   │   ├── models/                     # Modelos SQLAlchemy para banco de dados
│   │   │   └── product_model.py        # Modelo da tabela 'products'
│   │   ├── repositories/               # Camada de acesso a dados
│   │   │   └── product_repository.py   # Operações CRUD no banco
│   │   ├── routers/                    # Endpoints da API REST
│   │   │   └── product_router.py       # Rotas GET, POST, PUT, DELETE
│   │   ├── schemas/                    # Modelos Pydantic para validação
│   │   │   └── product.py              # Schemas de entrada/saída
│   │   ├── database.py                 # Configuração SQLAlchemy e conexão
│   │   └── main.py                     # Aplicação FastAPI principal
│   ├── Dockerfile                      # Imagem Docker do serviço
│   └── requirements.txt                # Dependências Python
├── optimizer-cargo-service/             # Backend de otimização (FastAPI + Algoritmo Genético)
│   ├── app/
│   │   ├── controllers/                # Controladores e lógica de otimização
│   │   │   ├── optimizer_controller.py # Controlador principal de otimização
│   │   │   └── genetic_algorithm.py    # Implementação do algoritmo genético
│   │   ├── models/                     # Modelos para otimização
│   │   │   └── subject.py              # Modelo de indivíduo (cromossomo)
│   │   ├── routers/                    # Endpoints da API de otimização
│   │   │   └── optimizer_router.py     # Rota POST /optimize/
│   │   ├── schemas/                    # Schemas para requisições de otimização
│   │   │   └── optimize.py             # Schemas de entrada/saída
│   │   └── main.py                     # Aplicação FastAPI principal
│   ├── Dockerfile                      # Imagem Docker do serviço
│   └── requirements.txt                # Dependências Python
├── products-frontend/                   # Frontend web (Streamlit)
│   ├── app/
│   │   ├── pages/                      # Páginas da interface web
│   │   │   ├── gerenciamento_de_produtos.py  # CRUD de produtos
│   │   │   └── controle_de_carga.py          # Otimização de carga
│   │   ├── services/                   # Serviços de comunicação com APIs
│   │   │   ├── produto_service.py      # Cliente da API de produtos
│   │   │   └── otimizacao_service.py   # Cliente da API de otimização
│   │   ├── models/                     # Modelos de dados do frontend
│   │   │   └── produto.py              # Modelo de produto para UI
│   │   ├── utils/                      # Utilitários e helpers
│   │   │   └── ui_helpers.py           # Funções auxiliares da interface
│   │   ├── config.py                   # Configurações (URLs, mensagens)
│   │   └── main.py                     # Aplicação Streamlit principal
│   ├── Dockerfile                      # Imagem Docker do frontend
│   └── requirements.txt                # Dependências Python
├── docker-compose.yml                  # Orquestração de todos os serviços
├── Makefile                           # Comandos de automação (build, run, logs)
├── pyproject.toml                     # Configuração de ferramentas (black, isort, mypy)
├── .gitignore                         # Arquivos ignorados pelo Git
└── README.md                          # Documentação principal do projeto
```

### 📋 Descrição dos Arquivos Principais

#### **Products Service** (`products-service/`)
- **`main.py`**: Ponto de entrada da aplicação FastAPI, configuração de rotas e eventos de startup
- **`database.py`**: Configuração do SQLAlchemy, conexão com PostgreSQL e criação de tabelas
- **`controllers/product_controller.py`**: Lógica de negócio entre API e repositório
- **`repositories/product_repository.py`**: Operações CRUD no banco de dados
- **`models/product_model.py`**: Modelo SQLAlchemy da tabela 'products'
- **`routers/product_router.py`**: Endpoints REST (GET, POST, PUT, DELETE)
- **`schemas/product.py`**: Validação de dados com Pydantic

#### **Optimizer Service** (`optimizer-cargo-service/`)
- **`main.py`**: Aplicação FastAPI para otimização
- **`controllers/optimizer_controller.py`**: Orquestração do algoritmo genético
- **`controllers/genetic_algorithm.py`**: Implementação do algoritmo genético
- **`models/subject.py`**: Modelo de indivíduo (cromossomo) para otimização
- **`routers/optimizer_router.py`**: Endpoint POST /optimize/
- **`schemas/optimize.py`**: Schemas para requisições de otimização

#### **Frontend** (`products-frontend/`)
- **`main.py`**: Aplicação Streamlit principal com navegação
- **`pages/gerenciamento_de_produtos.py`**: Interface CRUD de produtos
- **`pages/controle_de_carga.py`**: Interface de otimização de carga
- **`services/produto_service.py`**: Cliente HTTP para API de produtos
- **`services/otimizacao_service.py`**: Cliente HTTP para API de otimização
- **`models/produto.py`**: Modelo de dados para interface
- **`utils/ui_helpers.py`**: Funções auxiliares da interface
- **`config.py`**: Configurações (URLs, mensagens, estilos)

#### **Configuração e Deploy**
- **`docker-compose.yml`**: Orquestração de todos os serviços
- **`Makefile`**: Comandos de automação (build, run, logs, health)
- **`pyproject.toml`**: Configuração de ferramentas de qualidade
- **`.gitignore`**: Arquivos ignorados pelo controle de versão

### 🏗️ Padrões de Arquitetura

#### **Clean Architecture**
- **Controllers**: Lógica de negócio e validações
- **Repositories**: Acesso a dados e persistência
- **Models**: Entidades do domínio
- **Schemas**: Validação e serialização

#### **Padrões de Código**
- **Type Hints**: Uso completo de typing
- **Docstrings**: Documentação completa
- **Linting**: Black, isort, flake8
- **Testing**: Estrutura preparada para testes

## 📝 Licença

Este projeto foi desenvolvido para o projeto FIAP Tech Challenger Fase 02, e serve como fonte de avaliação do grupo.

