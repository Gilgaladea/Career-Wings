""" ZADANIE 1 """
exam_points = {"Mariusz": 30, "Mateusz": 55, "Marta": 76, "Roman": 30,
               "Arleta": 59, "Adrian": 96, "Monika": 91, "Andrzej": 22,
               "Krzysztof": 83, "Krystyna": 93, "Piotr": 44, "Dawid": 10, "Agnieszka": 15}

failed_students = [student for student, wynik in exam_points.items() if wynik <= 45]
print(failed_students)

top_students = [student for student, wynik in exam_points.items() if wynik >= 91]
print(top_students)

max_score = max(exam_points.values())
best_student = [student for student, wynik in exam_points.items() if wynik == max_score]
print(best_student)


""" ZADANIE 2 """
names = ['Paweł', 'Kewin', 'Ireneusz', 'Bolesław', 'Mateusz',
         'Edward', 'Piotr', 'Jan', 'Denis', 'Amir', 'Igor', 'Borys',
         'Robert', 'Ariel', 'Kuba', 'Rafał', 'Mateusz', 'Emanuel']
name_dict = {}
for name in names:
    if name[0] not in name_dict.keys():
        name_dict[name[0]] = {name}
    else:
        name_dict[name[0]].add(name)
print(name_dict)


""" ZADANIE 3 """
num = 30
fibonacci = []
while len(fibonacci) < num:
    if len(fibonacci) < 2:
        fibonacci.append(1)
    else:
        fibonacci.append(sum(fibonacci[-2:]))
print(fibonacci)


""" ZADANIE 4 """
def equation(a, b, c):
    delta = b * b - 4 * a * c
    if delta > 0:
        return (-b + delta ** (1 / 2)) / (2 * a), (-b - delta ** (1 / 2)) / (2 * a)
    elif delta == 0:
        return -b / (2 * a)
    else:
        return "Brak rozwiązań"


print(equation(1, 4, 3))
print(equation(2, 12, 18))
print(equation(1, 2, 3))