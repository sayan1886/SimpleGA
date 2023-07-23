from typing import Any
from dataclasses import dataclass

@dataclass
class Boundary:
    min: int
    max: int

    @staticmethod
    def from_dict(obj: Any) -> 'Boundary':
        _min = int(obj.get("min"))
        _max = int(obj.get("max"))
        return Boundary(_min, _max)
    
@dataclass
class Mutation:
    type: str
    bits: int

    @staticmethod
    def from_dict(obj: Any) -> 'Mutation':
        _type = str(obj.get("type"))
        _bits = int(obj.get("bits"))
        return Mutation(_type, _bits)
    
@dataclass
class Selection:
    type: str
    size: int

    @staticmethod
    def from_dict(obj: Any) -> 'Selection':
        _type = str(obj.get("type"))
        _size = int(obj.get("size"))
        return Selection(_type, _size)

@dataclass
class GAConfig:
    boundary: Boundary
    crossover_chances: float
    crossover_type: str
    objective: str
    generation_threshold: int
    mutation_chances: float
    mutation: Mutation
    n_chromosomes: int
    n_populations: int
    selection: Selection

    @staticmethod
    def from_dict(obj: Any) -> 'GAConfig':
        _boundary = Boundary.from_dict(obj.get("boundary"))
        _crossover_chances = float(obj.get("crossover_chances"))
        _crossover_type = str(obj.get("crossover_type"))
        _objective = str(obj.get("objective"))
        _generation_threshold = int(obj.get("generation_threshold"))
        _mutation_chances = float(obj.get("mutation_chances"))
        _mutation = Mutation.from_dict(obj.get("mutation"))
        _n_chromosomes = int(obj.get("n_chromosomes"))
        _n_populations = int(obj.get("n_populations"))
        _selection = Selection.from_dict(obj.get("selection"))
        return GAConfig(_boundary, _crossover_chances, _crossover_type,
                        _objective, _generation_threshold, _mutation_chances, 
                        _mutation, _n_chromosomes, _n_populations, _selection)


