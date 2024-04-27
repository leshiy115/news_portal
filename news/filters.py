import re

import django_filters as filters
from django_filters import (FilterSet, ModelChoiceFilter,
                            ModelMultipleChoiceFilter, DateFilter, DateTimeFilter,
                            DateFromToRangeFilter, NumberFilter, DateRangeFilter)
from django.contrib.auth.models import User
from .models import Post, Category
from django.forms import SelectDateWidget
from django.utils.translation import gettext_lazy as _


YEARS = [2018 + x for x in range(1, 8)]


class PostFilter(FilterSet):

    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label=_('Categories'),
        conjoined=True,
    )

    # Одна строчка весь день заняла(((.
    time_created = DateFilter(label=_('Publication date after'),
        lookup_expr='gt',
        widget=SelectDateWidget(years=YEARS))

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }






