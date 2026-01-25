<div align="center" class="text-center">
  <h1>42-DSLR</h1>
  
  <img alt="last-commit" src="https://img.shields.io/github/last-commit/SenoIsma/Data-Science-Logistic-Regression?style=flat&amp;logo=git&amp;logoColor=white&amp;color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
  <img alt="repo-top-language" src="https://img.shields.io/github/languages/top/SenoIsma/Data-Science-Logistic-Regression?style=flat&amp;color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
  <img alt="repo-language-count" src="https://img.shields.io/github/languages/count/SenoIsma/Data-Science-Logistic-Regression?style=flat&amp;color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
  <p><em>Built with the tools and technologies:</em></p>
  <img alt="Markdown" src="https://img.shields.io/badge/Markdown-000000.svg?style=flat&amp;logo=Markdown&amp;logoColor=white" class="inline-block mx-1" style="margin: 0px 2px;">
  <img alt="GNU%20Bash" src="https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=flat&amp;logo=GNU-Bash&amp;logoColor=white" class="inline-block mx-1" style="margin: 0px 2px;">
  <img alt="Python" src="https://img.shields.io/badge/python-2496ED.svg?style=flat&amp;logo=python&amp;logoColor=white" class="inline-block mx-1" style="margin: 0px 2px;">
</div>

<h2>Table of Contents</h2>
<ul class="list-disc pl-4 my-0">
  <li class="my-0"><a href="#building-the-42-dslr-project">Building the 42 DSLR project</a>
  <ul class="list-disc pl-4 my-0">
    <li class="my-0"><a href="#data-analysis">Data Analysis</a></li>
    <li class="my-0"><a href="#histogram-analysis">Histogram Analysis</a></li>
    <li class="my-0"><a href="#scatter-plot-analysis">Scatter Plot Analysis</a></li>
    <li class="my-0"><a href="#pair-plot-analysis">Pair Plot Analysis</a></li>
    <li class="my-0"><a href="#logistic-regression">Logistic Regression</a></li>
  </ul>
  </li>
</ul>

<h2>Building the 42 DSLR project</h2>

<h3>Data Analysis</h3>

#### Objective
Create a descriptive statistics program that analyzes the Hogwarts dataset without using built-in statistical functions like `describe()`, `mean()`, `std()`, etc.

#### Data Processing
1. **CSV Parsing**: Manual reading and parsing of the training dataset
2. **Data Type Handling**: Automatic detection and conversion of numerical features
3. **Missing Value Management**: Identification and exclusion of empty/invalid entries

#### Output Format
```
                    Feature 1    Feature 2    Feature 3    Feature 4
Count               149.000000   149.000000   149.000000   149.000000
Mean                5.848322     3.051007     3.774497     1.205369
Std                 5.906338     3.081445     4.162021     1.424286     #Standard deviation
Min                 4.300000     2.000000     1.000000     0.100000
25%                 5.100000     2.800000     1.600000     0.300000
50%                 5.800000     3.000000     4.400000     1.300000
75%                 6.400000     3.300000     5.100000     1.800000
Max                 7.900000     4.400000     6.900000     2.500000
```

#### Usage
```bash
python describe.py dataset_train.csv
```

<h3>Histogram Analysis</h3>

#### Objective
Identify which Hogwarts course has the most homogeneous score distribution between all four houses (Gryffindor, Slytherin, Hufflepuff, Ravenclaw).

#### Data Processing
1. **CSV Parsing**: Read the training dataset and extract student data by house
2. **Data Cleaning**: Handle missing values and convert string scores to floats
3. **House Segregation**: Separate students by their Hogwarts house for each subject

#### Homogeneity Measurement

We used the **Coefficient of Variation (CV)** to measure homogeneity between houses:

```
CV = (standard_deviation / mean) × 100
```

The CV measures relative dispersion - the lower the CV, the more homogeneous the distribution.

**Data Normalization:**

To ensure fair comparison and avoid issues with negative or very small values, all grades are normalized using the global minimum across all subjects. Each score is shifted so that the minimum value becomes 1:

```
normalized_score = original_score - global_min + 1
```

This normalization is applied before calculating house averages and the CV.

#### Algorithm Steps
1. For each subject:
   - Apply global minimum normalization to all scores
   - Calculate average score per house
   - Compute standard deviation of the four house averages
   - Calculate CV of house averages
2. Identify subject with lowest CV

#### Results

After applying global minimum normalization, the results show:

| Subject                       | CV (%)   |
|-------------------------------|----------|
| Arithmancy                    | 0.57     |
| Astronomy                     | 2.02     |
| Herbology                     | 0.02     |
| Defense Against the Dark Arts | 0.02     |
| Divination                    | 0.02     |
| Muggle Studies                | 1.76     |
| Ancient Runes                 | 0.39     |
| History of Magic              | 0.02     |
| Transfiguration               | 0.17     |
| Potions                       | 0.01     |
| **Care of Magical Creatures** | **0.00** |
| Charms                        | 0.03     |
| Flying                        | 0.40     |

**🏆 Most Homogeneous Course: Care of Magical Creatures (CV: 0.00%)**


<h3>Scatter Plot Analysis</h3>

#### Pearson's correlation coefficient

```
        Σ[(xi - x̄)(yi - ȳ)]
r = ─────────────────────────────
    √[Σ(xi - x̄)²] × √[Σ(yi - ȳ)²]
```

1. Averages of each of the two subjects (x and y)
2. Numerator
3. Variances of each of the two subjects
4. Numerator / Multiplication of the two variances

#### Algorithm Steps

1. Loop through each course except the last one
2. For each course, loop through all subsequent courses until the last one
3. Keep the names of the two courses and the correlation coefficient result
4. Display the students' marks for the two subjects with the highest correlation coefficient in absolute value in a scatter plot

#### Correlation coefficient analysis

For two features, the coefficient is always between [-1; 1], meaning that if :
- coef is close to 0 => no correlation between the two features
- coef is close to 1 => strong correlation, the two features evolve in the same way
- coef is close to -1 => strong correlation but when the first feature evolves, the second one goes the opposite way

#### Results

Highest correlation is between Astronomy and Defense Against the Dark Arts: -1.0000.
It means that there is a strong correlation between the two courses but a decreasing one. In other words, the higher a student's grade in Astronomy, the lower their grade in Dark Arts and vice versa.

<h3>Pair Plot Analysis</h3>

#### Objective
Create a comprehensive pair plot visualization that displays the relationships between all Hogwarts courses, showing both distribution patterns and correlations between subjects for each house.

#### Data Processing
1. **CSV Parsing**: Read the training dataset and extract student data
2. **House Segregation**: Separate students by their Hogwarts house (Gryffindor, Slytherin, Hufflepuff, Ravenclaw)
3. **Feature Extraction**: Extract all 13 course grades for visualization

#### Visualization Structure

The pair plot is a 13x13 matrix where each cell represents the relationship between two courses:

- **Diagonal Elements**: Histograms showing the distribution of grades for each individual course, separated by house
- **Off-Diagonal Elements**: Scatter plots showing the correlation between pairs of courses, with points colored by house

#### Matrix Interpretation

**Diagonal Histograms**: Show the grade distribution for each course. Overlapping histograms by house reveal:
- Which houses perform better in specific subjects
- The spread and skewness of grades within each house
- Outliers and grade clustering patterns

**Scatter Plots**: Reveal correlations between course pairs:
- **Positive correlation**: Points form an upward trend (students good at one subject tend to be good at the other)
- **Negative correlation**: Points form a downward trend (inverse relationship between subjects)
- **No correlation**: Points appear randomly scattered
- **House-specific patterns**: Different colored clusters can reveal house-specific correlations

#### Results

The pair plot provides a comprehensive overview of the Hogwarts academic landscape, enabling identification of:
- Courses with similar difficulty levels across houses
- Subject combinations that students excel at together
- House-specific academic strengths and weaknesses
- Overall correlation structure in the curriculum

This visualization complements the individual analyses by providing a holistic view of all course relationships simultaneously.

<h3>Logistic Regression</h3>

#### Definition

**Model type**    : `ŷ = σ(θ_0 + θ_1 x_1 + … + θ_n x_n)`
**Output nature** : `Probability ∈ [0, 1]`

Logistic regression is a classification algorithm that predicts the probability of an instance belonging to a particular class. Unlike linear regression, it uses the sigmoid function to constrain outputs between 0 and 1.

#### Sigmoid Function

The sigmoid (or logistic) function transforms any real-valued number into a probability:
```
         1
σ(z) = ─────────
       1 + e^(-z)
```

Where `z = θ^T x` (the linear combination of features and weights)

**Properties:**
- `σ(z) → 1` when `z → +∞`
- `σ(z) → 0` when `z → -∞`
- `σ(0) = 0.5`

#### Cost Function

For binary classification, we use the **log loss** (cross-entropy):
```
          1   m
J(θ) = - ───  Σ [y_i log(h_θ(x_i)) + (1 - y_i) log(1 - h_θ(x_i))]
          m  i=1
```

Where:
- `h_θ(x) = σ(θ^T x)` is the hypothesis (predicted probability)
- `y_i ∈ {0, 1}` is the true label
- `m` is the number of training examples

This cost function is **convex**, ensuring gradient descent converges to the global minimum.

#### Gradient Descent

To minimize the cost function, we update weights iteratively:
```
               ∂J(θ)            1   m
θ_j := θ_j - α ───── = θ_j - α ───  Σ (h_θ(x_i) - y_i) x_i^j
               ∂θ_j             m  i=1
```

Where:
- `α` is the learning rate (step size)
- The gradient tells us the direction to adjust weights
- We repeat until convergence

#### One-vs-All (OvA) Strategy

Since logistic regression is inherently **binary** (2 classes), but we need to classify into **4 houses**, we use the **One-vs-All** (also called One-vs-Rest) multi-class strategy.

**Principle:**
1. **Train K binary classifiers** (one for each of the K classes)
   - Classifier 1: Gryffindor vs. {Hufflepuff, Ravenclaw, Slytherin}
   - Classifier 2: Hufflepuff vs. {Gryffindor, Ravenclaw, Slytherin}
   - Classifier 3: Ravenclaw vs. {Gryffindor, Hufflepuff, Slytherin}
   - Classifier 4: Slytherin vs. {Gryffindor, Hufflepuff, Ravenclaw}

2. **Each classifier learns to answer**: "Is this student in MY house?"
   - Output: Probability that the student belongs to that specific house

3. **Prediction**: For a new student, run all K classifiers and:
```
   predicted_house = argmax(P(house_i | student))
                            i∈{1,2,3,4}
```
   Choose the house with the **highest probability**

**Mathematical Formulation:**

For each class `k`:
- Transform labels: `y_binary = 1` if `y = k`, else `0`
- Train classifier to minimize: `J_k(θ_k)`
- Store weights: `θ_k`

At prediction time:
```
class = argmax σ(θ_k^T x)
         k
```

#### Feature Engineering

To capture non-linear relationships between courses, we apply **polynomial feature expansion**:

**Original features** (13 courses):
```
x = [Arithmancy, Astronomy, Herbology, ..., Flying]
```

**Polynomial features (degree 2)**:
```
- Linear terms: x_1, x_2, ..., x_13
- Quadratic terms: x_1², x_2², ..., x_13²
- Interaction terms: x_1·x_2, x_1·x_3, ..., x_12·x_13
```

**Result**: ~104 features that capture:
- Individual course performance (linear terms)
- Course difficulty patterns (quadratic terms)
- Cross-course correlations (interaction terms)

Example: `Potions × Herbology` might reveal students good at both (Hufflepuff pattern)

#### Feature Normalization

To ensure stable gradient descent, we **normalize** all features:
```
         x - mean(x)
x_norm = ────────────
          std(x)
```

**Benefits:**
- All features on same scale (mean=0, std=1)
- Faster convergence
- Prevents features with large ranges from dominating
- Allows higher learning rate (α = 0.1)

#### Hyperparameters

**Learning Rate (α = 0.1)**
- Fixed theoretically based on normalized features
- With normalization, gradient is already scaled
- Higher LR → faster convergence
- Standard value for normalized data

**Polynomial Degree (2)**
- Degree 1: Too simple, linear boundaries only
- Degree 2: Captures non-linear interactions (~104 features)
- Degree 3: Too complex, ~455 features, overfitting risk
- **Optimal**: Degree 2 balances expressiveness and complexity

**Iterations (300)**
- Only hyperparameter tuned empirically
- Tested: 100, 200, 300, 400, 500, 750, 1000, 1500, 2000
- Convergence observed around 250-300 iterations
- Beyond 300: accuracy stagnates or decreases (overfitting)

#### Training Process

1. **Load and parse** training data (dataset_train.csv)
2. **Split** into train/test sets (80/20)
3. **Apply polynomial features** (degree 2)
4. **Normalize** features (mean=0, std=1)
5. **Train 4 OvA classifiers** using gradient descent
6. **Evaluate** on test set to find optimal iterations
7. **Save model** (weights, normalization params, label mapping)

#### Prediction Process

1. **Load model** (model.json)
2. **Parse test data** (dataset_test.csv)
3. **Apply same transformations**:
   - Polynomial features (degree 2)
   - Normalization (using training mean/std)
4. **Run all 4 classifiers**
5. **Select house** with highest probability
6. **Save predictions** (houses.csv)

#### Performance

**Target**: 98% accuracy (Sorting Hat standard)
**Achieved**: ~98.5% on test set

The model successfully replicates the Sorting Hat's decisions with high accuracy, demonstrating that:
- Course performance patterns encode house characteristics
- Polynomial features capture complex student profiles
- One-vs-All strategy effectively handles multi-class sorting

#### Usage
```bash
# Train the model
python logreg_train.py datasets/dataset_train.csv

# Make predictions
python logreg_predict.py datasets/dataset_test.csv

# Evaluate accuracy
python evaluate.py
```

#### Files Generated

- `model.json`: Complete model (weights, normalization params, mappings)
- `weights.csv`: Weight matrices only (compatibility)
- `houses.csv`: Predictions for test set

#### Implementation Notes

**Constraints respected:**
- ✅ No sklearn or similar ML libraries
- ✅ Gradient descent implemented from scratch
- ✅ One-vs-All strategy manually coded
- ✅ NumPy used only for matrix operations (not ML functions)

**Key features:**
- Robust error handling
- Reproducible results (fixed random seed)
- Complete model serialization
- Modular, object-oriented design
