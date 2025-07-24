
"""
genetic_algorithm.py

This module implements the GeneticAlgorithm class for solving the truck packing optimization problem using a genetic algorithm approach.
It provides methods for population initialization, sorting, evaluation, parent selection, elitism, and running the optimization process.
"""

from random import random
from typing import List, Optional
from app.schemas.product import ProductInput
from app.models.subject import Subject


class GeneticAlgorithm:
    """
    GeneticAlgorithm class for solving the truck packing optimization problem using a genetic algorithm.

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
    
    def __init__(self, products: List[ProductInput], limit: float, population_size: int, number_generations: int, mutation_rate: float = 0) -> None:
        """
        Initialize the GeneticAlgorithm instance.

        Args:
            products (List[ProductInput]): List of products to optimize.
            limit (float): Space limit of the truck.
            population_size (int): Size of the population.
            number_generations (int): Number of generations to run.
            mutation_rate (float, optional): Mutation rate. Defaults to 0.
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
        self.generation = 0
        self.population = []
        # Starting the chromosomes population, containing the spaces and product values
        # and varying the load
        for i in range(self.population_size):
            self.population.append(Subject(self.products, self.limit))
        self.best_solution = self.population[0]
    
    def sort_population(self) -> None:
        """
        Sorts the population in descending order by evaluation note.
        """
        # Population Assessment - sorting it by highest score
        # so you can select the best individuals
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
            sum_evaluation (float): The sum of evaluation notes in the population.

        Returns:
            int: The index of the selected parent.

        Raises:
            ValueError: If population is empty.
        """
        # Let's select the parents to generate a new population
        # We take the entire population, evaluate it, and select the best ones.
        # Let's use the rigged roulette method
        parent = -1
        # multiplication of a random number by the population sum
        drawn_value = random() * sum_evaluation 
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
        # Checking whether the current individual is better than the current best solution (Elitism)
        subject_candidate = self.population[0]
        self.solutions_list.append(subject_candidate.evaluation_note)
        
        print(f"> Gen Best Solution ... {subject_candidate}")
        if self.best_solution is None: # First best Solution
            # If there is no best solution yet, set the current subject as the best
            self.best_solution = subject_candidate
        elif subject_candidate.evaluation_note > self.best_solution.evaluation_note:
            self.best_solution = subject_candidate
        print(f"> Best Solution until now ... {self.best_solution}")
        
    def start_new_generation(self) -> None:
        """
        Starts a new generation by selecting parents and creating offspring.
        This method generates a new population by performing crossover and mutation on selected parents.
        """
        sum_evaluation = self.sum_evaluations()
        new_population = []
        while len(new_population) < self.population_size:
            # Let's generate two parents at once for the crossover
            parent1 = self.select_parent(sum_evaluation)
            parent2 = self.select_parent(sum_evaluation)
            children = self.population[parent1].crossover(self.population[parent2])
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
        self.best_solution = None
        self.solutions_list = []
        
        self.start_initial_population()
        self.sort_population()
        self.update_best_solution()
        
        for _ in range(self.number_generations):
            self.start_new_generation()
            self.sort_population()
            self.update_best_solution()
            
        return self.best_solution

