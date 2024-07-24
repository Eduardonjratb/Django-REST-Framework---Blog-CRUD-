from django.shortcuts import get_object_or_404
from .models import Postt


class MultipleFieldLookupMixin:


    def get_object(self):
        queryset = self.get_queryset() 
        queryset = self.filter_queryset(queryset)  
        filter = {}
        parent_id = Postt.objects.get(slug=self.kwargs["slug"]).id
        filter["parent"] = parent_id
        filter["id"] = self.kwargs["id"]
        obj = get_object_or_404(queryset, **filter)  
        self.check_object_permissions(self.request, obj)
        return obj