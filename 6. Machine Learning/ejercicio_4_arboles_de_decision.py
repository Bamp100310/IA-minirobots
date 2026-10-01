import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import urllib.error

def obtener_datos_gubernamentales():
    """
    Intenta descargar datos de COVID-19/Salud desde Datos Abiertos Colombia (API Socrata).
    Usa un fallback en caso de bloqueo de red (común en entornos locales/laboratorios).
    """
    url_datos = "https://www.datos.gov.co/resource/gt2j-8ykr.csv?$limit=1000"
    print(f"Conectando a Datos Abiertos Colombia: {url_datos} ...")
    
    try:
        df = pd.read_csv(url_datos)
        print("¡Datos descargados exitosamente desde la web!")
        # Seleccionar características relevantes para el problema (simplificado)
        df = df[['edad', 'sexo', 'tipo_recuperacion', 'estado']]
        df = df.dropna()
        return df
    except Exception as e:
        print(f"Aviso: No se pudo conectar a internet o la API cambió ({e}).")
        print("Generando dataset mock estadísticamente representativo (Datos Gov Colombia)...")
        # Fallback: Dataset emulado que refleja la estructura demográfica
        np.random.seed(42)
        n_mock = 500
        edades = np.random.randint(5, 90, n_mock)
        sexos = np.random.choice(['F', 'M'], n_mock)
        # Lógica simulada: mayores de 65 tienen mayor prob. de estado severo
        estados = ['Fallecido' if (e > 65 and np.random.rand() > 0.6) else 'Recuperado' for e in edades]
        
        df = pd.DataFrame({'edad': edades, 'sexo': sexos, 'estado': estados})
        return df

def ejecutar_arbol_decision():
    print("--- EJERCICIO 4: ÁRBOLES DE DECISIÓN (DATOS GOV.CO) ---")
    
    df = obtener_datos_gubernamentales()
    print("\nMuestra de los datos obtenidos:")
    print(df.head())
    
    # Preprocesamiento: Convertir variables categóricas a numéricas
    print("\nCodificando variables categóricas (Label Encoding)...")
    encoder_sexo = LabelEncoder()
    df['sexo_enc'] = encoder_sexo.fit_transform(df['sexo'])
    
    # Definir X (características) e y (rótulo objetivo)
    X = df[['edad', 'sexo_enc']]
    y = df['estado']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    print("Entrenando Árbol de Decisión (max_depth=3 para evitar sobreajuste)...")
    # Limitamos la profundidad para mantener el modelo interpretable (Caja Blanca)
    arbol = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)
    arbol.fit(X_train, y_train)
    
    predicciones = arbol.predict(X_test)
    exactitud = accuracy_score(y_test, predicciones)

    print(f"\nExactitud del Árbol de Decisión: {exactitud:.4f}")
    print("\nReporte de Clasificación:")
    print(classification_report(y_test, predicciones))
    
    print("\n--- REGLAS LÓGICAS (INTERPRETABILIDAD) ---")
    reglas = export_text(arbol, feature_names=['edad', 'sexo_enc'])
    print(reglas)
    
    print("Conclusión: Los árboles construyen particiones jerárquicas del dataset.")
    print("Su interpretabilidad permite extraer reglas claras (ej: si edad > X).")

if __name__ == "__main__":
    ejecutar_arbol_decision()