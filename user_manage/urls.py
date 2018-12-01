
from django.conf.urls import url, include
import views

urlpatterns = [

    url(r'^signup$', views.SignUpView.as_view(),'signup'),
]
