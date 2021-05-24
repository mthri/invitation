from django.views.generic import View
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from utils.response import SuccessJsonResponse, BadJsonResponse

class SetToListJSONEncoder(DjangoJSONEncoder):
     def default(self, o):
        if isinstance(o, set):
            return list(o)
        else:
            return super().default(o)


class DataTableView(View):
    http_method_names = ['post', 'options']
    max_length = 100
    queryset = None
    result_args = None
    result_kwargs = None
    search_on = None

    def post(self, request, *args, **kwargs):
        count = self.queryset.count()

        # get data from client
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 0))
        search = request.POST.get('search', None)

        if search and search.strip() != '':
            search_field = { self.search_on+'__icontains': search }
            self.queryset = self.queryset.filter(**search_field)

        # we can't set length  greater than max_length
        if length > self.max_length:
            length = self.max_length

        # limit our result
        self.queryset = self.queryset[start:(start+length)]

        results = list(self.queryset.values(*self.result_args, **self.result_kwargs))

        return SuccessJsonResponse({'data': results, 'iTotalDisplayRecords': count, 'iTotalRecords': count}, 
                                    encoder=SetToListJSONEncoder)