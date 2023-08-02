from django.urls import re_path
from homepage.views import reg_user, users_login
from django.conf.urls.static import static
from django.conf import settings

app_name = 'regandlogin'
urlpatterns = [
    re_path(r'^register', reg_user, name='reg_user'),
    re_path(r'^userlogin', users_login, name='login_user')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)