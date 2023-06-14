"""
Unit with randomized attributes.

@author "Dániel Lajos Mizsák" <info@pythonvilag.hu>
"""

import random

import config as cfg


class Unit:
    def __init__(self, order: int, number: int):
        colors = cfg.UNIT_COLORS
        shapes = cfg.UNIT_SHAPES
        used_colors = []

        self.background_color = random.choice(colors)
        used_colors.append(self.background_color)
        self.shape_color = random.choice([c for c in colors if c not in used_colors])
        used_colors.append(self.shape_color)
        self.text_color = random.choice([c for c in colors if c not in used_colors])
        used_colors.append(self.text_color)
        self.number_color = random.choice([c for c in colors if c not in used_colors])

        self.color_text = random.choice(colors)
        self.shape_text = random.choice(shapes)
        self.shape = random.choice(shapes)
        self.number = number
        self.order = order

    def __repr__(self) -> str:
        return f"Unit(order={self.order}, background_color={self.background_color})"


def create_units(unit_number: int = cfg.UNIT_NUMBER) -> tuple[Unit, ...]:
    numbers = [i + 1 for i in range(unit_number)]
    order = random.sample(numbers, len(numbers))
    number = random.sample(numbers, len(numbers))

    units = tuple(Unit(order[num], number[num]) for num in range(len(order)))
    return units


def create_task(units: tuple[Unit], task_number: int = 2) -> tuple[str, str]:
    selected_units = random.sample(units, task_number)
    task_text = "Enter the "
    solution_text = ""

    for unit in selected_units:
        unavailable_attributes = ["order", "number"]
        unit_attributes = [v for v in vars(unit).items() if v[0] not in unavailable_attributes]
        task, solution = random.sample(unit_attributes, 1)[0]

        task_text += f'{task.replace("_", " ")} ({unit.order}) and '
        solution_text += f"{solution} "

    task_text = task_text[:-5].upper()
    solution_text = solution_text[:-1].lower()

    return task_text, solution_text


if __name__ == "__main__":
    pass
