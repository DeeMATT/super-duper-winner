from .models import Pages
from .serializers import (
    PageSerializer, transformPage, transformPageDataSet
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .utils import (
    validate_keys, get_page_by_slug, get_page_by_title
)


class PageListView(APIView):
    """
    List all pages, or create a new page.
    """
    
    def get(self, request, format=None):
        pages = Pages.objects.all()
        serializer = PageSerializer(pages, many=True)
        return Response(transformPageDataSet(serializer.data))

    def post(self, request, format=None):
        data = request.data
        serializer = PageSerializer(data=data)
        if serializer.is_valid():

            body = data.get('body')
            # check if required fields are present in body object
            missingKeys = validate_keys(payload=body, requiredKeys=['html', 'css', 'js'])
            if missingKeys:
                raise serializers.ValidationError({
                    "body": "The body field should contain the key and values for: ['html', 'css', 'js']"
                })

            # check if title already exists
            title = data.get('title')
            if get_page_by_title(title):
                raise serializers.ValidationError({
                    "title": "There is an already existing record with same title"
                })

            serializer.save()
            return Response(transformPage(serializer.data), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PageDetailView(APIView):
    """
    Retrieve, update or delete a page instance.
    """
    def get_object(self, slug):
        obj = get_page_by_slug(slug)
        if not obj:
            raise Http404
        
        return obj

    def get(self, request, slug, format=None):
        page = self.get_object(slug=slug)
        serializer = PageSerializer(page)
        return Response(transformPage(serializer.data))

    def put(self, request, slug, format=None):
        page = self.get_object(slug)
        data = request.data
        serializer = PageSerializer(page, data=data)
        if serializer.is_valid():

            body = data.get('body')
            # check if required fields are present in body object
            missingKeys = validate_keys(payload=body, requiredKeys=['html', 'css', 'js'])
            if missingKeys:
                raise serializers.ValidationError({
                    "body": "The body field should contain the key and values for: ['html', 'css', 'js']"
                })

            # check if title already exists
            title = data.get('title')
            existing_page = get_page_by_title(title)
            if existing_page and page.id != existing_page.id:
                raise serializers.ValidationError({
                    "title": "There is an already existing record with same title"
                })

            serializer.save()
            return Response(transformPage(serializer.data))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        page = self.get_object(slug)
        page.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
