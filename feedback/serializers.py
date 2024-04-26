from rest_framework import serializers

from common.serializers import BasicSerializer
from .models import *


class CompanySerializer(BasicSerializer):
    model = Company
    departments = serializers.HyperlinkedRelatedField(many=True, queryset=Department.objects.all(),
                                                      view_name="department-detail")
    latest_feedbacks = serializers.SerializerMethodField(read_only=True, required=False, source='get_latest_feedbacks')

    class Meta(BasicSerializer.Meta):
        model = Company
        fields = ['url', 'name', 'departments', 'average_rating', 'count', 'latest_feedbacks']


class DepartmentSerializer(BasicSerializer):
    model = Department
    teams = serializers.HyperlinkedRelatedField(many=True, queryset=Team.objects.all(),
                                                view_name="team-detail")
    latest_feedbacks = serializers.SerializerMethodField(read_only=True, required=False, source='get_latest_feedbacks')

    class Meta(BasicSerializer.Meta):
        model = Department
        fields = ['url', 'name', 'company', 'teams', 'average_rating', 'count', 'latest_feedbacks']


class TeamSerializer(BasicSerializer):
    model = Team
    projects = serializers.HyperlinkedRelatedField(many=True, queryset=Project.objects.all(),
                                                   view_name="project-detail")
    latest_feedbacks = serializers.SerializerMethodField(read_only=True, required=False, source='get_latest_feedbacks')

    class Meta(BasicSerializer.Meta):
        model = Team
        fields = ['url', 'name', 'projects', 'employees', 'department', 'average_rating', 'count', 'latest_feedbacks']


class ProjectSerializer(BasicSerializer):
    model = Project
    latest_feedbacks = serializers.SerializerMethodField(read_only=True, required=False, source='get_latest_feedbacks')

    class Meta(BasicSerializer.Meta):
        model = Project
        fields = ['url', 'name', 'teams', 'positions', 'average_rating', 'count', 'latest_feedbacks']


class EmployeeSerializer(BasicSerializer):
    model = Employee
    latest_feedbacks = serializers.SerializerMethodField(read_only=True, required=False, source='get_latest_feedbacks')

    class Meta(BasicSerializer.Meta):
        model = Employee
        fields = ['url', 'first_name', 'last_name', 'team', 'projects', 'average_rating', 'count', 'latest_feedbacks']


class PositionSerializer(BasicSerializer):
    model = Position
    latest_feedbacks = serializers.SerializerMethodField(read_only=True, required=False, source='get_latest_feedbacks')

    class Meta(BasicSerializer.Meta):
        model = Position
        fields = ['url', 'name', 'description', 'skills', 'average_rating', 'count', 'latest_feedbacks']


class EmployeeManagementSerializer(serializers.HyperlinkedModelSerializer):
    model = EmployeeManagement
    feedbacks = serializers.HyperlinkedRelatedField(many=True, queryset=Feedback.objects.all(),
                                                    view_name="feedback-detail")

    class Meta:
        model = EmployeeManagement
        fields = '__all__'


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    model = Rating

    class Meta:
        model = Rating
        fields = '__all__'


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    model = Feedback
    ratings = serializers.HyperlinkedRelatedField(many=True,
                                                  queryset=Rating.objects.all().select_related('feedback', 'skill'),
                                                  view_name="rating-detail")

    class Meta(BasicSerializer.Meta):
        model = Feedback
        fields = ['url', 'feedback', 'date', 'rate_for', 'ratings', 'author', 'average_rating']


class SkillSerializer(BasicSerializer):
    model = Skill
    positions = serializers.HyperlinkedRelatedField(many=True, queryset=Position.objects.all(),
                                                    view_name="position-detail")

    class Meta(BasicSerializer.Meta):
        model = Skill
        fields = ['url', 'name', 'description', 'positions', 'average_rating', 'count']
