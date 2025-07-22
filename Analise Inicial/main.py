from produtos import Produto
from individuo import Individuo
from algoritmo_genetico import AlgoritmoGenetico
import matplotlib.pyplot as plt


if __name__ == '__main__':
    lista_produtos = []
    lista_produtos.append(Produto("Smart Fridge LG", 0.720, 1050.00))
    lista_produtos.append(Produto("Samsung Galaxy S21", 0.000095, 3200.00))
    lista_produtos.append(Produto("Smart TV 60'' Philips", 0.410, 4700.00))
    lista_produtos.append(Produto("Smart TV 48'' Sony", 0.280, 3800.00))
    lista_produtos.append(Produto("Smart TV 40'' TCL", 0.190, 2500.00))
    lista_produtos.append(Produto("Notebook HP", 0.00380, 2700.00))
    lista_produtos.append(Produto("Fan Arno Turbo", 0.480, 210.00))
    lista_produtos.append(Produto("Microwave Brastemp", 0.0450, 350.00))
    lista_produtos.append(Produto("Microwave Samsung", 0.0500, 410.00))
    lista_produtos.append(Produto("Microwave Midea", 0.0300, 280.00))
    lista_produtos.append(Produto("Fridge Electrolux", 0.600, 900.00))
    lista_produtos.append(Produto("Fridge Consul Frost", 0.800, 1300.00))
    lista_produtos.append(Produto("Notebook Acer", 0.500, 2100.00))
    lista_produtos.append(Produto("Notebook Apple MacBook Air", 0.520, 5200.00))
    lista_produtos.append(Produto("Tablet Samsung Tab S7", 0.000050, 1800.00))
    lista_produtos.append(Produto("Air Conditioner LG", 0.650, 2200.00))
    lista_produtos.append(Produto("Washing Machine Panasonic", 0.900, 1800.00))
    lista_produtos.append(Produto("Dryer Electrolux", 0.700, 1500.00))
    lista_produtos.append(Produto("Bluetooth Speaker JBL", 0.000030, 600.00))
    lista_produtos.append(Produto("Coffee Maker Nespresso", 0.0200, 450.00))
    
    espacos = []
    valores = []
    limite = 3
    tamanho_populacao = 2000
    taxa_mutacao = 0.01
    numero_geracoes = 100
    ag = AlgoritmoGenetico(tamanho_populacao)
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)
    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                       lista_produtos[i].valor))
    
    plt.plot(ag.lista_solucoes)
    plt.title("Acompanhamento dos valores")
    plt.savefig("grafico.png")