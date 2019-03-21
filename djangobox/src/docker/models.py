from django.db import models

import uuid

class SessionNum(models.Model):
	num = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
