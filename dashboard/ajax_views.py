from django.http import JsonResponse
from django.views.generic import View
from django.core.paginator import Paginator
from django.db.models import F, Value as V

from utils.response import SuccessJsonResponse, BadJsonResponse
from .mixins import PremissionMixin
from .ajax_forms import AddTagForm
from .models import Tag, Contact
from utils.generic_view import DataTableView, Select2View


class AddTag(PremissionMixin, View):
    http_method_names = ['post', 'options']

    def post(self, request, *args, **kwargs):
        form = AddTagForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return SuccessJsonResponse()

        errors = {'errors': dict(form.errors.get_json_data())}
        return BadJsonResponse(errors)


# This view used for DataTable
# TODO use DataTable View
class GetTags(PremissionMixin, View):
    http_method_names = ['post', 'options']
    max_length = 100

    def post(self, request, *args, **kwargs):
        # get user tags
        all_user_tags = Tag.get_by_user(request.user)
        count = all_user_tags.count()

        # get data from client
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 0))
        search = request.POST.get('search', None)

        if search and search.strip() != '':
            all_user_tags = all_user_tags.filter(name__icontains=search)

        # we can't set length  greater than max_length
        if length > self.max_length:
            length = self.max_length

        # limit our result
        all_user_tags = all_user_tags[start:(start+length)]

        results = list(all_user_tags.values(
            Id=F('id'), Name=F('name'), Description=F('description')))

        return SuccessJsonResponse({'data': results, 'iTotalDisplayRecords': count, 'iTotalRecords': count})


class RemoveTag(PremissionMixin, View):
    http_method_names = ['post', 'options']

    def post(self, request, tag_id: int, *args, **kwargs):
        user_tags = Tag.get_by_user(request.user)
        user_tags.filter(id=tag_id).delete()
        return SuccessJsonResponse()


class GetContact(PremissionMixin, DataTableView):
    result_args = ('id', 'tags',)
    result_kwargs = {'firstName': F('first_name'), 
                     'lastName': F('last_name'), 
                     'created': F('created_at'),
                     'contactInfo': F('communicative_road')}

    search_on = 'last_name'

    def post(self, request, *args, **kwargs):
        self.queryset = Contact.get_by_user(request.user)
        return super().post(request, *args, **kwargs)


class GetTagSelect2(PremissionMixin, Select2View):
    http_method_names = ['post']
    search_on = ('name', )
    result_args = ('id',)
    result_kwargs = {'text':F('name')}
    def post(self, request, *args, **kwargs):
        self.queryset = Tag.get_by_user(request.user)
        return super().post(request, *args, **kwargs)


class GetContactSelect2(PremissionMixin, Select2View):
    http_method_names = ['post']
    search_on = ['first_name', 'last_name']
    result_args = ('id',)
    def post(self, request, *args, **kwargs):
        self.queryset = Contact.get_by_user(request.user)
        return super().post(request, *args, **kwargs)