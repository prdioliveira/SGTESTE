from django import forms
from app.sgteste_app.models.projeto_models import Projeto
from datetime import datetime, timedelta
from app.sgteste_app.functions.planejamento_diario_utils import create_planning
from app.sgteste_app.models.diario_models import Diario


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'
        exclude = ['status_projeto']


class ProjetoEditForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'
        exclude = ['status_projeto']

    def save(self, commit=True):
        projeto = super(ProjetoEditForm, self).save(commit=False)
        if projeto.cts_adicionais == 0:
            diario = Diario.objects.filter(projeto_id=projeto.id)
            diario.delete()

        if commit:
            projeto.save()
        return projeto