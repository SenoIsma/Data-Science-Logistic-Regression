# ========================= describe =============================

def sum(tableau):
    """Calculate the sum of a column in a 2D array."""

    total = 0
    for row in tableau:
        try:
            total += float(row)
        except (ValueError, IndexError):
            continue
    return total

def count(tableau, col_index):
    """Count the number of valid entries in a column."""

    count = 0
    for row in tableau[1:]:  # Ignorer l'en-tête
        try:
            float(row[col_index])
            count += 1
        except (ValueError, IndexError):
            continue
    return count

def mean(tableau, col_index):
    """Calculate the mean of a column in a 2D array."""

    total = 0
    count = 0
    for row in tableau[1:]:  # Ignorer l'en-tête
        try:
            total += float(row[col_index])
            count += 1
        except (ValueError, IndexError):
            continue
    return total / count if count > 0 else 0

def std(tableau, col_index):
    """Calculate the standard deviation of a column in a 2D array."""

    m = mean(tableau, col_index)
    total = 0
    count = 0
    for row in tableau[1:]:  # Ignorer l'en-tête
        try:
            val = float(row[col_index])
            total += (val - m) ** 2
            count += 1
        except (ValueError, IndexError):
            continue
    variance = total / count if count > 0 else 0
    return variance ** 0.5

def min(tableau, col_index):
    """Calculate the minimum of a column in a 2D array."""

    minimum = float('inf')
    for row in tableau[1:]:  # Ignorer l'en-tête
        try:
            val = float(row[col_index])
            if val < minimum:
                minimum = val
        except (ValueError, IndexError):
            continue
    return minimum if minimum != float('inf') else None

def max(tableau, col_index):
    """Calculate the maximum of a column in a 2D array."""

    maximum = float('-inf')
    for row in tableau[1:]:  # Ignorer l'en-tête
        try:
            val = float(row[col_index])
            if val > maximum:
                maximum = val
        except (ValueError, IndexError):
            continue
    return maximum if maximum != float('-inf') else None

def percentile(tableau, col_index, percent):
    """Calculate the given percentile of a column in a 2D array."""

    values = []
    for row in tableau[1:]:  # Ignorer l'en-tête
        try:
            val = float(row[col_index])
            values.append(val)
        except (ValueError, IndexError):
            continue
    if not values:
        return None
    values.sort()
    if percent == 0:
        return values[0]
    if percent == 100:
        return values[-1]
    k = (len(values)-1) * (percent/100)
    f = int(k)
    c = k - f
    if f + 1 < len(values):
        return values[f] + c * (values[f + 1] - values[f])
    else:
        return values[f]

# ========================= histogram ============================

def calculate_average(score_list):
    """Calculate the average of a list of scores."""

    if len(score_list) == 0:
        return 0
    average = sum(score_list)
    result = average / len(score_list)
    return result

def search_min(gryffindor, slytherin, hufflepuff, ravenclaw):
    """Find the minimum grade among all houses."""

    all_notes = gryffindor + slytherin + hufflepuff + ravenclaw
    return min(all_notes) if all_notes else 0

def normalize_positive(notes_list, global_min):
    """Normalize grades to ensure all are positive."""

    # Décaler pour que le minimum soit à 1 (évite les moyennes nulles)
    return [note - global_min + 1 for note in notes_list]

def calculate_std(mean_list):
    """Calculate the standard deviation of a list of means."""

    if len(mean_list) == 0:
        return 0
    m = sum(mean_list) / len(mean_list)
    total = 0
    for mean in mean_list:
        total += (mean - m) ** 2
    std = total / len(mean_list)
    return std ** 0.5

# ========================= scatter plot =========================

def calculate_correlation_coefficient(x, y):
    """Calculate the Pearson correlation coefficient between two lists."""

    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x2 = sum(i**2 for i in x)
    sum_y2 = sum(i**2 for i in y)
    sum_xy = sum(x[i] * y[i] for i in range(n))

    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))**0.5

    if denominator == 0:
        return 0
    return numerator / denominator
