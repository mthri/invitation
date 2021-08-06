from django.urls import path

from . import views, ajax_views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('setting/', views.Setting.as_view(), name='setting'),
    path('invite/', views.Invite.as_view(), name='invite'),
    path('invite/history/', views.InviteHistory.as_view(), name='invite_history'),
    path('purchase/', views.Purchase.as_view(), name='purchase'),
    path('transactions/', views.Transactions.as_view(), name='transactions'),
]

# AJAX url
urlpatterns += [
    path('ajax/tag/add', ajax_views.AddTag.as_view(), name='ajax_tag_add'),
    path('ajax/tag/get/all', ajax_views.GetTags.as_view(), name='ajax_tag_get_all'),
    path('ajax/tag/remove/<int:tag_id>', ajax_views.RemoveTag.as_view(), name='ajax_tag_remove'),
    path('ajax/contact/get/all', ajax_views.GetContact.as_view(), name='ajax_contact_get_all'),
    path('ajax/contact/remove/<str:contact_id>', ajax_views.RemoveContact.as_view(), name='ajax_contact_remove'),
    path('ajax/tag/get/all/select2', ajax_views.GetTagSelect2.as_view(), name='ajax_tag_get_all_select2'),
    path('ajax/user/get/all/select2', ajax_views.GetContactSelect2.as_view(), name='ajax_contact_get_all_select2'),
    path('ajax/invition/add', ajax_views.CreateInviteCard.as_view(), name='ajax_create_invition'),
]
