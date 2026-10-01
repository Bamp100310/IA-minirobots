import numpy as np
import time
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def generar_dataset_matrices(num_muestras=50000):
    """
    Genera un dataset de multiplicaciones de matrices 2x2.
    Las entradas son 8 valores (-20 a 20) y las salidas son 4 valores.
    """
    print(f"Generando {num_muestras} muestras de matrices 2x2...")
    # Generamos matrices A y B con valores aleatorios enteros entre -20 y 20
    X = np.random.randint(-20, 21, size=(num_muestras, 8))
    Y = np.zeros((num_muestras, 4))

    for i in range(num_muestras):
        # Reconstruir las matrices A y B (2x2) desde el vector de 8 elementos
        A = X[i, 0:4].reshape(2, 2)
        B = X[i, 4:8].reshape(2, 2)
        # Multiplicación analítica exacta
        C = np.dot(A, B)
        # Aplanar la matriz resultante C (2x2) a un vector de 4 elementos
        Y[i] = C.flatten()
        
    return X, Y

if __name__ == "__main__":
    # Generar los datos
    X, y = generar_dataset_matrices(50000)
    
    # Dividir en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("\nEntrenando modelo de Machine Learning (MLPRegressor)...")
    print("Esto requiere calcular gradientes para miles de pesos durante varias épocas.")
    # Usamos una red neuronal multicapa simple para aproximar la función
    modelo_ml = MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=200, random_state=42)
    
    start_train = time.time()
    modelo_ml.fit(X_train, y_train)
    end_train = time.time()
    print(f"Tiempo de entrenamiento: {end_train - start_train:.4f} segundos")

    predicciones = modelo_ml.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predicciones))
    print(f"Error RMSE del modelo en validación: {rmse:.4f}")

    print("\n--- COMPARACIÓN: ML vs MÉTODO ANALÍTICO (10 Ejemplos) ---")
    X_nuevos, Y_reales = generar_dataset_matrices(10)
    
    # 1. Medir tiempo de Inferencia ML
    start_ml = time.perf_counter()
    Y_pred_ml = modelo_ml.predict(X_nuevos)
    end_ml = time.perf_counter()
    tiempo_ml = end_ml - start_ml

    # 2. Medir tiempo Analítico tradicional (dot product)
    start_analitico = time.perf_counter()
    for i in range(10):
        A = X_nuevos[i, 0:4].reshape(2, 2)
        B = X_nuevos[i, 4:8].reshape(2, 2)
        C = np.dot(A, B)
    end_analitico = time.perf_counter()
    tiempo_analitico = end_analitico - start_analitico

    print("\nResultados de Muestra (Primer ejemplo):")
    print(f"Matriz de entrada (A y B aplanadas): {X_nuevos[0]}")
    print(f"Resultado Analítico Exacto: {Y_reales[0]}")
    print(f"Resultado Predicho por ML:  {np.round(Y_pred_ml[0], 2)}")
    
    print("\n--- ANÁLISIS DE COSTO COMPUTACIONAL ---")
    print(f"Tiempo total método analítico (10 ejemplos): {tiempo_analitico:.6f} seg")
    print(f"Tiempo total inferencia ML (10 ejemplos):    {tiempo_ml:.6f} seg")
    print(f"Diferencia: El método de ML fue aproximadamente {tiempo_ml/tiempo_analitico:.1f} veces más lento en inferencia.")
    print("Conclusión: Usar ML para operaciones deterministas de álgebra lineal es ineficiente y agrega ruido innecesario.")