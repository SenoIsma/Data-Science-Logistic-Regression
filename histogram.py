def calculate_average(score_list):
    for i in range(len(score_list)):
        if score_list[i] :
            average = average + score_list[i]
    return average / len(score_list) if len(score_list) > 0 else 0


with open('./datasets/dataset_train.csv', 'r') as file:
    content = file.read()

lines = content.split('\n')
header = lines[0].split(',')

gryffindor_students = []
slytherin_students = []
hufflepuff_students = []
ravenclaw_students = []
arithmancy_gryffindor_students = []
arithmancy_slytherin_students = []
arithmancy_hufflepuff_students = []
arithmancy_ravenclaw_students = []

for i in range(1, len(lines)):
    if lines[i]:
        student_data = lines[i].split(',')
        house = student_data[1]
        arithmancy = student_data[6]

        if house == "Gryffindor":
            gryffindor_students.append(student_data)
            if arithmancy:
                arithmancy_gryffindor_students.append(float(arithmancy))
        elif house == "Slytherin":
            slytherin_students.append(student_data)
            if arithmancy:
                arithmancy_slytherin_students.append(float(arithmancy))
        elif house == "Hufflepuff":
            hufflepuff_students.append(student_data)
            if arithmancy:
                arithmancy_hufflepuff_students.append(float(arithmancy))
        elif house == "Ravenclaw":
            ravenclaw_students.append(student_data)
            if arithmancy:
                arithmancy_ravenclaw_students.append(float(arithmancy))

# TEST POUR VERIFIER LE NOMBRE D'ETUDIANT
#
# print(f"Gryffindor: {len(gryffindor_students)} étudiants")
# print(f"Slytherin: {len(slytherin_students)} étudiants")
# print(f"Hufflepuff: {len(hufflepuff_students)} étudiants")
# print(f"Ravenclaw: {len(ravenclaw_students)} étudiants")

# print(f"Gryffindor: {arithmancy_gryffindor_students[:5]}")
# print(f"Slytherin: {arithmancy_slytherin_students[:5]}")
# print(f"Hufflepuff: {arithmancy_hufflepuff_students[:5]}")
# print(f"Ravenclaw: {arithmancy_ravenclaw_students[:5]}")

# total = len(gryffindor_students) + len(slytherin_students) + len(hufflepuff_students) + len(ravenclaw_students)
# print("Etudiants totaux : ", total)

gryffindor_moyenne = calculate_average(arithmancy_gryffindor_students)

