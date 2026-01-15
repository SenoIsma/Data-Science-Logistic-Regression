import utils, maths, sys
import random, math
from itertools import combinations_with_replacement

def parse_dataset(data):
    header = data[0]
    rows = data[1:]

    label_index = header.index("Hogwarts House")

    # Colonnes numériques valides
    valid_cols = []
    for i, name in enumerate(header):
        if i == label_index:
            continue
        if name not in ["Index", "First Name", "Last Name", "Birthday"]:
            valid_cols.append(i)

    X = []
    y = []

    for row in rows:
        if len(row) != len(header):
            continue

        y.append(row[label_index])

        features = []
        for i in valid_cols:
            try:
                features.append(float(row[i]))
            except:
                features.append(0.0)  # valeur manquante

        X.append(features)

    return X, y


def encode_labels(y):
    houses = list(set(y))
    mapping = {house: i for i, house in enumerate(houses)}

    y_encoded = [mapping[label] for label in y]

    return y_encoded, mapping

def data_spliter(x, y, proportion):
    """
        Shuffles and splits the dataset (given by x and y) into a training and a test set,
        while respecting the given proportion of examples to be kept in the training set.
    """
    if not isinstance(x, list) or not isinstance(y, list):
        return None
    if len(x) == 0 or len(y) == 0:
        return None
    if len(x) != len(y):
        return None
    if not isinstance(proportion, float) or not (0 < proportion < 1):
        return None

    m = len(x)

    # Création et mélange des indices
    indices = list(range(m))
    random.shuffle(indices)

    # Shuffle des données
    x_shuffled = [x[i] for i in indices]
    y_shuffled = [y[i] for i in indices]

    # Découpage
    train_size = int(m * proportion)

    x_train = x_shuffled[:train_size]
    x_test = x_shuffled[train_size:]
    y_train = y_shuffled[:train_size]
    y_test = y_shuffled[train_size:]

    return x_train, x_test, y_train, y_test


def add_polynomial_features(x, power):
    """
        Add polynomial features to matrix X for all columns and all combinations up to 'power'.
    """
    if not isinstance(x, list) or len(x) == 0:
        return None
    if not all(isinstance(row, list) for row in x):
        return None
    if not isinstance(power, int) or power < 1:
        return None

    m = len(x)
    n = len(x[0])

    # Vérifier que toutes les lignes ont la même taille
    if not all(len(row) == n for row in x):
        return None

    X_poly = [[] for _ in range(m)]

    for p in range(1, power + 1):
        for comb in combinations_with_replacement(range(n), p):
            # Calcul du produit pour chaque ligne
            for i in range(m):
                prod = 1
                for idx in comb:
                    prod *= x[i][idx]
                X_poly[i].append(prod)

    return X_poly

def normalize_features(x):
        """
            Normalize features in X.
        """
        if not isinstance(x, list) or len(x) == 0:
            return None
        # mean = maths.mean(x, axis=0)
        # std = maths.std(x, axis=0)
        m = len(x)
        n = len(x[0])
        # Calcul des moyennes
        mean = []
        for j in range(n):
            col_sum = 0
            for i in range(m):
                col_sum += x[i][j]
            mean.append(col_sum / m)
        # Calcul des écarts-types
        std = []
        for j in range(n):
            var = 0
            for i in range(m):
                var += (x[i][j] - mean[j]) ** 2
            std.append(math.sqrt(var / m))
        # Normalisation
        X_norm = []
        for i in range(m):
            row = []
            for j in range(n):
                if std[j] == 0:
                    row.append(0)  # éviter division par 0
                else:
                    row.append((x[i][j] - mean[j]) / std[j])
            X_norm.append(row)

        return X_norm, mean, std

def apply_normalization(x, mean, std):
    X_norm = []
    for row in x:
        new_row = []
        for j in range(len(row)):
            if std[j] == 0:
                new_row.append(0)
            else:
                new_row.append((row[j] - mean[j]) / std[j])
        X_norm.append(new_row)
    return X_norm

def sigmoid(z):
    """Compute the sigmoid function."""
    if isinstance(z, list):
        return [1 / (1 + math.exp(-zi)) for zi in z]
    else:
        return 1 / (1 + math.exp(-z))

def fit_one_vs_all(x, y, num_labels, learning_rate=0.01, num_iterations=1000):
    """
        Trains multiple logistic regression classifiers using one-vs-all strategy.
    """
    if not isinstance(x, list) or len(x) == 0:
        return None
    if not isinstance(y, list) or len(y) == 0:
        return None
    if len(x) != len(y):
        return None
    if not isinstance(num_labels, int) or num_labels < 2:
        return None

    m = len(x)
    n = len(x[0])
    all_weights = []

    for label in range(num_labels):
        # Initialiser les poids
        weights = [0.0] * n

        # Convertir y en vecteur binaire pour la classe actuelle
        y_binary = [1 if yi == label else 0 for yi in y]

        x_T = maths.transpose_matrix(x)

        # Gradient descent
        for iteration in range(num_iterations):
            predictions = sigmoid(maths.mat_vec_dot(x, weights))
            errors = [predictions[i] - y_binary[i] for i in range(m)]
            gradient = maths.mat_vec_dot(x_T, errors)
            weights = [weights[j] - (learning_rate / m) * gradient[j] for j in range(n)]

        all_weights.append(weights)

    return all_weights

def main():
    """
        Main function to train logistic regression model.
        The program create weights.csv file.
        It contains the weights that will be used for the prediction.
    """

    if len(sys.argv) < 2:
        print("Usage: python logreg_train.py datasets/dataset_train.csv")
        return 1
    
    # ------------------ Load data ------------------
    file = sys.argv[1]
    all_students = utils.lire_csv(file)

    if not all_students or len(all_students) < 2:
        print("Data file can be empty or invalid.")
        return 1

    # ------------------ Split data ------------------
    X, y = parse_dataset(all_students)
    y_encoded, mapping = encode_labels(y)
    x_train, x_test, y_train, y_test = data_spliter(
        X, y_encoded, 0.8
    )

    # ------------------ Polynomial features ------------------
    x_train_poly = add_polynomial_features(x_train, 2)
    x_test_poly = add_polynomial_features(x_test, 2)

    # ------------------ Feature normalization ------------------
    x_train_norm, mean, std = normalize_features(x_train_poly)
    x_test_norm = apply_normalization(x_test_poly, mean, std)

    # ------------------ One-vs-all training ------------------
    num_labels = len(set(y_train))
    weights = fit_one_vs_all(x_train_norm, y_train, num_labels, learning_rate=0.1, num_iterations=300)

    # ------------------ Save weights to CSV ------------------
    utils.ecrire_csv("weights.csv", weights)

    return 0

if __name__ == "__main__":
    main()