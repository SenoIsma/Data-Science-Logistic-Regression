import sys
import utils
import numpy as np
from itertools import combinations_with_replacement

def parse_dataset(data):
    header = data[0]
    rows = data[1:]

    label_index = header.index("Hogwarts House")

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
                features.append(0.0)
        X.append(features)

    return np.array(X), np.array(y)


def encode_labels(y):
    houses = list(set(y)) # set -> créé un ensemble unique et list -> convertit en liste
    mapping = {house: i for i, house in enumerate(houses)} # dictionnaire de mappage
    y_encoded = np.array([mapping[label] for label in y])
    return y_encoded, mapping


def data_spliter(X, y, proportion):
    if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray) or not isinstance(proportion, float):
        return None
    if X.ndim != 2 or y.ndim != 1:
        return None
    if len(X) == 0 or len(y) == 0 or len(X) != len(y):
        return None
    if proportion <= 0 or proportion >= 1:
        return None
    m = len(X)
    indices = np.random.permutation(m) # melange les indices
    train_size = int(m * proportion)
    train_idx = indices[:train_size] # stock les proportion des premiers indices pour le train
    test_idx = indices[train_size:] # stock les proportion des derniers indices pour le test

    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


def add_polynomial_features(X, power):
    """
        Add polynomial features to matrix X for all columns and all combinations up to 'power'.
    """
    if not isinstance(X, np.ndarray) or not isinstance(power, int):
        return None
    if X.ndim != 2 or X.shape[0] == 0:
        return None
    if power < 1:
        return None
    m, n = X.shape
    features = []
    for p in range(1, power + 1):
        for comb in combinations_with_replacement(range(n), p):
            prod = np.ones(m)
            for idx in comb:
                prod *= X[:, idx]
            features.append(prod)

    return np.column_stack(features)


def normalize_features(X):
    """
        Normalize features in X.
    """
    if not isinstance(X, np.ndarray):
        return None
    if X.ndim != 2 or X.shape[0] == 0:
        return None
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)

    std[std == 0] = 1  # éviter division par 0
    X_norm = (X - mean) / std

    return X_norm, mean, std

def apply_normalization(X, mean, std):
    if not isinstance(X, np.ndarray)or  not isinstance(mean, np.ndarray) or not isinstance(std, np.ndarray):
        return None
    if X.ndim != 2 or mean.ndim != 1 or std.ndim != 1:
        return None
    if X.shape[1] != len(mean):
        return None
    std[std == 0] = 1
    return (X - mean) / std

def sigmoid(z):
    """
        Compute the sigmoid function.
    """
    z = np.clip(z, -500, 500) # limite les valeurs de z dans un intervalle (-500, 500) pour éviter overflow
    return 1 / (1 + np.exp(-z))


def fit_one_vs_all(X, y, num_labels, lr=0.1, iters=300):
    """
        Trains multiple logistic regression classifiers using one-vs-all strategy.
    """
    if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray) or not isinstance(num_labels, int) \
        or not isinstance(lr, float) or not isinstance(iters, int):
        return None
    if X.ndim != 2 or y.ndim != 1:
        return None
    if len(X) == 0 or len(y) == 0 or len(X) != len(y):
        return None
    if num_labels < 2:
        return None
    m, n = X.shape
    all_weights = []

    # biais
    X = np.c_[np.ones(m), X]  # ajouter une colonne de biais (1) à X
    n += 1

    for label in range(num_labels):
        theta = np.zeros(n)
        y_binary = (y == label).astype(int)

        for _ in range(iters):
            z = X @ theta
            h = sigmoid(z)

            gradient = (1 / m) * (X.T @ (h - y_binary))
            theta -= lr * gradient

        all_weights.append(theta)

    return np.array(all_weights)


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
    data = utils.lire_csv(file)

    if not data or len(data) < 2:
        print("Data file can be empty or invalid.")
        return 1

    # ------------------ Split data ------------------
    X, y = parse_dataset(data)
    y_encoded, mapping = encode_labels(y)
    x_train, x_test, y_train, y_test = data_spliter(X, y_encoded, 0.8)

    # ------------------ Polynomial features ------------------
    x_train_poly = add_polynomial_features(x_train, 2)
    x_test_poly = add_polynomial_features(x_test, 2)

    # ------------------ Feature normalization ------------------
    x_train_norm, mean, std = normalize_features(x_train_poly)
    x_test_norm = apply_normalization(x_test_poly, mean, std)

    # ------------------ One-vs-all training ------------------
    num_labels = len(set(y_train))
    weights = fit_one_vs_all(
        x_train_norm, y_train,
        num_labels,
        lr=0.1,
        iters=300
    )

    # ------------------ Save weights to CSV ------------------
    utils.ecrire_csv("weights.csv", weights.tolist())

    return 0

if __name__ == "__main__":
    main()