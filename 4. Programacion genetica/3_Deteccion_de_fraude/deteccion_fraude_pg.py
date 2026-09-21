"""Deteccion de fraude mediante Programacion Genetica con DEAP."""

from __future__ import annotations

import operator
import random
from pathlib import Path

import numpy as np
import pandas as pd
from deap import algorithms, base, creator, gp, tools
from sklearn.metrics import classification_report, confusion_matrix, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split


SEED = 2026
POPULATION_SIZE = 250
GENERATIONS = 50
MAX_TREE_HEIGHT = 7
DATA_PATH = Path(__file__).parent / "data" / "transacciones_limpias.csv"
TERMINALS = [
    "monto_alto",
    "hora_inusual",
    "distancia_lejana",
    "ingreso_bajo",
    "monto_muy_alto",
]


def boolean_not(value: bool) -> bool:
    return not value


def build_features(data: pd.DataFrame) -> np.ndarray:
    """Convert numeric variables into interpretable boolean risk indicators."""
    amount_ratio = data["monto_pesos"] / data["ingreso_mensual_pesos"]
    return np.column_stack(
        [
            (amount_ratio >= 0.20),
            ((data["hora_dia"] <= 5) | (data["hora_dia"] >= 23)),
            (data["distancia_residencia_km"] >= 20),
            (data["ingreso_mensual_pesos"] <= 1_800_000),
            (amount_ratio >= 0.50),
        ]
    ).astype(bool)


def build_primitive_set() -> gp.PrimitiveSet:
    primitive_set = gp.PrimitiveSet("FRAUD_RULE", len(TERMINALS))
    for index, name in enumerate(TERMINALS):
        primitive_set.renameArguments(**{f"ARG{index}": name})
    primitive_set.addPrimitive(operator.and_, 2, name="AND")
    primitive_set.addPrimitive(operator.or_, 2, name="OR")
    primitive_set.addPrimitive(operator.xor, 2, name="XOR")
    primitive_set.addPrimitive(boolean_not, 1, name="NOT")
    return primitive_set


def build_toolbox(primitive_set: gp.PrimitiveSet, train_x: np.ndarray, train_y: np.ndarray) -> base.Toolbox:
    if not hasattr(creator, "FraudFitness"):
        creator.create("FraudFitness", base.Fitness, weights=(-1.0, -0.01))
    if not hasattr(creator, "FraudIndividual"):
        creator.create("FraudIndividual", gp.PrimitiveTree, fitness=creator.FraudFitness)

    toolbox = base.Toolbox()
    toolbox.register("expression", gp.genHalfAndHalf, pset=primitive_set, min_=1, max_=3)
    toolbox.register("individual", tools.initIterate, creator.FraudIndividual, toolbox.expression)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluate(individual: creator.FraudIndividual) -> tuple[float, float]:
        rule = gp.compile(individual, primitive_set)
        predictions = np.array([bool(rule(*row)) for row in train_x], dtype=int)
        false_negatives = np.sum((train_y == 1) & (predictions == 0))
        false_positives = np.sum((train_y == 0) & (predictions == 1))
        weighted_errors = 2 * false_negatives + false_positives
        return float(weighted_errors), float(len(individual))

    toolbox.register("evaluate", evaluate)
    toolbox.register("select", tools.selTournament, tournsize=4)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=primitive_set)
    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=MAX_TREE_HEIGHT))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=MAX_TREE_HEIGHT))
    return toolbox


def main() -> None:
    random.seed(SEED)
    np.random.seed(SEED)
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "No existe data/transacciones_limpias.csv. Ejecute primero deteccion_fraude.py."
        )

    data = pd.read_csv(DATA_PATH)
    features = build_features(data)
    labels = data["fraude"].to_numpy(dtype=int)
    train_x, test_x, train_y, test_y = train_test_split(
        features,
        labels,
        test_size=0.25,
        random_state=SEED,
        stratify=labels,
    )

    primitive_set = build_primitive_set()
    toolbox = build_toolbox(primitive_set, train_x, train_y)
    population = toolbox.population(n=POPULATION_SIZE)
    hall_of_fame = tools.HallOfFame(1)
    algorithms.eaSimple(
        population,
        toolbox,
        cxpb=0.7,
        mutpb=0.25,
        ngen=GENERATIONS,
        halloffame=hall_of_fame,
        verbose=False,
    )

    best = hall_of_fame[0]
    rule = gp.compile(best, primitive_set)
    predictions = np.array([bool(rule(*row)) for row in test_x], dtype=int)
    print(f"Regla encontrada: {best}")
    print(f"Tamano de la regla: {len(best)} nodos")
    print(f"ROC-AUC: {roc_auc_score(test_y, predictions):.3f}")
    print(f"F1 de fraude: {f1_score(test_y, predictions, zero_division=0):.3f}")
    print("Matriz de confusion [real x predicho]:")
    print(confusion_matrix(test_y, predictions))
    print("Reporte de clasificacion:")
    print(classification_report(test_y, predictions, target_names=["No fraude", "Fraude"], zero_division=0))


if __name__ == "__main__":
    main()
