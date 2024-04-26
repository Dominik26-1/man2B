from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.models import BasicModel, CalculatedSummaryModel
from feedback.managers import CompanyManager, DepartmentManager, TeamManager, SkillManager, PositionManager, \
    EmployeeManager, ProjectManager, FeedbackManager


class Company(CalculatedSummaryModel):
    name = models.CharField(max_length=40, unique=True)

    objects = CompanyManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class Department(CalculatedSummaryModel):
    name = models.CharField(max_length=40)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, name="company", related_name="departments")

    objects = DepartmentManager()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'company')
        indexes = [
            models.Index(fields=['company']),
        ]


class Team(CalculatedSummaryModel):
    name = models.CharField(max_length=40)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, name="department",
                                   related_name="teams")
    objects = TeamManager()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'department')
        indexes = [
            models.Index(fields=['department']),
        ]


class Skill(CalculatedSummaryModel):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=50, null=True, blank=True)

    objects = SkillManager()

    def __str__(self):
        return self.name


class Position(CalculatedSummaryModel):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    skills = models.ManyToManyField(Skill, related_name="positions")

    objects = PositionManager()

    def __str__(self):
        return self.name


class Project(CalculatedSummaryModel):
    name = models.CharField(max_length=40, unique=True)
    teams = models.ManyToManyField(Team, related_name="projects")
    positions = models.ManyToManyField(Position, related_name="projects")

    objects = ProjectManager()

    def __str__(self):
        return self.name


class Employee(CalculatedSummaryModel):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, name="team", related_name="employees")
    projects = models.ManyToManyField(Project, through="EmployeeManagement", related_name="employees")

    objects = EmployeeManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        unique_together = ('first_name', 'last_name')
        indexes = [
            models.Index(fields=['team']),
        ]


class EmployeeManagement(BasicModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="employee_work")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_info")
    plan_iteration = models.CharField(max_length=5)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="filled_position")

    class Meta:
        unique_together = ('employee', 'project', 'plan_iteration')
        verbose_name_plural = "Employee Management"


class Feedback(CalculatedSummaryModel):
    feedback = models.CharField(max_length=80)
    rate_for = models.ForeignKey(EmployeeManagement, on_delete=models.CASCADE, related_name="feedbacks")
    date = models.DateField()
    author = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="give_feedback")

    objects = FeedbackManager()

    def __str__(self):
        return f'{self.feedback}'

    class Meta:
        unique_together = ('author', 'rate_for')
        indexes = [
            models.Index(fields=['rate_for']),
        ]


class Rating(BasicModel):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name="ratings")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)])

    def __str__(self):
        return f'{self.skill.name} : {self.rating}'

    class Meta:
        indexes = [
            models.Index(fields=['feedback']),
        ]
