import utils, sys

def main():
    """Main function to predict using logistic regression model."""

    if len(sys.argv) < 3:
        print("Usage: python logreg_predict.py datasets/dataset_test.csv weights_trained.csv")
        return 1
    data_file = sys.argv[1]
    model_file = sys.argv[2]
    all_students = utils.lire_csv(data_file)

    if not all_students or len(all_students) < 2:
        print("Data file can be empty or invalid.")
        return 1

    return 0

if __name__ == "__main__":
    main()