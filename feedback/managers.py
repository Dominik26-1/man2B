from common.managers import BasicManager


class CompanyManager(BasicManager):
    def get_sql_feedback(self):
        sql = 'select com.id as group_id, feedback.id as id, feedback.date as date, avg(rat.rating) from feedback_feedback feedback ' \
              'join feedback_rating rat on feedback.id = rat.feedback_id ' \
              'join feedback_employeemanagement em on feedback.rate_for_id = em.id ' \
              'join feedback_employee empl on em.employee_id = empl.id ' \
              'join feedback_team team on empl.team_id = team.id ' \
              'join feedback_department dep on dep.id = team.department_id ' \
              'join feedback_company com on com.id = dep.company_id ' \
              'group by com.id, feedback.id ' \
              'order by com.id'
        return sql


class DepartmentManager(BasicManager):
    def get_sql_feedback(self):
        sql = 'select dep.id as group_id, feedback.id as id, feedback.date as date, avg(rat.rating) from feedback_feedback feedback ' \
              'join feedback_rating rat on feedback.id = rat.feedback_id ' \
              'join feedback_employeemanagement em on feedback.rate_for_id = em.id ' \
              'join feedback_employee empl on em.employee_id = empl.id ' \
              'join feedback_team team on empl.team_id = team.id ' \
              'join feedback_department dep on dep.id = team.department_id ' \
              'group by dep.id, feedback.id ' \
              'order by dep.id'
        return sql


class TeamManager(BasicManager):
    def get_sql_feedback(self):
        sql = 'select team.id as group_id, feedback.id as id, feedback.date as date, avg(rat.rating) ' \
              'from feedback_feedback feedback ' \
              'join feedback_rating rat on feedback.id = rat.feedback_id ' \
              'join feedback_employeemanagement em on feedback.rate_for_id = em.id ' \
              'join feedback_employee empl on em.employee_id = empl.id ' \
              'join feedback_team team on empl.team_id = team.id ' \
              'group by team.id, feedback.id ' \
              'order by team.id'
        return sql


class ProjectManager(BasicManager):
    def get_sql_feedback(self):
        sql = 'select proj.id as group_id, feedback.id as id, feedback.date as date, avg(rat.rating) from feedback_feedback feedback ' \
              'join feedback_rating rat on feedback.id = rat.feedback_id ' \
              'join feedback_employeemanagement em on feedback.rate_for_id = em.id ' \
              'join feedback_project proj on em.project_id = proj.id ' \
              'group by proj.id, feedback.id ' \
              'order by proj.id'
        return sql


class EmployeeManager(BasicManager):
    def get_sql_feedback(self):
        sql = 'select empl.id as group_id, feedback.id as id, feedback.date as date, avg(rat.rating) from feedback_feedback feedback ' \
              'join feedback_rating rat on feedback.id = rat.feedback_id ' \
              'join feedback_employeemanagement em on feedback.rate_for_id = em.id ' \
              'join feedback_employee empl on em.employee_id = empl.id ' \
              'group by empl.id, feedback.id ' \
              'order by empl.id'
        return sql


class PositionManager(BasicManager):
    def get_sql_feedback(self):
        sql = 'select pos.id as group_id, feedback.id as id, feedback.date as date, avg(rat.rating) from feedback_feedback feedback ' \
              'join feedback_rating rat on feedback.id = rat.feedback_id ' \
              'join feedback_employeemanagement em on feedback.rate_for_id = em.id ' \
              'join feedback_position pos on pos.id = em.position_id ' \
              'group by pos.id, feedback.id ' \
              'order by pos.id'
        return sql


class SkillManager(BasicManager):
    def get_sql_feedback(self):
        sql = 'select skill.id as group_id, feedback.id as id, feedback.date as date, avg(rat.rating) from feedback_feedback feedback ' \
              'join feedback_rating rat on feedback.id = rat.feedback_id ' \
              'join feedback_skill skill on skill.id = rat.skill_id ' \
              'group by skill.id, feedback.id ' \
              'order by skill.id'
        return sql


class FeedbackManager(BasicManager):
    def get_sql_feedback(self):
        sql = 'select feedback.id as group_id, feedback.id as id, feedback.date as date, avg(rat.rating) from feedback_feedback feedback ' \
              'join feedback_rating rat on feedback.id = rat.feedback_id ' \
              'group by feedback.id ' \
              'order by feedback.id'
        return sql
