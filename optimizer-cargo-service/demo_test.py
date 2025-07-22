import requests
import random

products_json = [
    {"name": "Smart Fridge LG", "space": 0.720, "value": 1050.00, "amount": random.randint(1, 3)},
    {"name": "Samsung Galaxy S21", "space": 0.000095, "value": 3200.00, "amount": random.randint(1, 3)},
    {"name": "Smart TV 60'' Philips", "space": 0.410, "value": 4700.00, "amount": random.randint(1, 3)},
    {"name": "Smart TV 48'' Sony", "space": 0.280, "value": 3800.00, "amount": random.randint(1, 3)},
    {"name": "Smart TV 40'' TCL", "space": 0.190, "value": 2500.00, "amount": random.randint(1, 3)},
    {"name": "Notebook HP", "space": 0.00380, "value": 2700.00, "amount": random.randint(1, 3)},
    {"name": "Fan Arno Turbo", "space": 0.480, "value": 210.00, "amount": random.randint(1, 3)},
    {"name": "Microwave Brastemp", "space": 0.0450, "value": 350.00, "amount": random.randint(1, 3)},
    {"name": "Microwave Samsung", "space": 0.0500, "value": 410.00, "amount": random.randint(1, 3)},
    {"name": "Microwave Midea", "space": 0.0300, "value": 280.00, "amount": random.randint(1, 3)},
    {"name": "Fridge Electrolux", "space": 0.600, "value": 900.00, "amount": random.randint(1, 3)},
    {"name": "Fridge Consul Frost", "space": 0.800, "value": 1300.00, "amount": random.randint(1, 3)},
    {"name": "Notebook Acer", "space": 0.500, "value": 2100.00, "amount": random.randint(1, 3)},
    {"name": "Notebook Apple MacBook Air", "space": 0.520, "value": 5200.00, "amount": random.randint(1, 3)},
    {"name": "Tablet Samsung Tab S7", "space": 0.000050, "value": 1800.00, "amount": random.randint(1, 3)},
    {"name": "Air Conditioner LG", "space": 0.650, "value": 2200.00, "amount": random.randint(1, 3)},
    {"name": "Washing Machine Panasonic", "space": 0.900, "value": 1800.00, "amount": random.randint(1, 3)},
    {"name": "Dryer Electrolux", "space": 0.700, "value": 1500.00, "amount": random.randint(1, 3)},
    {"name": "Bluetooth Speaker JBL", "space": 0.000030, "value": 600.00, "amount": random.randint(1, 3)},
    {"name": "Coffee Maker Nespresso", "space": 0.0200, "value": 450.00, "amount": random.randint(1, 3)},
]

optimize_request = {
    "products": products_json,
    "limit": 3.0,
    "mutation_rate": 0.01,
    "number_generations": 100,
    "population_size": 200
}

response = requests.post(
    "http://localhost:8000/optimize/",
    json=optimize_request
)
print(response.json())
