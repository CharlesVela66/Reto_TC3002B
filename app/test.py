import joblib
from pygments.lexers import JavaLexer
from pygments import lex
from pygments.token import Token
import sys
import os

def extract_tokens(code):
    lexer = JavaLexer()
    tokens = []
    for ttype, value in lex(code, lexer):
        if ttype in Token.Name or ttype in Token.Keyword or ttype in Token.Operator:
            val = value.strip()
            if val:
                tokens.append(f"{ttype.__class__.__name__}:{val}")
    return " ".join(tokens)

def predict_similarity(file1, file2, model_path='rf_model.pkl'):
    """
    Predice la similitud entre dos archivos de código Java.

    Args:
        file1 (str): Ruta al primer archivo Java.
        file2 (str): Ruta al segundo archivo Java.
        model_path (str): Ruta al modelo entrenado.

    Returns:
        tuple: (score, is_similar)
    """
    model = joblib.load(model_path)
    vectorizer = joblib.load(model_path.replace('.pkl', '_vectorizer.pkl'))

    # Leer los archivos
    try:
        with open(file1, 'r', encoding='utf-8') as f:
            code1 = f.read()

        with open(file2, 'r', encoding='utf-8') as f:
            code2 = f.read()
    except Exception as e:
        print(f"Error al leer los archivos: {e}")
        return None, None

    # Extraer tokens
    t1 = extract_tokens(code1)
    t2 = extract_tokens(code2)
    token_pair = f"{t1} {t2}"

    # Vectorizar
    X = vectorizer.transform([token_pair])

    # Predecir
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(X.toarray())[0]
        similarity_score = proba[1] if len(proba) > 1 else proba[0]
    else:
        prediction = model.predict(X.toarray())[0]
        similarity_score = float(prediction)

    is_similar = similarity_score >= 0.5

    return similarity_score, is_similar

if __name__ == "__main__":
    # Verificar argumentos
    if len(sys.argv) < 3:
        print("Uso: python predictor.py archivo1.java archivo2.java [ruta_al_modelo]")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    model_path = 'rf_model.pkl'

    # Verificar que los archivos existen
    if not os.path.exists(file1):
        print(f"Error: El archivo {file1} no existe.")
        sys.exit(1)

    if not os.path.exists(file2):
        print(f"Error: El archivo {file2} no existe.")
        sys.exit(1)

    # Verificar que el modelo existe
    if not os.path.exists(model_path):
        print(f"Error: El modelo {model_path} no existe.")
        sys.exit(1)

    # Predecir similitud
    score, is_similar = predict_similarity(file1, file2, model_path)

    # Imprimir resultados
    if score is not None:
        print(f"Archivo 1: {file1}")
        print(f"Archivo 2: {file2}")
        print(f"Puntuación de similitud: {score:.4f}")
        print(f"¿Son similares?: {'Sí' if is_similar else 'No'}")