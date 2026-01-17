import sys
import json
import utils
import numpy as np
from itertools import combinations_with_replacement


def parse_dataset(data):
    """Parse dataset and return feature matrix X and label vector y."""
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
    """Encode string labels into integers."""
    houses = sorted(list(set(y))) # set -> créé un ensemble unique et list -> convertit en liste
    mapping = {house: i for i, house in enumerate(houses)} # dictionnaire de mappage
    inverse_mapping = {i: house for house, i in mapping.items()}
    y_encoded = np.array([mapping[label] for label in y])
    return y_encoded, mapping, inverse_mapping


class LogisticRegression:
    """Logistic Regression classifier with One-vs-All strategy."""

    def __init__(self, lr=0.01, iters=1000):
        self.lr = lr
        self.iters = iters
        self.thetas = None
        self.mean = None
        self.std = None
        self.polynomial_degree = None
        self.label_mapping = None
        self.inverse_mapping = None

    @staticmethod
    def data_spliter(X, y, proportion):
        """Split the dataset into a training and a test set given a proportion."""
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
    
    @staticmethod
    def add_polynomial_features(X, power):
        """Add polynomial features to matrix X for all columns and all combinations up to 'power'."""
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

    @staticmethod
    def normalize_features(X, mean=None, std=None):
        """Normalize features in X to avoid division by zero and ensure consistent scaling."""
        if not isinstance(X, np.ndarray):
            return None
        if X.ndim != 2 or X.shape[0] == 0:
            return None
        if mean is None:
            mean = np.mean(X, axis=0)
        if std is None:
            std = np.std(X, axis=0)

        std[std == 0] = 1  # éviter division par 0
        X_norm = (X - mean) / std

        return X_norm, mean, std
    
    @staticmethod
    def sigmoid(z):
        """Compute the sigmoid function which represents the probability of the positive class."""
        z = np.clip(z, -500, 500) # limite les valeurs de z dans un intervalle (-500, 500) pour éviter overflow
        return 1 / (1 + np.exp(-z))
    
    def fit_one_classifier(self, X, y_binary, iters=None):
        """Train one binary classifier."""
        if iters is None:
            iters = self.iters
    
        m, n = X.shape
        theta = np.zeros(n + 1)  # ajouter un poids pour le biais
        X_bias = np.c_[np.ones(m), X]  # ajouter une colonne de biais (1) à X

        for _ in range(iters):
            z = X_bias @ theta
            y_hat = self.sigmoid(z)
            gradient = (1 / m) * (X_bias.T @ (y_hat - y_binary))
            theta -= self.lr * gradient

        return theta

    def fit(self, X, y, num_labels, polynomial_degree=2, label_mapping=None, inverse_mapping=None):
        """Train all classifiers (One-vs-All)."""
        
        # ------------------ Polynomial features ------------------
        X_poly = self.add_polynomial_features(X, polynomial_degree)
        # ------------------ Feature normalization ------------------
        X_norm, mean, std = self.normalize_features(X_poly)
        
        self.mean = mean
        self.std = std
        self.polynomial_degree = polynomial_degree
        self.label_mapping = label_mapping
        self.inverse_mapping = inverse_mapping
        
        # ------------------ One-vs-all training ------------------
        weights = []
        for label in range(num_labels):
            y_binary = (y == label).astype(int)
            theta = self.fit_one_classifier(X_norm, y_binary)
            weights.append(theta)
        
        self.thetas = np.array(weights)
        return self.thetas
    
    def predict(self, X):
        """Predict labels for input data X."""
        if self.thetas is None:
            raise ValueError("Model not trained yet. Call fit() first.")
        
        # ------------------ Same preprocessing ------------------
        X_poly = self.add_polynomial_features(X, self.polynomial_degree)
        X_norm, _, _ = self.normalize_features(X_poly, self.mean, self.std)

        X_bias = np.c_[np.ones(X_norm.shape[0]), X_norm] # ajouter une colonne de biais (1) à X
        z = X_bias @ self.thetas.T
        probas = self.sigmoid(z)
        predictions = np.argmax(probas, axis=1)
        
        return predictions
    
    def accuracy(self, X, y):
        """Calculate accuracy of the model on data X with true labels y."""
        y_pred = self.predict(X)
        return np.mean(y_pred == y) * 100
    
    def save_model(self, filename="model.json"):
        """Save the trained model parameters to a JSON file."""
        if self.thetas is None:
            raise ValueError("Model not trained yet.")
        
        model_data = {
            'polynomial_degree': int(self.polynomial_degree),
            'learning_rate': float(self.lr),
            'iterations': int(self.iters),
            'label_mapping': self.label_mapping,
            'inverse_mapping': {int(k): v for k, v in self.inverse_mapping.items()},
            'weights': self.thetas.tolist(),
            'mean': self.mean.tolist(),
            'std': self.std.tolist(),
        }
        
        with open(filename, 'w') as f:
            json.dump(model_data, f, indent=2)
        
        print(f"Model saved to {filename}")


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

    # ------------------ Parse & split data ------------------
    X, y = parse_dataset(data)
    y_encoded, mapping, inverse_mapping = encode_labels(y)
    np.random.seed(42)  # Fixe le générateur aléatoire
    X_train, X_test, y_train, y_test = LogisticRegression.data_spliter(X, y_encoded, 0.8)

    # ------------------ Find optimal iterations ------------------
    num_labels = len(mapping)
    best_accuracy = 0
    best_iter = 0
    best_model = None
    iterations_to_test = [100, 200, 300, 400, 500, 750, 1000, 1500, 2000]

    print(f"{'Iterations':<12} {'Train Acc':<15} {'Test Acc':<15} {'Status'}")
    print("-"*70)

    for iters in iterations_to_test:
        # learning rate : 0.1 car normalisation des features
        model = LogisticRegression(lr=0.1, iters=iters)
        # puissance     : 2 CAR pour ~14 features (hors Index, Names, Birthday) :
            # 1 : 14 features / 2 : ~104 features / 3 : ~455 features (trop!)
            # ET 1 ne permet pas de capturer les interactions non linéaires
        model.fit(X_train, y_train, num_labels, polynomial_degree=2, 
                  label_mapping=mapping, inverse_mapping=inverse_mapping)
        
        train_acc = model.accuracy(X_train, y_train)
        test_acc = model.accuracy(X_test, y_test)
        
        if test_acc > best_accuracy:
            status = "✓ Improvement"
            best_accuracy = test_acc
            best_iter = iters
            best_model = model
        elif abs(test_acc - best_accuracy) < 0.1:
            status = "≈ Stable"
        else:
            status = "⚠ Degradation"
        
        print(f"{iters:<12} {train_acc:>6.2f}%{'':<8} {test_acc:>6.2f}%{'':<8} {status}")
    
    print("-"*70)
    print(f"\nOptimal result:")
    print(f"  → Number of iterations : {best_iter}")
    print(f"  → Test accuracy : {best_accuracy:.2f}%\n")

    
    # ------------------ Save weights to CSV ------------------
    best_model.save_model("model.json")
    utils.ecrire_csv("weights.csv", best_model.thetas.tolist())

    return 0

if __name__ == "__main__":
    main()