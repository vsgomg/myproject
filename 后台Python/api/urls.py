
from django.conf.urls import url
from api.views import course
from api.views import auth
from api.views import shoppingcar

urlpatterns = [
    url(r'auth/$',auth.AuthView.as_view({'post':'login'})),
    url(r'courses/$',course.CoursesView.as_view({'get':'list','post':'create'})),
    url(r'courses/(?P<pk>\d+)/$',course.CoursesView.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
    url(r'shoppingcar/$',shoppingcar.ShoppingCarView.as_view({'post':'create','get':'list'}))
]