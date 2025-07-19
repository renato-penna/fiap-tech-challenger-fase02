import random
from typing import List
from app.schemas.optimize import ProdutoInput

class Individuo:
    def __init__(self, produtos: List[ProdutoInput], limite: float):
        self.produtos = produtos
        self.limite = limite
        self.cromossomo = [random.randint(0, 1) for _ in produtos]
        self.nota_avaliacao = 0
        self.espaco_usado = 0
        self.valores = [p.valor * p.quantidade for p in produtos]
        self.espacos = [p.espaco * p.quantidade for p in produtos]
        self.quantidades = [p.quantidade for p in produtos]
        self.avaliacao()

    def avaliacao(self):
        nota = 0
        espaco = 0
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == 1:
                nota += self.valores[i]
                espaco += self.espacos[i]
        if espaco > self.limite:
            nota = 1  # penalidade
        self.nota_avaliacao = nota
        self.espaco_usado = espaco

    def crossover(self, outro):
        corte = random.randint(1, len(self.cromossomo) - 1)
        filho1 = Individuo(self.produtos, self.limite)
        filho2 = Individuo(self.produtos, self.limite)
        filho1.cromossomo = self.cromossomo[:corte] + outro.cromossomo[corte:]
        filho2.cromossomo = outro.cromossomo[:corte] + self.cromossomo[corte:]
        filho1.avaliacao()
        filho2.avaliacao()
        return filho1, filho2

    def mutacao(self, taxa_mutacao):
        for i in range(len(self.cromossomo)):
            if random.random() < taxa_mutacao:
                self.cromossomo[i] = 1 - self.cromossomo[i]
        self.avaliacao()
        return self

class AlgoritmoGenetico:
    def __init__(self, produtos, limite, taxa_mutacao, numero_geracoes, tamanho_populacao):
        self.produtos = produtos
        self.limite = limite
        self.taxa_mutacao = taxa_mutacao
        self.numero_geracoes = numero_geracoes
        self.tamanho_populacao = tamanho_populacao
        self.populacao = [Individuo(produtos, limite) for _ in range(tamanho_populacao)]
        self.melhor = None

    def resolver(self):
        for _ in range(self.numero_geracoes):
            self.populacao.sort(key=lambda ind: ind.nota_avaliacao, reverse=True)
            nova_populacao = [self.populacao[0]]  # elitismo
            while len(nova_populacao) < self.tamanho_populacao:
                pais = random.sample(self.populacao[:10], 2)
                filhos = pais[0].crossover(pais[1])
                nova_populacao.extend([f.mutacao(self.taxa_mutacao) for f in filhos])
            self.populacao = nova_populacao[:self.tamanho_populacao]
        self.populacao.sort(key=lambda ind: ind.nota_avaliacao, reverse=True)
        self.melhor = self.populacao[0]
        return self.melhor
