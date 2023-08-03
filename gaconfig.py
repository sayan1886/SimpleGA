from typing import Any
from dataclasses import dataclass

@dataclass
class Boundary:
    min: float
    max: float

    @staticmethod
    def from_dict(obj: Any) -> 'Boundary':
        _min = float(obj.get("min"))
        _max = float(obj.get("max"))
        return Boundary(_min, _max)
    
@dataclass
class Elitism:
    capacity: float

    @staticmethod
    def from_dict(obj: Any) -> 'Elitism':
        _capacity = float(obj.get("capacity"))
        return Elitism(_capacity)
    
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
        _size = int(obj.get("size")) if obj.get("size") is not None else 0
        return Selection(_type, _size)

@dataclass
class GAConfig:
    boundary: Boundary
    crossover_chances: float
    crossover_type: str
    n_generation: int
    elitism: Any
    mutation_chances: float
    mutation: Mutation
    n_chromosomes: int
    n_gene: int
    n_populations: int
    objective: str
    plot_type: str
    selection: Selection

    @staticmethod
    def from_dict(obj: Any) -> 'GAConfig':
        _boundary = Boundary.from_dict(obj.get("boundary"))
        _crossover_chances = float(obj.get("crossover_chances"))
        _crossover_type = str(obj.get("crossover_type"))
        _elitism = Elitism.from_dict(
                    obj.get("elitism")) if obj.get("elitism") is not None else None
        _mutation_chances = float(obj.get("mutation_chances"))
        _mutation = Mutation.from_dict(obj.get("mutation"))
        _n_chromosomes = int(obj.get("n_chromosomes"))
        _n_gene = int(obj.get("n_gene"))
        _n_generation = int(obj.get("n_generation"))
        _n_populations = int(obj.get("n_populations"))
        _objective = str(obj.get("objective"))
        _plot_type = str(obj.get("plot_type"))
        _selection = Selection.from_dict(obj.get("selection"))
        return GAConfig(boundary=_boundary, 
                        crossover_chances=_crossover_chances, 
                        crossover_type=_crossover_type,
                        elitism=_elitism, mutation=_mutation, 
                        mutation_chances=_mutation_chances,
                        n_chromosomes=_n_chromosomes, n_gene= _n_gene,
                        n_generation=_n_generation, 
                        n_populations=_n_populations,objective=_objective, 
                        plot_type=_plot_type ,selection=_selection)


