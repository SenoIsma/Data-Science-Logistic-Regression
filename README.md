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
  <li class="my-0"><a href="#overview">Overview</a></li>
  <ul class="list-disc pl-4 my-0">
    <li class="my-0"><a href="#introduction-to-python">Introduction to Python</a></li>
  </ul>
  <li class="my-0"><a href="#building-the-42-dslr-project">Building the 42 DSLR project</a>
  <ul class="list-disc pl-4 my-0">
    <li class="my-0"><a href="#data-nalysis">Data Analysis</a></li>
    <li class="my-0"><a href="#histogram-analysis">Histogram Analysis</a></li>
    <li class="my-0"><a href="#scatter-plot-analysis">Scatter Plot Analysis</a></li>
    <li class="my-0"><a href="#pair-plot-analysis">Pair Plot Analysis</a></li>
    <li class="my-0"><a href="#logistic-regression">Logistic Regression</a></li>
  </ul>
  </li>
</ul>

<h2>Overview</h2>
<h3>Introduction to Python</h3>

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


#### Algorithm Steps
1. For each subject:
   - Calculate average score per house
   - Apply normalization if negative values exist
   - Compute standard deviation of the four house averages
   - Calculate CV of house averages
2. Identify subject with lowest CV

#### Results

| Subject | CV (%) |
|---------|--------|
| **Arithmancy** | **0.57** |
| Care of Magical Creatures | 1.29 |
| Transfiguration | 4.20 |
| Ancient Runes | 19.67 |
| Potions | 20.53 |


<h3>Scatter Plot Analysis</h3>

<h3>Pair Plot Analysis</h3>


<h3>Logistic Regression</h3>
