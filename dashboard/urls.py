from django.urls import path

from . import views, ajax_views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('setting/', views.Setting.as_view(), name='setting')
]

# AJAX url
urlpatterns += [
    path('ajax/tag/add', ajax_views.AddTag.as_view(), name='ajax_tag_add'),
    path('ajax/tag/get/all', ajax_views.GetTags.as_view(), name='ajax_tag_get_all'),
    path('ajax/tag/remove/<int:tag_id>', ajax_views.RemoveTag.as_view(), name='ajax_tag_remove'),
    path('ajax/contact/get/all', ajax_views.GetContact.as_view(), name='ajax_contact_get_all'),
]
