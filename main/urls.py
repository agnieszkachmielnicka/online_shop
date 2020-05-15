from django.urls import path
from django.conf.urls import url

from main import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^categories/$', views.categories, name="categories"),
    url(r'^categories/(?P<category_name>[-\w]+)/$', views.single_category, name="single_category"),
    url(r'^basket/$', views.basket, name="basket"),
    url(r'^add_product_to_basket/(?P<product_id>\d+)/$', views.add_product_to_basket, name='add_product_to_basket'),
    url(r'^remove_product_from_basket/(?P<product_id>\d+)/$', views.remove_product_from_basket, name='remove_product_from_basket'),
    url(r'^order', views.order, name='order'),
    url(r'^history', views.history, name='history')
]
