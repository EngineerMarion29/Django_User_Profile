from django.urls import re_path
from adminview.views import profile_admin
from adminview.views import user_profile_list
from adminview.views import bulk_upload_csv
from adminview.views import export_user_profiles_to_csv
from adminview.views import delete_user_profiles
from adminview.views import profile_details_def

app_name = 'admin_view'
urlpatterns = [
    re_path(r'^emp_users', profile_admin, name='users'),
    re_path(r'^emp_list', user_profile_list, name='list'),
    re_path(r'^delete', delete_user_profiles, name='deletee'),
    re_path(r'^viewprofile/(?P<profile_id>\d+)/$', profile_details_def, name='view_prof'),
    re_path(r'^b_upload', bulk_upload_csv, name='b_upload'),
    re_path(r'^export-user-profiles/', export_user_profiles_to_csv, name='export_user_profiles')
    #re_path(r'^resume/(?P<user_profile_id>\d+)/$', show_resume, name='show_resume')
]