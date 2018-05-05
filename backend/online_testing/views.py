from datetime import datetime

import pytz
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
import numpy as np
from rest_framework.viewsets import GenericViewSet, mixins

from online_testing.models import Question, Paper, Examination
from online_testing.serializers import QuestionSerializer, PaperSerializer, ExaminationSerializer
from online_testing.filters import QuestionFilter


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (DjangoFilterBackend, QuestionFilter)
    filter_fields = ('question_id',)

    @action(methods=['post'], detail=False)
    def batches_deletion(self, request):
        question_id_list = request.data.getlist('question_id_list')
        for question_id in question_id_list:
            self.queryset.get(question_id=question_id).delete()
        return Response({'question_list': question_id_list})

    @action(methods=['post'], detail=False)
    def condition_list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(QuestionViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        print(request.user)
        print(request.session)
        #for i in request.session:
        #    print(i)
        #print(request.auth)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'question_list': serializer.data})


class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

    def create(self, request, *args, **kwargs):

        def softmax(x):
            return np.exp(x) / np.sum(np.exp(x))

        data = request.data.copy()
        auto = False
        if isinstance(request.data.get('auto'), str):
            if request.data.get('auto') == 'True':
                auto = True
        else:
            auto = bool(request.data.get('auto'))
        if auto:
            num_choice = int(request.data.get('num_choice'))
            num_judge = int(request.data.get('num_judge'))
            question_set = QuestionFilter().filter_queryset(request, Question.objects.all(), None)
            choice_list = question_set.filter(type='Choice')
            judge_list = question_set.difference(choice_list)
            for choice in choice_list:
                print(choice.description)
            for judge in judge_list:
                print(judge.description)
            content = {'message': 'The questions are less than expected'}
            if choice_list.count() < num_choice or judge_list.count() < num_judge:
                return Response(content, status=status.HTTP_417_EXPECTATION_FAILED)
            l1 = [id for id in choice_list.values_list('question_id', 'level')]
            l2 = [id for id in judge_list.values_list('question_id', 'level')]
            np.random.shuffle(l1)
            np.random.shuffle(l2)
            l = l1[0: num_choice] + l2[0: num_judge]
            question_id_list = [li[0] for li in l]
            score_list = np.array(np.around(100 * softmax([li[1] for li in l])), dtype='int32')
            data.setlist('score_list', score_list)
            data.setlist('question_id_list', question_id_list)
        else:
            question_id_list = request.data.getlist('question_id_list')
            score_list = []
            for question_id in question_id_list:
                question = Question.objects.get(question_id=question_id)
                score_list.append(question.level)
            score_list = np.array(np.around(100 * softmax(score_list)), dtype='int32')
            data.setlist('score_list', score_list)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = dict(serializer.data)
        data['question_list'] = []
        for question_id in data['question_id_list']:
            question = Question.objects.all().get(question_id=question_id)
            data['question_list'].append(QuestionSerializer(question).data)
        data.pop('question_id_list')
        return Response(data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'paper_list': serializer.data})


class ExaminationViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   #mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer

    def create(self, request, *args, **kwargs):
        return super(ExaminationViewSet, self).create(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def left_time(self, request, pk=None):
        exam = self.get_object()
        left_time = 0
        if exam.submit:
            return Response({'left_time': left_time})
        left_time = exam.paper.duration * 60 - \
                    (datetime.now() - exam.start_time.replace(tzinfo=None)).total_seconds()
        return Response({'left_time': left_time})

    #@action(methods=['post'], detail=True)
    @action(methods=['get'], detail=True)
    def conservation(self, request, pk=None):
        exam = self.get_object()
        if not exam.begin and not exam.submit:
            exam.begin = True
            exam.start_time = datetime.now()
            exam.save()
            return Response({'message': 'start successfully', 'is_ok': True}, status=status.HTTP_200_OK)
        if exam.begin:
            return Response({'message': 'already began', 'is_ok': False},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'already submitted', 'is_ok': False},
                        status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['post'], detail=True)
    @action(methods=['get'], detail=True)
    def submission(self, request, pk=None):
        exam = self.get_object()
        if not exam.submit:
            exam.submit = True
            exam.save()
            return Response({'message': 'submit successfully', 'is_ok': True}, status=status.HTTP_200_OK)
        return Response({'message': 'never starts or already submitted', 'is_ok': False}, status=status.HTTP_400_BAD_REQUEST)
        # request.user


class AnalysisViewSet(GenericViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer

    @action(methods=['post'], detail=False)
    def student(self, request):
        # TODO:
        pass

    @action(methods=['post'], detail=False)
    def paper(self, request):
        # TODO:
        pass

    @action(methods=['post'], detail=False)
    def type(self, request):
        # TODO:
        pass

    @action(methods=['post'], detail=False)
    def tag(self, request):
        # TODO:
        pass


