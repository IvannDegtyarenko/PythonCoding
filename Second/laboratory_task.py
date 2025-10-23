import json
from pathlib import Path

class Teacher:
    def __init__(self, id, subject_ids):
        self.id = id
        self.subject_ids = set(subject_ids)

    def can_teach(self, subject_id):
        return subject_id in self.subject_ids


class StudentGroup:
    def __init__(self, id, subject_ids):
        self.id = id
        self.subject_ids = set(subject_ids)

    def needs_subject(self, subject_id):
        return subject_id in self.subject_ids


class Classroom:
    def __init__(self, id):
        self.id = id


class Lesson:
    def __init__(self, teacher, subject_id, group, classroom, time_slot):
        self.teacher = teacher
        self.subject_id = subject_id
        self.group = group
        self.classroom = classroom
        self.time_slot = time_slot


class Timetable:
    def __init__(self, input_file):
        self.input_file = input_file
        self.timetable = []
        self.load_data()
        self.create_objects()

    def load_data(self):
        with open(self.input_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        print("Данные загружены из файла")

    def create_objects(self):
        self.teachers = {}
        for teacher_id, subject_ids in self.data["Teachers"].items():
            self.teachers[int(teacher_id)] = Teacher(int(teacher_id), subject_ids)

        self.groups = {}
        for group_id, subject_ids in self.data["Groups"].items():
            self.groups[int(group_id)] = StudentGroup(int(group_id), subject_ids)

        self.classrooms = []
        for i in range(1, self.data["Classrooms"] + 1):
            self.classrooms.append(Classroom(i))

        self.classes_count = self.data["Classes"]
        self.subjects_count = self.data["Subjects"]

        print(
            f"Создано: {len(self.teachers)} преподавателей, {len(self.groups)} групп, {len(self.classrooms)} аудиторий"
        )

    def is_slot_free(self, teacher, group, classroom, time_slot):
        for lesson in self.timetable:
            if lesson.classroom.id == classroom.id and lesson.time_slot == time_slot:
                return False
            if lesson.teacher.id == teacher.id and lesson.time_slot == time_slot:
                return False
            if lesson.group.id == group.id and lesson.time_slot == time_slot:
                return False
        return True

    def build_timetable(self):
        all_lessons = []
        for subject_id in range(1, self.subjects_count + 1):
            for group in self.groups.values():
                if group.needs_subject(subject_id):
                    for teacher in self.teachers.values():
                        if teacher.can_teach(subject_id):
                            all_lessons.append((teacher, subject_id, group))

        print(f"Всего требуется занятий: {len(all_lessons)}")

        # Сортируем занятия по сложности размещения (приоритет редким комбинациям)
        def get_lesson_priority(lesson):
            teacher, subject_id, group = lesson
            # Считаем, сколько преподавателей могут вести этот предмет
            teacher_options = len([t for t in self.teachers.values() if t.can_teach(subject_id)])
            # Считаем, сколько групп нуждаются в этом предмете
            group_options = len([g for g in self.groups.values() if g.needs_subject(subject_id)])
            return teacher_options + group_options  # чем меньше, тем выше приоритет

        all_lessons.sort(key=get_lesson_priority)

        success_count = 0
        for teacher, subject_id, group in all_lessons:
            placed = False
            # Пробуем разместить занятие
            for time_slot in range(1, self.classes_count + 1):
                for classroom in self.classrooms:
                    if self.is_slot_free(teacher, group, classroom, time_slot):
                        lesson = Lesson(
                            teacher, subject_id, group, classroom, time_slot
                        )
                        self.timetable.append(lesson)
                        placed = True
                        success_count += 1
                        break
                if placed:
                    break

            if not placed:
                print(
                    f"Не удалось разместить: Преподаватель {teacher.id}, Группа {group.id}, Предмет {subject_id}"
                )

        print(f"Успешно размещено: {success_count}/{len(all_lessons)} занятий")
        return success_count == len(all_lessons)

    def print_timetable(self):
        if not self.timetable:
            print("Расписание пустое!")
            return

        table = []
        for i in range(self.classes_count):
            row = []
            for j in range(len(self.classrooms)):
                row.append(None)
            table.append(row)

        for lesson in self.timetable:
            row = lesson.time_slot - 1  # пары с 1, индексы с 0
            col = lesson.classroom.id - 1  # аудитории с 1, индексы с 0
            table[row][col] = lesson

        print("\n" + "=" * 90)
        print("РАСПИСАНИЕ НА ДЕНЬ")
        print("=" * 90)

        header = "Пара \\ Аудитория |"
        for room in self.classrooms:
            header += f"    Ауд {room.id}     |"
        print(header)
        print("-" * len(header))

        for time_slot in range(self.classes_count):
            row_str = f"     {time_slot + 1} пара      |"
            for room in self.classrooms:
                lesson = table[time_slot][room.id - 1]
                if lesson:
                    cell = f"T{lesson.teacher.id}-G{lesson.group.id}-S{lesson.subject_id}"
                    row_str += f" {cell:^14} |"
                else:
                    row_str += f" {'---':^14} |"
            print(row_str)

        print("=" * 90)


def main():
    print("ПОСТРОЕНИЕ РАСПИСАНИЯ")
    print("=" * 50)

    path = Path("time_table.json")
    path = path.absolute()
    print(path)

    timetable = Timetable(path)

    if timetable.build_timetable():
        print("\nРасписание успешно составлено!")
        timetable.print_timetable()
    else:
        print("\nНе удалось составить полное расписание!")
        if timetable.timetable:
            print("\nЧастичное расписание:")
            timetable.print_timetable()


if __name__ == "__main__":
    main()