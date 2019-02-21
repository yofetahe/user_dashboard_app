from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard_index/$', views.dashboard_index, name="dashboard_index"),
    url(r'^get_profile_edit_form/(?P<user_id>\d+)/$', views.get_profile_edit_form, name="get_profile_edit_form"),
    url(r'^get_message_page/(?P<user_id>\d+)/$', views.get_message_page, name="get_message_page"),
    url(r'^remove_user/(?P<user_id>\d+)/$', views.remove_user, name="remove_user"),
    url(r'^get_user_registation_form/$', views.get_user_registation_form, name="get_user_registation_form"),
    url(r'^register$', views.register, name="register"),    
    url(r'^udpate_information/(?P<user_id>\d+)/$', views.udpate_information, name="udpate_information"),
    url(r'^change_password/(?P<user_id>\d+)/$', views.change_password, name="change_password"),
    url(r'^edit_description/(?P<user_id>\d+)/$', views.edit_description, name="edit_description"),
    url(r'^save_post/(?P<user_id>\d+)/$', views.save_post, name="save_post"),
    url(r'^save_comment/(?P<msg_id>\d+)/$', views.save_comment, name="save_comment"),
]