from django.db import models
from django.utils.functional import cached_property


class BasicManager(models.Manager):
    @cached_property
    def all_feedbacks(self):
        from feedback.models import Feedback
        feedbacks = Feedback.objects.raw(
            self.get_sql_feedback())
        return list(feedbacks)

    def get_sql_feedback(self):
        raise NotImplementedError("SQL command to retrieve feedbacks is not implemented.")

    class Meta:
        abstract = True
