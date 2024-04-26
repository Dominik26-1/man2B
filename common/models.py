from datetime import date, timedelta

import numpy as np
from django.db import models
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.functional import cached_property


# Create your models here.
def get_feedbacks(instance):
    company_feedbacks = list(filter(lambda f: f.group_id == instance.id, type(instance).objects.all_feedbacks))
    return company_feedbacks


class BasicModel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class CalculatedSummaryModel(BasicModel):

    def new_feedback_count(self, params):
        try:
            days = int(params['days'])
        except (MultiValueDictKeyError, ValueError, TypeError):
            days = 0
        feedbacks = get_feedbacks(self)
        reference_date = date.today() - timedelta(days=days)
        last_feedbacks = list(filter(lambda f: f.date >= reference_date, feedbacks))
        return len(last_feedbacks)

    @cached_property
    def count(self):
        return len(get_feedbacks(self))

    @cached_property
    def average_rating(self):
        # average rating from all feedbacks
        feedbacks = get_feedbacks(self)
        if len(feedbacks) == 0:
            return 0
        averages = list(map(lambda f: f.avg, feedbacks))
        return np.mean([averages])

    class Meta:
        abstract = True
