from django.views.generic import View
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F, Value
from django.db.models.functions import Concat

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
    result_args:tuple = None
    result_kwargs:dict = None
    search_on:tuple = None

    def post(self, request, *args, **kwargs):
        count = self.queryset.count()

        # get data from client
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 0))
        search = request.POST.get('search', None)

        search_field = dict()

        if search and search.strip() != '':
                
            for search_key in self.search_on:
                search_field.update({search_key+'__icontains': search})

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
    search_on:list = None
    max_length = 10
    search_key = 'query'
    result_args = None
    result_kwargs = None

    def get(self, request, *args, **kwargs):
        search = request.GET.get(self.search_key, '')
        #TODO do it like datatable
        if len(self.search_on) > 1:
            _tmp = []
            for index, value in enumerate(self.search_on):
                if index != 0 and index % 2 != 0:
                    _tmp.append(Value(' '))
                _tmp.append(value)

            self.queryset = self.queryset.annotate(concated=Concat(*_tmp))\
                                         .filter(concated__icontains=search)[:self.max_length]
            if not self.result_kwargs:
                self.result_kwargs = {'text': F('concated')}
        else:
            self.search_on = self.search_on[0]
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
