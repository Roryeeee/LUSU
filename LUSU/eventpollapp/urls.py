from django.urls import path
from .views import EventCreateView, event_detail

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='create_event'),
    path('<uuid:event_id>/', event_detail, name='event_detail'),  # Use UUIDField not int
]
