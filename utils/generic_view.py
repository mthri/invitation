from django.views.generic import View
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F

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
            #TODO add multi query support
            search_field = {self.search_on+'__icontains': search}
            self.queryset = self.queryset.filter(**search_field)

        # we can't set length  greater than max_length
        if length > self.max_length:
            length = self.max_length

        # limit our result
        self.queryset = self.queryset[start:(start+length)]

        results = list(self.queryset.values(
            *self.result_args, **self.result_kwargs))

        return SuccessJsonResponse({'data': results, 'iTotalDisplayRecords': count, 'iTotalRecords': count},
                                   encoder=SetToListJSONEncoder)


class Select2View(View):
    http_method_names = ['post', 'get']
    queryset = None
    search_on = None
    max_length = 10
    search_key = 'query'
    result_args = None
    result_kwargs = None

    def get(self, request, *args, **kwargs):
        search = request.GET.get(self.search_key, '')
        search_field = {self.search_on+'__icontains': search}
        # limit output result
        self.queryset = self.queryset.filter(**search_field)[:self.max_length]
        # only show required field
        result = list(self.queryset.values(*self.result_args, **self.result_kwargs))
        return SuccessJsonResponse({'data': result})

    def post(self, request, *args, **kwargs):
        #TODO find better solution
        post_data = request.POST.dict()
        get_date = request.GET.dict()
        get_date.update(post_data)
        request.GET = get_date
        return self.get(request, *args, **kwargs)
