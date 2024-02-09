import re

import django_filters as filters
from django_filters import (FilterSet, ModelChoiceFilter,
                            ModelMultipleChoiceFilter, DateFilter, DateTimeFilter,
                            DateFromToRangeFilter, NumberFilter, DateRangeFilter)
from django.contrib.auth.models import User
from .models import Post, Category
from django.forms import SelectDateWidget


YEARS = [2018 + x for x in range(1, 8)]


class PostFilter(FilterSet):

    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Категории',
        conjoined=True,
    )

    # Одна строчка весь день заняла(((.
    time_created = DateFilter(label='Дата публикации после',
        lookup_expr='gt',
        widget=SelectDateWidget(years=YEARS))

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }






