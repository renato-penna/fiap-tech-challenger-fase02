
"""
subject.py

This module implements the Subject class, representing an individual in the genetic algorithm for truck packing optimization.
It provides methods for chromosome generation, evaluation, crossover, mutation, and string representation.
"""

from random import random
from typing import List
from app.schemas.product import ProductInput


class Subject:
    """
    Subject class representing an individual in the genetic algorithm for truck packing optimization.

    Attributes:
        generation (int): Generation number of the subject.
        limit (float): Space limit of the truck.
        evaluation_note (float): Evaluation score of the subject.
        space_used (float): Total space used by the subject.
        products (List[ProductInput]): List of products.
        values (List[float]): List of product values.
        spaces (List[float]): List of product spaces.
        amounts (List[int]): List of product amounts.
        chromosome (List[str]): Chromosome representing product selection.
    """
    
    def __init__(self, products: List[ProductInput], limit: float, generation: int = 0) -> None:
        """
        Initializes a Subject instance, generates chromosome, and evaluates the initial solution.

        Args:
            products (List[ProductInput]): List of products.
            limit (float): Space limit of the truck.
            generation (int, optional): Generation number. Defaults to 0.
        """
        # Inicia variáveis de controle
        self.generation = generation
        self.limit = limit
        self.evaluation_note = 0  # Soma dos valores que entrarão na carga
        self.space_used = 0  # Soma do espaço total usado
        
        # Inicia variáveis de informação e gera o cromossomo
        self.products = products
        self._init_info_variables()
        self._generate_chromosome()
        
        # Primeira avaliação
        self.evaluate()
        
    def _init_info_variables(self) -> None:
        """
        Initializes info variables for values, spaces, and amounts based on products.
        """
        self.values = [p.value * p.amount for p in self.products]
        self.spaces = [p.space * p.amount for p in self.products]
        self.amounts = [p.amount for p in self.products]
        
    def _generate_chromosome(self) -> None:
        """
        Generates a random chromosome for the subject, representing product selection.
        """
        self.chromosome = []
        for i in range(len(self.spaces)):
            if random() < 0.5:  # 50% de chance de pegar o produto
                self.chromosome.append("0")  # Não vou pegar
            else:
                self.chromosome.append("1")  # Vou pegar
        
    def evaluate(self) -> None:
        """
        Evaluates the subject's chromosome, calculating the evaluation note and space used.
        Applies a penalty if the space used exceeds the limit.
        """
        evaluation_note = 0
        space_used = 0
        for i in range(len(self.chromosome)):
            if self.chromosome[i] == "1":
                evaluation_note += (self.values[i] * self.amounts[i])
                space_used += (self.spaces[i] * self.amounts[i])

        if space_used > self.limit:
            evaluation_note = 1  # penalidade: Se a soma for maior que o limite de espaço,
            # excede o valor da carga.
            # Não posso carregar tudo, então esta solução não é uma boa solução
            # Rebaixo a pontuação para 1.
            
        self.evaluation_note = evaluation_note
        self.space_used = space_used

    def crossover(self, other: 'Subject') -> tuple['Subject', 'Subject']:
        """
        Performs crossover between this subject and another, generating two offspring.

        Args:
            other (Subject): The other parent subject.

        Returns:
            Tuple[Subject, Subject]: Two offspring subjects.
        """
        # Define posição de corte para o crossover
        cut_position = round(random() * len(self.chromosome))
        
        # Inicia os filhos com o crossover dos pais
        son1 = Subject(self.products, self.limit, generation=self.generation + 1)
        son2 = Subject(self.products, self.limit, generation=self.generation + 1)
        
        # subdivide os cromossomos e substitui os cromossomos dos filhos
        son1.chromosome = self.chromosome[:cut_position] + other.chromosome[cut_position:]
        son2.chromosome = other.chromosome[:cut_position] + self.chromosome[cut_position:]
        
        # Avalia os filhos
        son1.evaluate()
        son2.evaluate()
        return son1, son2

    def mutate(self, mutation_rate: float) -> 'Subject':
        """
        Mutates the subject's chromosome based on the mutation rate.

        Args:
            mutation_rate (float): Probability of mutation for each gene.

        Returns:
            Subject: The mutated subject.
        """
        for i in range(len(self.chromosome)):
            if random() < mutation_rate:
                if self.chromosome[i] == '1':
                    self.chromosome[i] = '0'
                else:
                    self.chromosome[i] = '1'
        self.evaluate()
        return self
    
    def __str__(self) -> str:
        """
        Returns a string representation of the subject, including generation, value, space used, and chromosome.

        Returns:
            str: String representation of the subject.
        """
        return f"""
        Gen:{self.generation} -> 
        Value: {self.evaluation_note} 
        Space Used: {self.space_used} 
        Chromosome: {self.chromosome}
        """