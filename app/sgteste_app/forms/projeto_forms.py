from django import forms
from app.sgteste_app.models.projeto_models import Projeto


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'
        exclude = ['status_projeto']