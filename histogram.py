import matplotlib.pyplot as plt

def calculate_average(score_list):
    if len(score_list) == 0:
        return 0
    average = sum(score_list)
    result = average / len(score_list)
    return result

def search_min(gryffindor, slytherin, hufflepuff, ravenclaw):
    all_notes = gryffindor + slytherin + hufflepuff + ravenclaw
    return min(all_notes) if all_notes else 0

def normalize_positive(notes_list, global_min):
    # Décaler pour que le minimum soit à 1 (évite les moyennes nulles)
    return [note - global_min + 1 for note in notes_list]

def calculate_std(mean_list):
    if len(mean_list) == 0:
        return 0
    m = sum(mean_list) / len(mean_list)
    total = 0
    for mean in mean_list:
        total += (mean - m) ** 2
    std = total / len(mean_list)
    return std ** 0.5

with open('./datasets/dataset_train.csv', 'r') as file:
    content = file.read()

lines = content.split('\n')
header = lines[0].split(',')

all_cv = []
all_students = []
for i in range(1, len(lines)):
    if lines[i]:
        student_data = lines[i].split(',')
        all_students.append(student_data)

# Calculer le minimum global sur toutes les matières
global_min = float('inf')
for subject_index in range(6, len(header)):
    if header[subject_index]:
        for student in all_students:
            note = student[subject_index]
            if note:
                try:
                    global_min = min(global_min, float(note))
                except ValueError:
                    pass

for subject_index in range(6, len(header)):
    if header[subject_index]:
        subject_name = header[subject_index]

        gryffindor_notes = []
        slytherin_notes = []
        hufflepuff_notes = []
        ravenclaw_notes = []
        for student in all_students:
            house = student[1]
            note = student[subject_index]
            if note:
                try:
                    if house == "Gryffindor":
                        gryffindor_notes.append(float(note))
                    elif house == "Slytherin":
                        slytherin_notes.append(float(note))
                    elif house == "Hufflepuff":
                        hufflepuff_notes.append(float(note))
                    elif house == "Ravenclaw":
                        ravenclaw_notes.append(float(note))

                except ValueError:
                    pass

        # Normalisation avec le minimum global
        gryffindor_notes = normalize_positive(gryffindor_notes, global_min)
        slytherin_notes = normalize_positive(slytherin_notes, global_min)
        hufflepuff_notes = normalize_positive(hufflepuff_notes, global_min)
        ravenclaw_notes = normalize_positive(ravenclaw_notes, global_min)

        averages = [
            calculate_average(gryffindor_notes),
            calculate_average(slytherin_notes), 
            calculate_average(hufflepuff_notes),
            calculate_average(ravenclaw_notes)
        ]

        std = calculate_std(averages)
        if calculate_average(averages) == 0 :
            print("division par 0")
        # Coefficient de Variation
        cv = (std / calculate_average(averages)) * 100
        print(cv)
        all_cv.append(cv)

min_cv = min(all_cv)
min_index = all_cv.index(min_cv)

# Retrouver le nom de la matière
subject_names = []
for subject_index in range(6, len(header)):
    if header[subject_index]:
        subject_names.append(header[subject_index])

most_homogeneous = subject_names[min_index]

print(f"🏆 MOST HOMOGENEOUS COURSE: {most_homogeneous}")
print(f"📊 COEFFICIENT OF VARIATION: {min_cv:.2f}%")
                
gryffindor_origin = []
slytherin_origin = []
hufflepuff_origin = []
ravenclaw_origin = []
for student in all_students:
    house = student[1]
    note = student[min_index + 6]
    if note:
        try:
            if house == "Gryffindor":
                gryffindor_origin.append(float(note))
            elif house == "Slytherin":
                slytherin_origin.append(float(note))
            elif house == "Hufflepuff":
                hufflepuff_origin.append(float(note))
            elif house == "Ravenclaw":
                ravenclaw_origin.append(float(note))

        except ValueError:
            pass

plt.hist(ravenclaw_origin, bins=20, alpha=0.7, label="Ravenclaw")
plt.hist(hufflepuff_origin, bins=20, alpha=0.7, label="Hufflepuff") 
plt.hist(gryffindor_origin, bins=20, alpha=0.7, label="Gryffindor")
plt.hist(slytherin_origin, bins=20, alpha=0.7, label="Slytherin")
plt.title(f"Distribution of grades - {most_homogeneous}")
plt.xlabel("GRADES")
plt.ylabel("NUMBER OF STUDENTS")
plt.legend()
plt.show()
