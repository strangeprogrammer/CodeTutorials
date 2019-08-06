from django.urls import path

from .views import (
	renderTutorial,
)

app_name = 'tutorials'

urlpatterns = [
	path('<slug:tutorialname>/', renderTutorial), # Must be a slug instead of a string or a path to ensure clients can't call the template rendering mechanism on arbitrary files
]
