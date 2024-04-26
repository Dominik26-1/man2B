from rest_framework import viewsets

from common.views import BasicView
from feedback.serializers import *


# Create your views here.

class CompanyView(BasicView):
    queryset = Company.objects.prefetch_related('departments')
    serializer_class = CompanySerializer

    def get_queryset(self):
        try:
            del Company.objects.all_feedbacks
        except AttributeError:
            pass
        return super(CompanyView, self).get_queryset()


class DepartmentView(BasicView):
    queryset = Department.objects.prefetch_related('teams')
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        try:
            del Department.objects.all_feedbacks
        except AttributeError:
            pass
        return super(DepartmentView, self).get_queryset()


class ProjectView(BasicView):
    queryset = Project.objects.prefetch_related('teams', 'positions')
    serializer_class = ProjectSerializer

    def get_queryset(self):
        try:
            del Project.objects.all_feedbacks
        except AttributeError:
            pass
        return super(ProjectView, self).get_queryset()


class TeamView(BasicView):
    queryset = Team.objects.prefetch_related('employees', 'projects')
    serializer_class = TeamSerializer

    def get_queryset(self):
        try:
            del Team.objects.all_feedbacks
        except AttributeError:
            pass
        return super(TeamView, self).get_queryset()


class EmployeeView(BasicView):
    queryset = Employee.objects.prefetch_related('projects')
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        try:
            del Employee.objects.all_feedbacks
        except AttributeError:
            pass
        return super(EmployeeView, self).get_queryset()


class PositionView(BasicView):
    queryset = Position.objects.prefetch_related('skills')
    serializer_class = PositionSerializer

    def get_queryset(self):
        try:
            del Position.objects.all_feedbacks
        except AttributeError:
            pass
        return super(PositionView, self).get_queryset()


class EmployeeManagementView(viewsets.ModelViewSet):
    queryset = EmployeeManagement.objects.all().prefetch_related('feedbacks')
    serializer_class = EmployeeManagementSerializer


class RatingView(viewsets.ModelViewSet):
    queryset = Rating.objects.all().prefetch_related('feedback')
    serializer_class = RatingSerializer


class FeedbackView(viewsets.ModelViewSet):
    queryset = Feedback.objects.prefetch_related('ratings')
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        try:
            del Feedback.objects.all_feedbacks
        except AttributeError:
            pass
        return super(FeedbackView, self).get_queryset()


class SkillView(viewsets.ModelViewSet):
    queryset = Skill.objects.prefetch_related('positions')
    serializer_class = SkillSerializer

    def get_queryset(self):
        try:
            del Skill.objects.all_feedbacks
        except AttributeError:
            pass
        return super(SkillView, self).get_queryset()
