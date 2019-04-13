from django.urls import path

from .views import (
	runPOST,
)

app_name = 'docker'

urlpatterns = [
	path('runPOST/', runPOST, name = 'runPOST'),
]
