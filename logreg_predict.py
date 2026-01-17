import sys
import json
import utils
import numpy as np
from logreg_train import LogisticRegression


def parse_dataset_test(data):
    """Parse test dataset (without labels)."""
    header = data[0]
    rows = data[1:]

    # Identify valid feature columns (same as training)
    valid_cols = []
    for i, name in enumerate(header):
        if name not in ["Index", "First Name", "Last Name", "Birthday", "Hogwarts House"]:
            valid_cols.append(i)

    X = []
    for row in rows:
        if len(row) != len(header):
            continue
        features = []
        for i in valid_cols:
            try:
                features.append(float(row[i]))
            except:
                features.append(0.0)
        X.append(features)

    return np.array(X)


def load_model(model_file="model.json"):
    """Load trained model from JSON file."""
    try:
        with open(model_file, 'r') as f:
            model_data = json.load(f)
        
        model = LogisticRegression(
            lr=model_data['learning_rate'],
            iters=model_data['iterations']
        )
        
        model.thetas = np.array(model_data['weights'])
        model.mean = np.array(model_data['mean'])
        model.std = np.array(model_data['std'])
        model.polynomial_degree = model_data['polynomial_degree']
        model.label_mapping = model_data['label_mapping']
        model.inverse_mapping = {int(k): v for k, v in model_data['inverse_mapping'].items()}
        
        return model
    
    except FileNotFoundError:
        print(f"Error: Model file '{model_file}' not found!")
        print("Please train the model first using: python logreg_train.py datasets/dataset_train.csv")
        return None
    except KeyError as e:
        print(f"Error: Invalid model file format. Missing key: {e}")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def predict_houses(model, X):
    """Predict Hogwarts houses for students in X."""
    predictions_indices = model.predict(X)
    predictions_houses = [model.inverse_mapping[int(idx)] for idx in predictions_indices]
    return predictions_houses


def main():
    """
    Main function to predict using logistic regression model.
    The program creates houses.csv file.
    
    Output example of houses.csv:
        Index,Hogwarts House
        0,Gryffindor
        1,Hufflepuff
        2,Ravenclaw
        3,Hufflepuff
        4,Slytherin
        5,Ravenclaw
        6,Hufflepuff
        ...
    
    Evaluation: python evaluate.py
    will return something like:
        Your score on test set: 0.88
    
    The minimum score required is up to 0.98
    """
    
    if len(sys.argv) < 2:
        print("Usage: python logreg_predict.py datasets/dataset_test.csv")
        return 1
    
    # ------------------ Load model ------------------
    data_file = sys.argv[1]
    model = load_model()
    
    if model is None:
        return 1
    
    print("Model loaded successfully")
    print(f"  - Polynomial degree: {model.polynomial_degree}")
    print(f"  - Learning rate: {model.lr}")
    print(f"  - Iterations: {model.iters}")
    print(f"  - Classes: {list(model.label_mapping.keys())}\n")
    
    # ------------------ Load test data ------------------
    all_students = utils.lire_csv(data_file)
    
    if not all_students or len(all_students) < 2:
        print("Error: Data file is empty or invalid.")
        return 1
    
    X_test = parse_dataset_test(all_students)
    
    # ------------------ Make predictions ------------------
    predictions_houses = predict_houses(model, X_test)
    
    # ------------------ Save predictions ------------------
    lines = [["Index", "Hogwarts House"]]
    for i, house in enumerate(predictions_houses):
        lines.append([str(i), house])

    utils.ecrire_csv("houses.csv", lines)

    print(f"Predictions saved to houses.csv for {len(predictions_houses)} students")
    
    return 0


if __name__ == "__main__":
    main()