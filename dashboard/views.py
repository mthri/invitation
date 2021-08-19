from django.http.response import Http404, HttpResponse
from dashboard import send_invition
from payment.models import Invoice
import uuid

from django.http.request import HttpRequest
from dashboard.models import InvitationCard, Template, Tag, Contact as ContactModel
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from .mixins import PremissionMixin
from .forms import UserForm
from utils.upload import save_uploaded_file
from utils.config import CSV_DIRECTORY_PATH, CONFIG
from utils.email import render_to_string


@login_required
def index(request):
    return render(request, 'dashboard/base.html')


def show_invite_card(request, card_id):
    invite_card = InvitationCard.objects.select_related('contact', 'invitation__template')\
                                        .filter(id=card_id)

    if not invite_card.exclude():
        raise Http404
    else:
        invite_card = invite_card.first()

    template_file = open(invite_card.invitation.template.path.path, 'r').read()

    context = {
        **invite_card.invitation.informations,
        'first_name': invite_card.contact.first_name,
        'last_name': invite_card.contact.last_name
    }
    content = render_to_string(template_file, context=context)
    return HttpResponse(content)


class Profile(PremissionMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/profile.html',
                      context={'user': request.user})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()

        return render(request, 'dashboard/profile.html',
                      context={'user': request.user,
                               'errors': form.errors.get_json_data()})


class Contact(PremissionMixin, View):

    def get(self, request, *arg, **kwargs):
        return render(request, 'dashboard/contact_manage.html', context={'csv_sample': 'upload/upload/csv/sample.csv'})

    def post(self, request: HttpRequest, *args, **kwargs):
        path = CONFIG['FILE_UPLOAD_TEMP_DIR'] + '/' + \
            CSV_DIRECTORY_PATH + str(uuid.uuid4())
        save_uploaded_file(path=path, file=request.FILES['file'])

        tags = [int(tag) for tag in request.POST.getlist('tags')]

        tags = Tag.validate_tags(request.user, tags)
        contact_list = []
        with open(path, 'r', encoding="utf8") as f:
            # skip first row
            lines = f.readlines()[1:]
            for line in lines:
                cols = line.split(',')
                first_name = cols[0]
                last_name = cols[1]
                phone = cols[2]
                email = cols[3]
                contact_list.append(ContactModel(
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    tags=tags,
                    owner=request.user,
                    communicative_road={'email': email}
                ))

        ContactModel.objects.bulk_create(contact_list)

        return render(request, 'dashboard/contact_manage.html')


class Setting(PremissionMixin, View):

    def get(self, request, *arg, **kwargs):
        return render(request, 'dashboard/setting.html')


class Invite(PremissionMixin, View):

    def get(self, request, *args, **kwargs):
        content = {
            'tempaltes': Template.objects.all(),
            'SMS_COST': CONFIG['SMS_COST']
        }
        return render(request, 'dashboard/invite.html', context=content)


class InviteHistory(PremissionMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/invite_list.html')


class Purchase(PremissionMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/purchase.html')


class Transactions(PremissionMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/transactions.html',
                      context={'choices': Invoice.StatusChoices.choices})
