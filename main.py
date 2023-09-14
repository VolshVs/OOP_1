from statistics import mean

class Student:
    students = []
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        Student.students.append(self)

    def average_rating(self):
        for grade in self.grades:
            grade_ = sum(self.grades[grade]) / len(self.grades[grade])
        return round(grade_, 1)


    def grades_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course \
                in self.courses_in_progress and course \
                in lecturer.courses_attached and 0 < grade <= 10:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка выполнения задачи.'

    def __str__(self):
        some_student = (f'Имя: {self.name}\n'
                        f'Фамилия: {self.surname}\n'
                        f'Средняя оценка за домашние задания: '
                        f'{self.average_rating()}\n'
                        f'Курсы в процессе изучения: '
                        f'{", ".join(self.courses_in_progress)}\n'
                        f'Завершенные курсы: '
                        f'{", ".join(self.finished_courses)}')
        return some_student

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Человек ошибся аудиторией, он не является'
                  ' студентом данного потока!')
            return
        return self.average_rating() > other.average_rating()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    lecturers = []
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.courses_attached = []
        Lecturer.lecturers.append(self)

    def average_rating(self):
        for grade in self.grades:
            grade_ = sum(self.grades[grade]) / len(self.grades[grade])
        return round(grade_, 1)

    def __str__(self):
        some_lecturer = (f'Имя: {self.name}\n'
                         f'Фамилия: {self.surname}\n'
                         f'Средняя оценка за лекции: {self.average_rating()}')
        return some_lecturer

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('Данный товарищ не является лектором!')
            return
        return self.average_rating() > other.average_rating()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []


    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached \
                and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка выполнения задачи.'

    def __str__(self):
        some_reviewer = (f'Имя: {self.name}\n'
                         f'Фамилия: {self.surname}')
        return some_reviewer


def comparison_of_students(students_list: list, course: str):
    count = 0
    summ = 0
    for student_ in students_list:
        if isinstance(student_, Student):
            if course in student_.grades:
                summ += mean(student_.grades[course])
                count += 1
    return f'{round((summ / count), 1)}'


def comparison_of_lecturers(lecturers_list: list, course: str):
    count = 0
    summ = 0
    for lecturer_ in lecturers_list:
        if isinstance(lecturer_, Lecturer):
            if course in lecturer_.grades:
                summ += mean(lecturer_.grades[course])
                count += 1
    return f'{round((summ / count), 1)}'



# Тестирование:

# Студенты:
student_1 = Student('Иван', 'Иванов', 'мужчина')
student_1.courses_in_progress += ['Python', 'JavaScript']
student_1.finished_courses += ['Git']
student_2 = Student('Вера', 'Надеждовна', 'женщина')
student_2.courses_in_progress += ['Python']
student_2.finished_courses += ['JavaScript', 'Git']

# Лекторы:
lecturer_1 = Lecturer('Елена', 'Малышева')
lecturer_1.courses_attached += ['Python', 'Git']
lecturer_2 = Lecturer('Геннадий', 'Малахов')
lecturer_2.courses_attached += ['Python', 'JavaScript', 'Git']

# Проверяющие:
reviewer_1 = Reviewer('Олег', 'Булыгин')
reviewer_1.courses_attached += ['Python']
reviewer_2 = Reviewer('Елена', 'Никитина')
reviewer_2.courses_attached += ['Python']


# Выставляем оценки:

# Лекторам:
student_1.grades_lecturer(lecturer_1, 'Python', 10)
student_1.grades_lecturer(lecturer_1, 'Python', 9)
student_1.grades_lecturer(lecturer_2, 'Python', 9)
student_1.grades_lecturer(lecturer_2, 'Python', 7)

student_2.grades_lecturer(lecturer_1, 'Python', 6)
student_2.grades_lecturer(lecturer_1, 'Python', 7)
student_2.grades_lecturer(lecturer_2, 'Python', 8)
student_2.grades_lecturer(lecturer_2, 'Python', 9)

# Студентам:
reviewer_1.rate_hw(student_1, 'Python', 9)
reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_2, 'Python', 8)
reviewer_1.rate_hw(student_2, 'Python', 7)

reviewer_2.rate_hw(student_1, 'Python', 2)
reviewer_2.rate_hw(student_1, 'Python', 10)
reviewer_2.rate_hw(student_2, 'Python', 1)
reviewer_2.rate_hw(student_2, 'Python', 9)

print()
print(student_1.__str__())
print()
print(student_2.__str__())
print()
print('*'*79)
print()
print(lecturer_1.__str__())
print()
print(lecturer_2.__str__())
print()
print('%'*79)
print()
print(reviewer_1.__str__())
print()
print(reviewer_2.__str__())
print()
print('$'*79)
print()
print("Сравнение студентов по средней оценке:")
print(student_1.__lt__(student_2))
print(student_2 > student_1)
print(student_1 == student_2)
student_1.__lt__(lecturer_1)
print()
print('Сравнение лекторов по средней оценке за лекции:')
print(lecturer_1.__lt__(lecturer_2))
print(lecturer_2 == student_1)
print(lecturer_2 > lecturer_1)
lecturer_1.__lt__(student_2)

print()
print('*')
comparison_of_students = comparison_of_students(Student.students, 'Python')
comparison_of_lecturers = comparison_of_lecturers(Lecturer.lecturers, \
                                                  "Python")
print(f'Подсчет средней оценки за домашние задания всех студентов '
      f'в рамках курса Python: {comparison_of_students}')
print(f'Подсчет средней оценки за лекции всех лекторов '
      f'в рамках курса Python: {comparison_of_lecturers}')
print('*')


