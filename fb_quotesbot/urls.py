from django.conf.urls import include, url
from .views import QuotesBotView
urlpatterns = [
    url(r'^b4829fda25bf02722794d4aac0da31155fb5c8f143963f29fd/?$', QuotesBotView.as_view())
]
