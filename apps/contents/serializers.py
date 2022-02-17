from rest_framework import serializers
from .models import Pages


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pages
        # fields = "__all__"
        exclude = ['id']
        read_only_fields = ['published_at', 'updated_at']


def transformPage(obj):
    title = obj['title'].lower()

    return {
        title: obj
    }

def transformPageDataSet(dataset):
    return list(map(lambda x: transformPage(x), dataset))
