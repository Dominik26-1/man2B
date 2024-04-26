import datetime
from decimal import Decimal

from django.test import TransactionTestCase
from rest_framework import status
from datetime import date

from .data_mock import *

URL_TEST_PREFIX = "http://testserver"


def create_sample_data():
    company = Company.objects.create(name="Company1")
    dep = Department.objects.create(name="Department1", company=company)
    team = Team.objects.create(name="Team1", department=dep)
    project = Project.objects.create(name="Project1")
    project.teams.add(team)
    emp = Employee.objects.create(first_name="Martin", last_name="Novak", team=team)
    emp2 = Employee.objects.create(first_name="Milan", last_name="Novak", team=team)
    skill = Skill.objects.create(name="Potential")
    position = Position.objects.create(name="Junior Developer")
    position.skills.add(skill)
    emp_mng = EmployeeManagement.objects.create(employee=emp, project=project, plan_iteration="Q1",
                                                position=position)
    emp_mng2 = EmployeeManagement.objects.create(employee=emp2, project=project, plan_iteration="Q1",
                                                 position=position)
    f1 = Feedback.objects.create(feedback="prvy feedback", rate_for=emp_mng, date=date.today(), author=emp)
    Feedback.objects.create(feedback="druhy feedback", rate_for=emp_mng2,
                            date=date.today() - datetime.timedelta(days=3), author=emp)
    Rating.objects.create(feedback=f1, skill=skill, rating=5)


# Create your tests here.
class TestCompany(TransactionTestCase):
    reset_sequences = True
    url = "/company/"

    def setUp(self):
        Company.objects.create(name="Company1")

    def test_get_companies(self):
        response = self.client.get(self.url)
        expected_company = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_company["name"], "Company1")
        self.assertEqual(expected_company["departments"], [])
        self.assertEqual(expected_company["average_rating"], 0.0)
        self.assertEqual(expected_company["url"], f"{URL_TEST_PREFIX}{self.url}1/")
        self.assertEqual(len(response.data), 1)

    def test_post_company(self):
        data = {"name": "Company2"}
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        company_data = self.client.get(self.url).data
        self.assertEqual(company_data[1]["name"], "Company2")

    def test_update_delete_company(self):
        pk = "1"
        company_url = f'{self.url}{pk}/'
        company_data = self.client.get(company_url).data
        company_data["name"] = "CompanyReplaced"
        response_company = self.client.put(company_url, data=company_data, content_type='application/json')
        self.assertEqual(response_company.status_code, status.HTTP_200_OK)
        self.assertEqual(company_data["name"], "CompanyReplaced")

        dlt_response = self.client.delete(company_url)
        self.assertEqual(dlt_response.status_code, status.HTTP_204_NO_CONTENT)
        no_company = self.client.get(company_url)
        self.assertEqual(no_company.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_same_company(self):
        data = {"name": "Company1"}
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDepartment(TransactionTestCase):
    reset_sequences = True
    url = "/department/"

    def setUp(self):
        company1 = Company.objects.create(name="Company1")
        Company.objects.create(name="Company2")
        Department.objects.create(name="Department1", company=company1)

    def test_get_department(self):
        response = self.client.get(self.url)
        expected_company = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_company["name"], "Department1")
        self.assertEqual(expected_company["teams"], [])
        self.assertEqual(expected_company["average_rating"], 0.0)
        self.assertEqual(expected_company["url"], f"{URL_TEST_PREFIX}{self.url}1/")
        self.assertEqual(len(response.data), 1)

    def test_post_department(self):
        data = {"name": "Department2",
                "company": "http://testserver/company/2/"}
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        department_data = self.client.get(self.url).data
        company = department_data[1]["company"]
        self.assertEqual(department_data[1]["name"], "Department2")
        self.assertEqual(company, "http://testserver/company/2/")
        department_urls = self.client.get(path=company).data["departments"]
        self.assertEqual(department_urls[0], f"{URL_TEST_PREFIX}{self.url}2/")

    def test_update_delete_department(self):
        pk = "1"
        dep_url = f"{self.url}{pk}/"
        dep_data = self.client.get(dep_url).data
        dep_data["name"] = "DepReplaced"
        response = self.client.put(dep_url, data=dep_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dep_data["name"], "DepReplaced")

        dlt_response = self.client.delete(dep_url)
        self.assertEqual(dlt_response.status_code, status.HTTP_204_NO_CONTENT)
        no_dep = self.client.get(dep_url)
        self.assertEqual(no_dep.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_same_dep(self):
        data = {"name": "Department1",
                "company": f"{URL_TEST_PREFIX}company/1/"}
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestEmployee(TransactionTestCase):
    reset_sequences = True
    url = "/employee/"

    def setUp(self):
        create_sample_data()

    def test_get_employee(self):
        response = self.client.get(self.url)
        employee = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(employee["first_name"], "Martin")
        self.assertEqual(employee["last_name"], "Novak")
        team_employee = self.client.get(employee["team"]).data["employees"][0]
        self.assertEqual(team_employee, f"{URL_TEST_PREFIX}/employee/1/")

    def test_post_employee(self):
        data = {"first_name": "Marek",
                "team": "http://testserver/team/1/",
                "last_name": "Skuska"}
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        employee_data = self.client.get(self.url).data
        self.assertEqual(employee_data[2]["first_name"], "Marek")

    def test_update_delete_employee(self):
        pk = "1"
        employee_url = f"{self.url}{pk}/"
        employee_data = self.client.get(employee_url).data
        employee_data["first_name"] = "Lukas"
        response = self.client.put(employee_url, data=employee_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(employee_data["first_name"], "Lukas")

        dlt_response = self.client.delete(employee_url)
        self.assertEqual(dlt_response.status_code, status.HTTP_204_NO_CONTENT)
        no_employee = self.client.get(employee_url)
        self.assertEqual(no_employee.status_code, status.HTTP_404_NOT_FOUND)


class TestFeedback(TransactionTestCase):
    reset_sequences = True
    url = "/feedback/"

    def setUp(self):
        create_sample_data()

    def test_get_feedback(self):
        response = self.client.get(self.url)
        feedbacks = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(feedbacks), 2)
        self.assertEqual(feedbacks[0]["feedback"], "prvy feedback")
        self.assertEqual(feedbacks[1]["feedback"], "druhy feedback")

    def test_post_feedback(self):
        data = {"feedback": "third feedback",
                "rate_for": "http://testserver/employee_management/1/",
                "date": "2022-05-09",
                "author": "http://testserver/employee/2/"}
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_delete_feedback(self):
        pk = "1"
        feedback_url = f"{self.url}{pk}/"
        feedback_data = self.client.get(feedback_url).data
        feedback_data["feedback"] = "replaced feedback"
        response = self.client.put(feedback_url, data=feedback_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(feedback_data["feedback"], "replaced feedback")

        dlt_response = self.client.delete(feedback_url)
        self.assertEqual(dlt_response.status_code, status.HTTP_204_NO_CONTENT)
        no_employee = self.client.get(feedback_url)
        self.assertEqual(no_employee.status_code, status.HTTP_404_NOT_FOUND)


class TestRating(TransactionTestCase):
    reset_sequences = True
    url = "/rating/"

    def setUp(self):
        create_sample_data()

    def test_get_rating(self):
        response = self.client.get(self.url)
        rating = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rating), 1)
        self.assertEqual(rating[0]["feedback"], f'{URL_TEST_PREFIX}/feedback/1/')
        self.assertEqual(rating[0]["rating"], 5)
        self.assertEqual(rating[0]["skill"], f'{URL_TEST_PREFIX}/skill/1/')

    def test_post_rating(self):
        data = {"feedback": "http://testserver/feedback/1/",
                "skill": "http://testserver/skill/1/",
                "rating": 9}
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        rat = self.client.get(f'{self.url}2/').data
        self.assertEqual(rat['rating'], 9)

    def test_update_delete_rating(self):
        pk = "1"
        rating_url = f"{self.url}{pk}/"
        rating_data = self.client.get(rating_url).data
        rating_data["rating"] = 8
        response = self.client.put(rating_url, data=rating_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(rating_url).data["rating"], 8)

        dlt_response = self.client.delete(rating_url)
        self.assertEqual(dlt_response.status_code, status.HTTP_204_NO_CONTENT)
        no_rating = self.client.get(rating_url)
        self.assertEqual(no_rating.status_code, status.HTTP_404_NOT_FOUND)


class TestCalculations(TransactionTestCase):
    reset_sequences = True
    url = "/employee/"

    def setUp(self):
        create_sample_data()
        python = Skill.objects.create(name="Python")
        java = Skill.objects.create(name="Java")
        sql = Skill.objects.create(name="SQL")
        f = Feedback.objects.all()

        Rating.objects.create(feedback=f[0], skill=python, rating=5)
        Rating.objects.create(feedback=f[0], skill=java, rating=7)
        Rating.objects.create(feedback=f[0], skill=sql, rating=8)

        Rating.objects.create(feedback=f[1], skill=python, rating=7)
        Rating.objects.create(feedback=f[1], skill=java, rating=9)
        Rating.objects.create(feedback=f[1], skill=sql, rating=7)

    def test_avg_rating_empl(self):
        response = self.client.get(self.url)
        employees = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(round(employees[0]['average_rating'], 2), (round(Decimal(25 / 4.0), 2)))
        self.assertEqual(employees[0]['count'], 1)
        self.assertEqual(employees[0]['latest_feedbacks'], 1)
        self.assertEqual(round(employees[1]['average_rating'], 2), (round(Decimal(23.0 / 3.0), 2)))
        self.assertEqual(employees[1]['count'], 1)
        self.assertEqual(employees[1]['latest_feedbacks'], 0)

    def test_latest_feed_param(self):
        response = self.client.get(f'{self.url}?days=5')
        employees = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(employees[1]['latest_feedbacks'], 1)

    def test_avg_rating_team(self):
        response = self.client.get("/team/")
        team = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(round(team["average_rating"], 2), round(Decimal(6.958333333333334), 2))
        self.assertEqual(team["count"], 2)
        self.assertEqual(team["latest_feedbacks"], 1)

    def test_latest_feed_param_team(self):
        response = self.client.get("/team/?days=10")
        team = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(team["latest_feedbacks"], 2)
