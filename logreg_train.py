import utils, sys

def main():
    """
        Main function to train logistic regression model.
        The program create weights.csv file.
        It contains the weights that will be used for the prediction.
    """

    if len(sys.argv) < 2:
        print("Usage: python logreg_train.py datasets/dataset_train.csv")
        return 1
    file = sys.argv[1]
    all_students = utils.lire_csv(file)

    if not all_students or len(all_students) < 2:
        print("Data file can be empty or invalid.")
        return 1
    

    return 0

if __name__ == "__main__":
    main()