import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

def ejecutar_knn():
    print("--- EJERCICIO 3: K-NEAREST NEIGHBORS (KNN) ---")
    print("Cargando dataset de Reconocimiento de Vinos...")
    
    # Cargar datos
    vinos = datasets.load_wine()
    X = vinos.data
    y = vinos.target
    
    # Separar en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # KNN usa métricas de distancia (como Euclidiana). Si una característica va 
    # de 1 a 1000 y otra de 0.1 a 1.0, la primera dominará el cálculo de distancia.
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Evaluando diferentes valores de K (Vecinos) para balancear sesgo/varianza...")
    valores_k = range(1, 21)
    precisiones = []
    
    mejor_k = 1
    mejor_precision = 0
    
    for k in valores_k:
        # Inicializar y "entrenar" (memoria)
        knn = KNeighborsClassifier(n_neighbors=k, metric='euclidean')
        knn.fit(X_train_scaled, y_train)
        
        # Predecir
        predicciones = knn.predict(X_test_scaled)
        precision = accuracy_score(y_test, predicciones)
        precisiones.append(precision)
        
        if precision > mejor_precision:
            mejor_precision = precision
            mejor_k = k

    print(f"\nEl valor óptimo encontrado es K = {mejor_k} con una exactitud de {mejor_precision:.4f}")
    
    # Entrenar modelo final
    knn_final = KNeighborsClassifier(n_neighbors=mejor_k, metric='euclidean')
    knn_final.fit(X_train_scaled, y_train)
    
    print("\nEjemplo de Predicción (Primeros 5 registros de prueba):")
    print(f"Predicciones: {knn_final.predict(X_test_scaled[:5])}")
    print(f"Clases reales: {y_test[:5]}")
    
    print("\nConclusión: KNN es un algoritmo de 'Lazy Learning'. No optimiza pesos,")
    print("pero su inferencia se basa en la moda estadística de sus vecinos más cercanos.")

if __name__ == "__main__":
    ejecutar_knn()