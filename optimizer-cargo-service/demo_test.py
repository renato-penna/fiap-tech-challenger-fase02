"""
Demo Test Module.

This module provides a demonstration test for the cargo optimization
service, sending sample product data to test the genetic algorithm.
"""

import random
from typing import List, Dict, Any

import requests


def create_sample_products() -> List[Dict[str, Any]]:
    """
    Create sample product data for testing the optimization service.

    Returns:
        List[Dict[str, Any]]: List of sample products with random quantities
    """
    return [
        {"name": "Smart Fridge LG", "space": 0.720, "value": 1050.00,
         "amount": random.randint(1, 3)},
        {"name": "Samsung Galaxy S21", "space": 0.000095, "value": 3200.00,
         "amount": random.randint(1, 3)},
        {"name": "Smart TV 60'' Philips", "space": 0.410, "value": 4700.00,
         "amount": random.randint(1, 3)},
        {"name": "Smart TV 48'' Sony", "space": 0.280, "value": 3800.00,
         "amount": random.randint(1, 3)},
        {"name": "Smart TV 40'' TCL", "space": 0.190, "value": 2500.00,
         "amount": random.randint(1, 3)},
        {"name": "Notebook HP", "space": 0.00380, "value": 2700.00,
         "amount": random.randint(1, 3)},
        {"name": "Fan Arno Turbo", "space": 0.480, "value": 210.00,
         "amount": random.randint(1, 3)},
        {"name": "Microwave Brastemp", "space": 0.0450, "value": 350.00,
         "amount": random.randint(1, 3)},
        {"name": "Microwave Samsung", "space": 0.0500, "value": 410.00,
         "amount": random.randint(1, 3)},
        {"name": "Microwave Midea", "space": 0.0300, "value": 280.00,
         "amount": random.randint(1, 3)},
        {"name": "Fridge Electrolux", "space": 0.600, "value": 900.00,
         "amount": random.randint(1, 3)},
        {"name": "Fridge Consul Frost", "space": 0.800, "value": 1300.00,
         "amount": random.randint(1, 3)},
        {"name": "Notebook Acer", "space": 0.500, "value": 2100.00,
         "amount": random.randint(1, 3)},
        {"name": "Notebook Apple MacBook Air", "space": 0.520, "value": 5200.00,
         "amount": random.randint(1, 3)},
        {"name": "Tablet Samsung Tab S7", "space": 0.000050, "value": 1800.00,
         "amount": random.randint(1, 3)},
        {"name": "Air Conditioner LG", "space": 0.650, "value": 2200.00,
         "amount": random.randint(1, 3)},
        {"name": "Washing Machine Panasonic", "space": 0.900, "value": 1800.00,
         "amount": random.randint(1, 3)},
        {"name": "Dryer Electrolux", "space": 0.700, "value": 1500.00,
         "amount": random.randint(1, 3)},
        {"name": "Bluetooth Speaker JBL", "space": 0.000030, "value": 600.00,
         "amount": random.randint(1, 3)},
        {"name": "Coffee Maker Nespresso", "space": 0.0200, "value": 450.00,
         "amount": random.randint(1, 3)},
    ]


def test_optimization() -> None:
    """
    Test the optimization service with sample data.

    Sends a POST request to the optimization endpoint with sample
    product data and prints the response.
    """
    products_json = create_sample_products()

    optimize_request = {
        "products": products_json,
        "limit": 3.0,
        "mutation_rate": 0.01,
        "number_generations": 100,
        "population_size": 200
    }

    try:
        response = requests.post(
            "http://localhost:8002/optimize/",
            json=optimize_request,
            timeout=30
        )
        response.raise_for_status()
        print("Optimization Results:")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error testing optimization: {e}")


if __name__ == "__main__":
    test_optimization()
