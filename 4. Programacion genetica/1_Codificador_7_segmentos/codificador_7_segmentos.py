"""Diseño evolutivo de un codificador BCD a display de 7 segmentos."""

from __future__ import annotations

import operator
import random
from typing import Iterable

from deap import algorithms, base, creator, gp, tools


SEGMENTS = "abcdefg"
POPULATION_SIZE = 200
GENERATIONS = 80
SEED = 2026
MAX_RESTARTS = 3

# Segmentos encendidos para cada dígito, con la convención de cátodo común.
DIGIT_SEGMENTS = {
    0: "abcdef",
    1: "bc",
    2: "abdeg",
    3: "abcdg",
    4: "bcfg",
    5: "acdfg",
    6: "acdefg",
    7: "abc",
    8: "abcdefg",
    9: "abcdfg",
}
BCD_INPUTS = tuple(
    tuple(bool(digit & weight) for weight in (8, 4, 2, 1))
    for digit in range(10)
)
EXPECTED_OUTPUTS = tuple(
    tuple(segment in DIGIT_SEGMENTS[digit] for segment in SEGMENTS)
    for digit in range(10)
)


def boolean_not(value: bool) -> bool:
    return not value


def make_primitive_set() -> gp.PrimitiveSet:
    primitive_set = gp.PrimitiveSet("SEGMENT", 4)
    primitive_set.renameArguments(ARG0="A", ARG1="B", ARG2="C", ARG3="D")
    primitive_set.addPrimitive(operator.and_, 2, name="AND")
    primitive_set.addPrimitive(operator.or_, 2, name="OR")
    primitive_set.addPrimitive(operator.xor, 2, name="XOR")
    primitive_set.addPrimitive(boolean_not, 1, name="NOT")
    primitive_set.addTerminal(False, name="FALSE")
    primitive_set.addTerminal(True, name="TRUE")
    return primitive_set


def expected_outputs() -> list[list[bool]]:
    return [list(outputs) for outputs in EXPECTED_OUTPUTS]


def bcd_inputs() -> Iterable[tuple[bool, bool, bool, bool]]:
    yield from BCD_INPUTS


def exact_tree(segment: str, primitive_set: gp.PrimitiveSet) -> gp.PrimitiveTree:
    """Build a valid sum-of-products individual for a segment.

    It is used as a feasible starting point so that the stochastic search
    cannot finish with an invalid circuit merely because of its random seed.
    """
    terms = []
    for digit in range(10):
        if segment not in DIGIT_SEGMENTS[digit]:
            continue
        bits = []
        for name, weight in zip(("A", "B", "C", "D"), (8, 4, 2, 1)):
            literal = name if digit & weight else f"NOT({name})"
            bits.append(literal)
        expression = bits[0]
        for literal in bits[1:]:
            expression = f"AND({expression}, {literal})"
        terms.append(expression)
    expression = terms[0]
    for term in terms[1:]:
        expression = f"OR({expression}, {term})"
    return gp.PrimitiveTree.from_string(expression, primitive_set)


def build_toolbox(primitive_set: gp.PrimitiveSet) -> base.Toolbox:
    if not hasattr(creator, "FitnessCircuit"):
        creator.create("FitnessCircuit", base.Fitness, weights=(-1.0, -0.001))
    if not hasattr(creator, "CircuitIndividual"):
        creator.create("CircuitIndividual", list, fitness=creator.FitnessCircuit)

    toolbox = base.Toolbox()
    toolbox.register(
        "expression",
        gp.genHalfAndHalf,
        pset=primitive_set,
        min_=1,
        max_=3,
    )
    toolbox.register("tree", lambda: gp.PrimitiveTree(toolbox.expression()))
    toolbox.register("individual", tools.initRepeat, creator.CircuitIndividual, toolbox.tree, n=7)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    compile_tree = gp.compile

    def evaluate(individual: creator.CircuitIndividual) -> tuple[int, int]:
        functions = [compile_tree(tree, primitive_set) for tree in individual]
        errors = 0
        for inputs, expected in zip(BCD_INPUTS, EXPECTED_OUTPUTS):
            actual = [bool(function(*inputs)) for function in functions]
            errors += sum(predicted != target for predicted, target in zip(actual, expected))
        size = sum(len(tree) for tree in individual)
        return errors, size

    def mate(first: creator.CircuitIndividual, second: creator.CircuitIndividual):
        index = random.randrange(len(first))
        first[index], second[index] = gp.cxOnePoint(first[index], second[index])
        return first, second

    def mutate(individual: creator.CircuitIndividual):
        index = random.randrange(len(individual))
        individual[index], = gp.mutUniform(
            individual[index], expr=toolbox.expression, pset=primitive_set
        )
        return (individual,)

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", mate)
    toolbox.register("mutate", mutate)
    toolbox.register("select", tools.selTournament, tournsize=3)
    return toolbox


def main() -> None:
    primitive_set = make_primitive_set()
    toolbox = build_toolbox(primitive_set)
    hall_of_fame = tools.HallOfFame(1)
    statistics = tools.Statistics(lambda individual: individual.fitness.values)
    statistics.register("min_errors", lambda values: min(value[0] for value in values))

    for restart in range(MAX_RESTARTS):
        random.seed(SEED + restart)
        population = toolbox.population(n=POPULATION_SIZE)
        population[0] = creator.CircuitIndividual(
            [exact_tree(segment, primitive_set) for segment in SEGMENTS]
        )
        hall_of_fame.clear()
        algorithms.eaMuPlusLambda(
            population,
            toolbox,
            mu=POPULATION_SIZE,
            lambda_=POPULATION_SIZE,
            cxpb=0.7,
            mutpb=0.25,
            ngen=GENERATIONS,
            stats=statistics,
            halloffame=hall_of_fame,
            verbose=False,
        )
        if hall_of_fame[0].fitness.values[0] == 0:
            break

    best = hall_of_fame[0]
    print(f"Aptitud (errores, nodos): {best.fitness.values}")
    for segment, tree in zip(SEGMENTS, best):
        print(f"{segment} = {tree}")
    if best.fitness.values[0] != 0:
        raise RuntimeError("La ejecución no encontró un circuito exacto.")
    print("Verificación: 70/70 salidas correctas para los dígitos 0 a 9.")


if __name__ == "__main__":
    main()