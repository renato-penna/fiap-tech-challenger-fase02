"""
Genetic Algorithm Module.

This module implements the GeneticAlgorithm class for solving the truck packing
optimization problem using a genetic algorithm approach. It provides methods
for population initialization, sorting, evaluation, parent selection, elitism,
and running the optimization process.
"""

from random import random
from typing import List, Optional

from app.models.subject import Subject
from app.schemas.product import ProductInput


class GeneticAlgorithm:
    """
    GeneticAlgorithm class for solving the truck packing optimization problem
    using a genetic algorithm.

    Attributes:
        products (List[ProductInput]): List of products to optimize.
        population (List[Subject]): Current population of subjects.
        generation (int): Current generation number.
        solutions_list (List[float]): List of best solution values per generation.
        mutation_rate (float): Mutation rate for genetic algorithm.
        number_generations (int): Number of generations to run.
        population_size (int): Size of the population.
        limit (float): Space limit of the truck.
        best_solution (Optional[Subject]): Best solution found so far.
    """
    products: List[ProductInput]
    population: List[Subject]
    generation: int = 0
    solutions_list: List[float] = []
    mutation_rate: float = 0.01
    number_generations: int = 100
    population_size: int = 200
    limit: float = 0.0
    best_solution: Optional[Subject] = None

    def __init__(self, products: List[ProductInput], limit: float,
                 population_size: int, number_generations: int,
                 mutation_rate: float = 0) -> None:
        """
        Initialize the GeneticAlgorithm instance.

        Args:
            products: List of products to optimize.
            limit: Space limit of the truck.
            population_size: Size of the population.
            number_generations: Number of generations to run.
            mutation_rate: Mutation rate. Defaults to 0.
        """
        self.products = products
        self.limit = limit
        self.population_size = population_size
        self.number_generations = number_generations
        self.mutation_rate = mutation_rate

    def start_initial_population(self) -> None:
        """
        Initializes the population with random subjects and resets the generation counter.
        Sets the best solution to the first subject in the population.
        """
        # Reseta contador de geração
        self.generation = 0
        self.population = []
        # Iniciando a população de cromossomos, contendo os espaços e valores dos produtos
        # e variando a carga
        for i in range(self.population_size):
            self.population.append(Subject(self.products, self.limit))
        # Define a primeira solução como melhor inicial
        self.best_solution = self.population[0]

    def sort_population(self) -> None:
        """
        Sorts the population in descending order by evaluation note.
        """
        # Avaliação da População - ordenando por maior pontuação
        # para que você possa selecionar os melhores indivíduos
        self.population.sort(
            key=lambda subject: subject.evaluation_note,
            reverse=True
        )

    def sum_evaluations(self) -> float:
        """
        Sums the evaluation notes of all subjects in the population.

        Returns:
            float: The sum of evaluation notes.
        """
        return sum(subject.evaluation_note for subject in self.population)

    def select_parent(self, sum_evaluation: float) -> int:
        """
        Selects a parent index using the roulette wheel selection method.

        Args:
            sum_evaluation: The sum of evaluation notes in the population.

        Returns:
            int: The index of the selected parent.

        Raises:
            ValueError: If population is empty.
        """
        # Roleta viciada: indivíduos com melhor fitness têm maior chance
        # Vamos selecionar os pais para gerar uma nova população
        # Pegamos toda a população, avaliamos e selecionamos os melhores.
        # Vamos usar o método da roleta viciada
        parent = -1
        # multiplicação de um número aleatório pela soma da população
        drawn_value = random() * sum_evaluation  # Valor sorteado
        soma = 0
        i = 0
        while i < len(self.population) and soma < drawn_value:
            soma += self.population[i].evaluation_note
            parent += 1
            i += 1
        return parent

    def update_best_solution(self) -> None:
        """
        Updates the best solution if the provided subject is better than the current best.
        """
        # Verificando se o indivíduo atual é melhor que a melhor solução atual (Elitismo)
        subject_candidate = self.population[0]
        self.solutions_list.append(subject_candidate.evaluation_note)

        print(f"> Gen Best Solution ... {subject_candidate}")
        # Atualiza a melhor solução global se necessário
        if self.best_solution is None:  # Primeira melhor solução
            # Se ainda não há melhor solução, define o sujeito atual como o melhor
            self.best_solution = subject_candidate
        elif (subject_candidate.evaluation_note >
              self.best_solution.evaluation_note):
            self.best_solution = subject_candidate
        print(f"> Best Solution until now ... {self.best_solution}")

    def start_new_generation(self) -> None:
        """
        Starts a new generation by selecting parents and creating offspring.
        This method generates a new population by performing crossover and
        mutation on selected parents.
        """
        # Seleção de pais usando roleta viciada
        sum_evaluation = self.sum_evaluations()
        new_population = []
        while len(new_population) < self.population_size:
            # Vamos gerar dois pais de uma vez para o crossover
            parent1 = self.select_parent(sum_evaluation)
            parent2 = self.select_parent(sum_evaluation)
            # Realiza crossover entre os pais
            children = self.population[parent1].crossover(
                self.population[parent2]
            )
            # Aplica mutação nos filhos
            new_population.extend([
                child.mutate(self.mutation_rate) for child in children
            ])
        self.population = list(new_population)

    def run(self) -> Optional[Subject]:
        """
        Runs the genetic algorithm optimization process for the specified number of generations.
        Returns the best solution found.

        Returns:
            Optional[Subject]: The best solution found after all generations.

        Raises:
            Exception: If population is not initialized.
        """
        # Inicializa a melhor solução e lista de soluções
        self.best_solution = None
        self.solutions_list = []

        # Inicializa população e avalia a primeira geração
        self.start_initial_population()
        self.sort_population()
        self.update_best_solution()

        # Executa o algoritmo genético por N gerações
        for _ in range(self.number_generations):
            self.start_new_generation()  # Cria nova geração
            self.sort_population()       # Ordena por fitness
            self.update_best_solution()  # Atualiza melhor solução

        return self.best_solution

