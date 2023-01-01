import enum



class Task_status(enum.Enum):
    task_standby = 'task_standby'
    task_close = 'task_close'
    task_open = 'task_open'


class Genders_person(enum.Enum):
    male = 'male'
    female = 'female'

    