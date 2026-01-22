from django.urls import path

from records.views import RecordCreateView, SuccessRecordsListView


urlpatterns = [
    path('records/', RecordCreateView.as_view(), name='record-create'),
    path('records/success/', SuccessRecordsListView.as_view(), name='records-success'),
]
