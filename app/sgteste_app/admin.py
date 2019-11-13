from django.contrib import admin

# Register your models here.
from app.sgteste_app.models import fixtures_models, projeto_models, diario_models

admin.register(fixtures_models)
admin.register(projeto_models)
admin.register(diario_models)