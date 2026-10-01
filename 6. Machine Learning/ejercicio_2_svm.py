import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

def ejecutar_svm():
    print("--- EJERCICIO 2: SUPPORT VECTOR MACHINE (SVM) ---")
    print("Cargando dataset de Cáncer de Mama (Wisconsin)...")
    
    # Cargar datos
    datos = datasets.load_breast_cancer()
    X = datos.data
    y = datos.target
    nombres_clases = datos.target_names # 0: maligno, 1: benigno
    
    # Dividir datos (80% entrenamiento, 20% prueba)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # SVM es altamente sensible a la escala de los datos debido a que maximiza 
    # la distancia geométrica (margen) entre puntos. Escalar es obligatorio.
    print("Escalando características para maximizar eficacia geométrica del margen...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("\n1. Entrenando SVM con Kernel Lineal (Espacio original)...")
    svm_lineal = SVC(kernel='linear', C=1.0, random_state=42)
    svm_lineal.fit(X_train_scaled, y_train)
    predicciones_lineal = svm_lineal.predict(X_test_scaled)
    
    print("Matriz de Confusión (Kernel Lineal):")
    print(confusion_matrix(y_test, predicciones_lineal))
    print(f"Exactitud: {svm_lineal.score(X_test_scaled, y_test):.4f}")

    print("\n2. Entrenando SVM con Kernel RBF (Espacio de alta dimensión)...")
    # El Kernel RBF (Radial Basis Function) permite trazar fronteras curvas 
    # mapeando los datos implícitamente a infinitas dimensiones (Kernel Trick).
    svm_rbf = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
    svm_rbf.fit(X_train_scaled, y_train)
    predicciones_rbf = svm_rbf.predict(X_test_scaled)
    
    print("Matriz de Confusión (Kernel RBF):")
    print(confusion_matrix(y_test, predicciones_rbf))
    print(f"Exactitud: {svm_rbf.score(X_test_scaled, y_test):.4f}")
    
    print("\nReporte de Clasificación Final (Modelo RBF):")
    print(classification_report(y_test, predicciones_rbf, target_names=nombres_clases))
    print("Conclusión: SVM es un algoritmo robusto. Gracias al escalado y los Kernels, ")
    print("puede aislar eficazmente características críticas (Vectores de Soporte).")

if __name__ == "__main__":
    ejecutar_svm()