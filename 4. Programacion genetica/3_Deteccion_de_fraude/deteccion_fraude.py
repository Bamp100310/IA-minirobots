"""Generacion de datos y deteccion de transacciones potencialmente fraudulentas."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


SEED = 2026
N_TRANSACTIONS = 5000
RANDOM_STATE = np.random.default_rng(SEED)
FEATURES = ["monto_pesos", "hora_dia", "distancia_residencia_km", "ingreso_mensual_pesos"]
TARGET = "fraude"
OUTPUT_DIR = Path(__file__).parent / "data"


def generate_raw_data(n_rows: int = N_TRANSACTIONS) -> pd.DataFrame:
    """Create a synthetic transaction file with realistic correlations and noise."""
    income = np.clip(RANDOM_STATE.lognormal(np.log(2_800_000), 0.55, n_rows), 900_000, 15_000_000)
    hour_probabilities = np.array(
        [0.01, 0.005, 0.004, 0.004, 0.005, 0.01, 0.025, 0.05,
         0.07, 0.07, 0.07, 0.07, 0.08, 0.08, 0.075, 0.07,
         0.065, 0.06, 0.06, 0.05, 0.04, 0.03, 0.02, 0.011]
    )
    hour_probabilities /= hour_probabilities.sum()
    hour = RANDOM_STATE.choice(
        np.arange(24),
        size=n_rows,
        p=hour_probabilities,
    )
    distance = np.clip(RANDOM_STATE.gamma(shape=2.0, scale=4.0, size=n_rows), 0.1, 80)
    amount = np.clip(
        income * RANDOM_STATE.lognormal(np.log(0.025), 0.9, n_rows),
        5_000,
        8_000_000,
    )

    night = ((hour <= 5) | (hour >= 23)).astype(float)
    high_amount = (amount / income > 0.20).astype(float)
    far_away = (distance > 20).astype(float)
    risk_score = -4.2 + 2.2 * night + 1.7 * high_amount + 1.1 * far_away
    risk_score += 0.8 * (amount / income > 0.50)
    fraud_probability = 0.01 + 0.45 / (1 + np.exp(-risk_score))
    fraud = RANDOM_STATE.binomial(1, fraud_probability)

    data = pd.DataFrame(
        {
            "monto_pesos": np.rint(amount),
            "hora_dia": hour,
            "distancia_residencia_km": np.round(distance, 2),
            "ingreso_mensual_pesos": np.rint(income),
            "fraude": fraud,
        }
    )

    # Simulate common problems in an initially collected file.
    missing_rows = RANDOM_STATE.choice(n_rows, size=round(n_rows * 0.01), replace=False)
    data.loc[missing_rows, "distancia_residencia_km"] = np.nan
    duplicate_rows = data.sample(round(n_rows * 0.01), random_state=SEED)
    return pd.concat([data, duplicate_rows], ignore_index=True)


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Clean the generated file and enforce plausible domain constraints."""
    clean = data.drop_duplicates().copy()
    clean["hora_dia"] = clean["hora_dia"].round().clip(0, 23)
    clean["monto_pesos"] = clean["monto_pesos"].clip(5_000, 8_000_000)
    clean["distancia_residencia_km"] = clean["distancia_residencia_km"].clip(0.1, 80)
    clean["ingreso_mensual_pesos"] = clean["ingreso_mensual_pesos"].clip(900_000, 15_000_000)
    clean["distancia_residencia_km"] = clean["distancia_residencia_km"].fillna(
        clean["distancia_residencia_km"].median()
    )
    clean[TARGET] = clean[TARGET].astype(int).clip(0, 1)
    return clean.reset_index(drop=True)


def build_model() -> Pipeline:
    preprocess = ColumnTransformer(
        [("numeric", StandardScaler(), FEATURES)],
        remainder="drop",
    )
    return Pipeline(
        [
            ("preprocess", preprocess),
            (
                "classifier",
                LogisticRegression(class_weight="balanced", max_iter=1000, random_state=SEED),
            ),
        ]
    )


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    raw_data = generate_raw_data()
    clean = clean_data(raw_data)
    raw_path = OUTPUT_DIR / "transacciones_raw.csv"
    clean_path = OUTPUT_DIR / "transacciones_limpias.csv"
    raw_data.to_csv(raw_path, index=False)
    clean.to_csv(clean_path, index=False)

    train, test = train_test_split(
        clean,
        test_size=0.25,
        random_state=SEED,
        stratify=clean[TARGET],
    )
    model = build_model()
    model.fit(train[FEATURES], train[TARGET])
    probabilities = model.predict_proba(test[FEATURES])[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    print(f"Archivo inicial: {raw_path} ({len(raw_data)} filas)")
    print(f"Archivo revisado: {clean_path} ({len(clean)} filas)")
    print(f"Tasa de fraude: {clean[TARGET].mean():.2%}")
    print(f"ROC-AUC: {roc_auc_score(test[TARGET], probabilities):.3f}")
    print(f"Average precision: {average_precision_score(test[TARGET], probabilities):.3f}")
    print("\nMatriz de confusion [real x predicho]:")
    print(confusion_matrix(test[TARGET], predictions))
    print("\nReporte de clasificacion:")
    print(classification_report(test[TARGET], predictions, target_names=["No fraude", "Fraude"], zero_division=0))

    examples = pd.DataFrame(
        {
            "monto_pesos": [120_000, 2_500_000],
            "hora_dia": [14, 2],
            "distancia_residencia_km": [2, 45],
            "ingreso_mensual_pesos": [3_000_000, 2_000_000],
        }
    )
    examples["probabilidad_fraude"] = model.predict_proba(examples[FEATURES])[:, 1].round(3)
    examples["prediccion"] = np.where(examples["probabilidad_fraude"] >= 0.5, "Sí", "No")
    print("Ejemplos de prediccion:")
    print(examples.to_string(index=False))


if __name__ == "__main__":
    main()
