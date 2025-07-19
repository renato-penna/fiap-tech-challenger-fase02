from fastapi import HTTPException
from app.schemas.optimize import OptimizeRequest, OptimizeResponse, ProdutoOutput
from app.services.genetic_optimizer import AlgoritmoGenetico

class OptimizerController:
    @staticmethod
    def optimize(data: OptimizeRequest) -> OptimizeResponse:
        ag = AlgoritmoGenetico(
            produtos=data.produtos,
            limite=data.limite,
            taxa_mutacao=data.taxa_mutacao,
            numero_geracoes=data.numero_geracoes,
            tamanho_populacao=data.tamanho_populacao
        )
        melhor = ag.resolver()
        produtos_result = []
        espaco_total = 0
        valor_total = 0
        for i, gene in enumerate(melhor.cromossomo):
            if gene == 1:
                p = data.produtos[i]
                total_espaco = p.espaco * p.quantidade
                total_valor = p.valor * p.quantidade
                produtos_result.append(ProdutoOutput(
                    nome=p.nome,
                    espaco=p.espaco,
                    valor=p.valor,
                    quantidade=p.quantidade,
                    total_espaco=total_espaco,
                    total_valor=total_valor
                ))
                espaco_total += total_espaco
                valor_total += total_valor
        return OptimizeResponse(produtos=produtos_result, espaco_total=espaco_total, valor_total=valor_total)
