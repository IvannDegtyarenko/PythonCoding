import json
from pathlib import Path
import os

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

        def get_lesson_priority(lesson):
            teacher, subject_id, group = lesson
            teacher_options = len([t for t in self.teachers.values() if t.can_teach(subject_id)])
            group_options = len([g for g in self.groups.values() if g.needs_subject(subject_id)])
            return teacher_options + group_options

        all_lessons.sort(key=get_lesson_priority)

        success_count = 0
        for teacher, subject_id, group in all_lessons:
            placed = False
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
        table = [[None for _ in self.classrooms] for _ in range(self.classes_count)]

        for lesson in self.timetable:
            row = lesson.time_slot - 1
            col = lesson.classroom.id - 1
            table[row][col] = lesson

        all_texts = ["---"]
        for lesson in self.timetable:
            text = f"Teacher{lesson.teacher.id} | Group{lesson.group.id} | Subject{lesson.subject_id}"
            all_texts.append(text)
        for room in self.classrooms:
            all_texts.append(f"Ауд {room.id}")

        min_cell_width = 20
        cell_width = max(min_cell_width, max(len(text) for text in all_texts) + 2)

        left_col_width = 18
        total_width = left_col_width + len(self.classrooms) * (cell_width + 3) + 1

        print("\n" + "=" * total_width)
        print(f"{'РАСПИСАНИЕ НА ДЕНЬ':^{total_width}}")
        print("=" * total_width)

        header = f"{'Пара \\ Аудитория':<{left_col_width}} |"
        for room in self.classrooms:
            header += f" {'Ауд ' + str(room.id):^{cell_width}} |"
        print(header)
        print("-" * total_width)

        for time_slot in range(self.classes_count):
            row_label = f"{time_slot + 1} пара"
            row_str = f"{row_label:>{left_col_width}} |"
            for room in self.classrooms:
                lesson = table[time_slot][room.id - 1]
                if lesson:
                    cell_text = f"Teacher{lesson.teacher.id} | Group{lesson.group.id} | Subject{lesson.subject_id}"
                else:
                    cell_text = "---"
                row_str += f" {cell_text:^{cell_width}} |"
            print(row_str)

        print("=" * total_width)


def main():
    print("ПОСТРОЕНИЕ РАСПИСАНИЯ")
    print("=" * 50)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "time_table.json")
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
    