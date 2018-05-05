import uuid

from django.db import models
import ast
import django.utils.timezone as timezone
from authentication.models import Faculty, Course, Student


class ListField(models.TextField):
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value
        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


# Create your models here.
class Question(models.Model):
    QUESTION_TYPE = (
        ('Choice', 'Choice'),
        ('Judge', 'Judge'),
    )
    QUESTION_LEVEL = (
        (0, 'Very Easy'),
        (1, 'Easy'),
        (2, 'Medium'),
        (3, 'Difficult'),
        (4, 'Very Difficult')
    )
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    description = models.TextField(null=False)
    choice_list = ListField(null=False)
    answer_list = ListField(null=False)
    tag = models.CharField(max_length=32)
    type = models.CharField(choices=QUESTION_TYPE, null=False, max_length=12, default='Choice')
    level = models.IntegerField(choices=QUESTION_LEVEL, null=False, default=0)
    provider = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)


class Paper(models.Model):
    paper_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    paper_name = models.CharField(max_length=128, null=False)
    start_time = models.DateTimeField(default=timezone.now())
    deadline = models.DateTimeField(default=timezone.now())
    duration = models.IntegerField()
    question_id_list = ListField(null=False)
    # question_id_list = models.ManyToManyField(Question)
    score_list = ListField(null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)


class Examination(models.Model):
    exam_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    teacher = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    answers = models.FileField(upload_to='answers/', null=True)
    score = models.SmallIntegerField(null=False, default=-1)
    start_time = models.DateTimeField(default=timezone.now())
    submit = models.BooleanField(default=False)