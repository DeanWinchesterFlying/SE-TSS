import ast

from rest_framework import serializers
from online_testing.models import Question, Paper, Examination


class ListField(serializers.ListField):
    def to_representation(self, data):
        if not isinstance(data, list):
            data = ast.literal_eval(data)
        return super(ListField, self).to_representation(data)


class QuestionSerializer(serializers.ModelSerializer):
    answer_list = ListField(child=serializers.IntegerField())
    choice_list = ListField(child=serializers.CharField())
    teacher_name = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('question_id', 'description', 'choice_list', 'answer_list',
                  'tag', 'type', 'level', 'teacher_name')

    def get_level(self, obj):
        return obj.get_level_display()

    def get_teacher_name(self, obj):
        return 'chen yue'


class PaperSerializer(serializers.ModelSerializer):
    question_id_list = ListField(child=serializers.IntegerField())
    score_list = ListField(child=serializers.IntegerField())

    class Meta:
        model = Paper
        fields = '__all__'


class ExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        fields = '__all__'