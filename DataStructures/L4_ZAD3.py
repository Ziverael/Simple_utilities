import random
import sys
"""
Rozważ sytuację z życia wziętą, np.: 
- auta w kolejce do myjni,
- kasy w supermarkecie,
- samoloty na pasie startowym, 
- okienko w banku. 
Postaw pytanie badawcze. Wykorzystując liniowe struktury danych 
zaprojektuj i przeprowadź symulację, która udzieli na nie odpowiedzi. 
Pamiętaj o określeniu wszystkich uproszczeń swojego modelu. 
 """

"""
Variables representing length required to preparation, number of tasks, points to score and how long time student has to achieve task.
"""
semester = 15 * 7 * 2 # 15 weeks * 7 days * 2 half of the day
lengths = {'l' : [.5, 1, 1.5], 'c' : [3, 4, 5, 5.5], 'e' : [6, 7, 8, 9]}
tasks = {'l' : 14 , 'c' : 2, 'e' : 1}
points = {'l' : .75, 'c' : 20, 'e' : 40}
deadlines = {'l' : 7, 'c' : 14, 'e' : 20}

def test_date():
    """
    Return test dates
    """
    test1 = (5, 6, 7, 8)
    test2 = (11, 12, 13, 14)
    return random.choice(test1), random.choice(test2)

def if_give_test(week):
    """
    Return True if test is assign to student and False in other situation.
    In following weeks probability raises from 25% to 100% in 4 weeks
    that usually tests appears.
    """
    if week < 7:
        sett = week - 2
    else:
        sett = week - 8
    chance = []
    while sett:
        chance.append(1)
        sett -= 1
    while len(chance) < 4:
        chance.append(0)
    if random.choice(chance):
        return True
    else:
        return False

"""Data structure"""
class Stack():
    def __init__(self):
        self.l = []
    
    def push(self, item):
        self.l.append(item)
    
    def pop(self):
        return self.l.pop()
    
    def size(self):
        return len(self.l)
    
    def peek(self):
        return self.l[-1]

    def is_empty(self):
        return self.l == []


class Student():
    """
    Student class.
    ATRIBUTES
    ---------
    task_stack - stack of Task  objects
    
    METHODS
    -------
    take(task)
    Take a new task.

    Args:
    task - Task object

    Return none

    do_your_job(clock)
    Evaluate tasks. If student speds enought time on the task he will score points. Also student scores points if its taks's deadline.
    It's called per every half day.

    Args:
    clock - actual time

    Return:
    total - list of tuples (course id, points)
    """
    def __init__(self):
        self.tasks_stack = Stack()
    
    def take(self, task):
        self.tasks_stack.push(task)
    
    def do_your_job(self, clock):
        total = []
        if not self.tasks_stack.is_empty():
            while self.tasks_stack.peek().get_deadline() >= clock:
                buffer = self.tasks_stack.pop()
                course = buffer.get_course()
                points = buffer.resolve()
                total.append((course, points))
                if self.tasks_stack.is_empty():
                    break

        if not self.tasks_stack.is_empty():
            buffer = self.tasks_stack.peek()
            points = buffer.evaluate()
            if points:
                course = self.tasks_stack.pop().get_course()
                total.append((course, points))
            
        return total


class Course():
    """
    Course representation.
    ATRIBUTES
    ---------
    type_ - course type
    exam -  if course has final exam (only for lectures)
    objectives - number of assignments
    tests - dates of assigning tests
    score - student's score
    id -    course id
    week_day -  week day of classes

    METHODS
    -------

    get_id()
    Return course id.

    get_objectives()
    Return number of following objectives.

    get_type()
    Return course type.

    get_week_day()
    Return week_day attribute.

    get_test_dates()
    Return test_dates or nothing if type_ is differ than lectures.

    get_exam_date()
    Return exam date.

    give_task(student, deadline, type)
    Give task for a student.

    Args:
    student - Student object
    deadline - task deadline
    type - task type ('l' - list, 'c' - test, 'e' - exam)

    Return:
    None or False if not avaliable any objective
    
    result(string = False)
    Return score and feedback about course.

    Args:
    string (=False) If return string representation

    Return:
    1 if passed or 0 if not and string instead if string argument is True

    return_task(points)
    Student scores points.

    Args:
    points -  points

    Return:
    None
    """
    def __init__(self, type_, id_, week_day, exam = False):
        self.type_ = type_
        self.exam = exam
        if type_ == "lectures":
            if exam:
                self.objectives = tasks['e'] + tasks['c']
                self.exam_date =  week_day #exam date
            else:
                self.objectives = tasks['c']
            self.tests = test_date() # Test week
        else:
            self.objectives = tasks['l']
        self.score = 0
        self.id = id_
        self.week_day = week_day
    
    def __str__(self):
        return "Course\n" + "-" * 10 + "\nId {}\nType {}\nScore {}\nWeek day {}\nObjectives {}\nExam {}\n".format(self.id, self.type_, self.score, self.week_day, self.objectives, self.exam) 

    def __repr__(self):
        return str(self)

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type_

    def get_objectives(self):
        return self.objectives
    
    def get_week_day(self):
        return self.week_day

    def get_test_dates(self):
        if self.type_ == "lectures":
            return self.tests
        else:
            return False
    
    def get_exam_date(self):
        if self.type_ == "lectures" and self.exam:
            return self.exam_date
        else:
            return False

    def give_task(self, student, deadline, type_):
        if self.objectives <= 0:
            return False
        self.objectives -= 1

        student.take(Task(type_, deadline , self.id))

    def result(self, string = False):
        if self.type_ == 'lectures':
            if self.exam:
                min_ = 45
            else:
                min_ = 25.25
            if self.score > min_:
                result = "Passed", 1 
            else:
                result = "Failed", 0 
            if string:
                return "Grade" + "-" * 10 + "\n score: {} / {}\nResult {}\n".format(self.score, min_ * 2, result[0])
            return result[1]
        return None
    def return_task(self, points):
        self.score += points

class Task():
    """
    Task representation
    ATTRIBUTES
    ----------
    length - time required to finish
    type_ - type of the task
    deadline - when task is evaluated
    course - course which assign the task
    to_finish - remaining time

    METHODS
    -------
    get_deadline()
    Return deadline.

    get_course()
    Return course.

    evaluate()
    Decrease remaining time (student practice) and resolve if student finished preparation or it's a taks's deadline.

    Return:
    points scored

    resolve()
    Return points depend on student practice and total value.


    """
    def __init__(self, type_, deadline, course):
        self.length = random.choice(lengths[type_])
        self.to_finish = self.length
        self.type_ = type_
        self.deadline = deadline
        self.course = course
    
    def get_deadline(self):
        return self.deadline

    def evaluate(self):
        self.to_finish -= .5
        if self.to_finish <= 0:
            return self.resolve()
        else:
            return 0
    
    def resolve(self):
        return points[self.type_] * ((self.length - self.to_finish) / self.length)

    def get_course(self):
        return self.course

    def __str__(self):
        return "Task\n" + "-" * 10 + "\nLength {}\nRemaining {}\nDeadline {}\nCourse id {}".format(self.length, self.to_finish, self.deadline, self.course)


def simulation(time):
    """
    Simulate semester going.

    Args:
    time - length of the semester

    Return:
    Number of passed courses.
    """

    student = Student()
    courses = [Course('lectures', i, i) for i in range(1, 3)]
    courses.extend([Course('lectures', i, i, exam = True) for i in range(3, 6)])
    courses.extend([Course('labs', i, i) for i in range(1, 6)])

    while  time: 
        ###SCORING###       
        points = student.do_your_job(time)
        if points:
            #print(points, time)
            i, j = 0, 0
            while j < len(points):
                while courses[i].get_id() != points[j][0]:
                    i += 1
                courses[i].return_task(points[j][1])
                i = 0
                j += 1
            
        ###GIVING TASKS###
        week_day = (time % 14) / 2
        week = 15 - int(time / 14)

        if int(week_day) == week_day: #New day

            for i in courses:
                if i.get_week_day() == week_day:
                    if i.get_type() == 'lectures':
                        for j in i.get_test_dates():
                            if j - week == 2:
                                i.give_task(student, time - 2 * deadlines['c'], 'c')
                        if week == 12 and i.get_exam_date() == week_day: # Time to prepare for exam
                            i.give_task(student, time - 2 * deadlines['e'], 'e')
                    else:
                        i.give_task(student, time - 2 * deadlines['l'], 'l')

        time -= 1
        
    count = 0
    for i in courses:
        buff = i.result()
        if buff != None:
            count += buff
    return count

def main(probes):
    for i in probes:
        try:
            i = int(i)
        except:
            raise TypeError
        sum_ = 0
        divisor = i
        while i:
            sum_ += simulation(semester)
            i -= 1
        print("Average: ",sum_ / divisor)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main([500])
    else:
        main(sys.argv[1 : ])