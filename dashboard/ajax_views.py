from datetime import datetime
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.views.generic import View
from django.db.models import F, Count, Value as V
from django.utils.translation import ugettext_lazy as _

from utils.response import SuccessJsonResponse, BadJsonResponse
from .mixins import PremissionMixin, JsonValidatorMixin
from .ajax_forms import AddTagForm
from .models import Invitation, Tag, Contact, Template
from utils.generic_view import DataTableView, Select2View
from .json_schema import create_invite_card, communicates
from utils.validators import is_phone_number
from utils.time import format_date

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


class AddContact(PremissionMixin, JsonValidatorMixin, View):
    http_method_names = ['post']
    json_body_schema = communicates
    
    def post(self, request:HttpRequest, *args, **kwargs):
    
        if not is_phone_number(self.json_body['phone']):
            return BadJsonResponse({'message': _('فرمت تلفن همراه صحیح نمی باشد')})
        
        communicative_road = {}
        # from now only support email (future: telegram)
        if self.json_body.get('email'):
            communicative_road = {
                'email': self.json_body['email']
            }

        Contact.create_contact(first_name=self.json_body['first_name'], last_name=self.json_body['last_name'], 
                               user=request.user, phone=self.json_body['phone'], tags=self.json_body['tags'], 
                               communicative_road=communicative_road)
        
        return SuccessJsonResponse({})


class GetContact(PremissionMixin, DataTableView):
    result_args = ('id', 'tags',)
    result_kwargs = {'firstName': F('first_name'), 
                     'lastName': F('last_name'), 
                     'created': F('created_at'),
                     'contactInfo': F('communicative_road')}

    search_on = ('last_name', )

    def post(self, request, *args, **kwargs):
        self.queryset = Contact.get_by_user(request.user)
        return super().post(request, *args, **kwargs)


class RemoveContact(PremissionMixin, View):
    http_method_names = ['post']

    def post(self, request, contact_id: str, *args, **kwargs):
        contact_id = contact_id.strip()
        user_contact = Contact.get_by_user(request.user)
        user_contact.filter(id=contact_id).update(is_deleted=True)
        return SuccessJsonResponse()


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


class CreateInviteCard(PremissionMixin, JsonValidatorMixin, View):
    http_method_names = ['post']
    json_body_schema = create_invite_card
    
    def post(self, request:HttpRequest, *args, **kwargs):
        template = Template.by_id(self.json_body['template'])
        
        if not template:
            return BadJsonResponse({'message': 'قالب یافت نشد'})

        self.json_body['sendDateTime'] = datetime.fromtimestamp(int(self.json_body['sendDateTime'][:10]))
        
        if self.json_body['tagBase']:
            Invitation.create_invitation(request.user, template, 
                                         self.json_body['templateInfoPanel'], self.json_body['isScheduler'], 
                                         tags=self.json_body['contactOrTag'], send_at=self.json_body['sendDateTime'])
        else:
            Invitation.create_invitation(request.user, template, 
                                         self.json_body['templateInfoPanel'], self.json_body['isScheduler'], 
                                         contacts=self.json_body['contactOrTag'], send_at=self.json_body['sendDateTime'])

        return SuccessJsonResponse()


class GetInvititon(PremissionMixin, DataTableView):
    result_args = ('id', 'title')
    result_kwargs = {'cardCount': F('card_count'),
                     'sendAt': F('send_at')}

    search_on = ('title', )

    def post(self, request, *args, **kwargs):
        start_date = request.POST.get('startDate')
        # end_date = request.POST.get('endDate')

        self.queryset = Invitation.get_by_user(request.user)
        if start_date and start_date.strip():
            start_date = format_date(start_date)
            self.queryset = self.queryset.filter(send_at__gte=start_date)

        # if end_date and end_date.strip():
        #     end_date = format_date(end_date)
        #     self.queryset.filter(send_at__lte=end_date)

        self.queryset = self.queryset.annotate(card_count=Count('cards'))
        return super().post(request, *args, **kwargs)
