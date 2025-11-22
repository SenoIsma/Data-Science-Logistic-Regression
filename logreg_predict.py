import utils, sys

def main():
    """
        Main function to predict using logistic regression model.
        The program create houses.csv file.
        Output example of houses.csv :
        Index,Hogwarts House
        0,Gryffindor
        1,Hufflepuff
        2,Ravenclaw
        3,Hufflepuff
        4,Slytherin
        5,Ravenclaw
        6,Hufflepuff
        ...

        Evaluation : python evaluate.py
        will return something like
            Your score on test set: 0.88
        in order to evaluate the precision of our model.
        The minimum score requiere is up to 0.98
    """

    if len(sys.argv) < 3:
        print("Usage: python logreg_predict.py datasets/dataset_test.csv weights.csv")
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