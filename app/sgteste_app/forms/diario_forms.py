from django import forms
from app.sgteste_app.models.diario_models import Diario


class DiarioForm(forms.ModelForm):
    disabled_fields = ('data_execucao', 'cts_previstos',)

    class Meta:
        model = Diario
        fields = '__all__'
        exclude = ['projeto']

    def __init__(self, *args, **kwargs):
        super(DiarioForm, self).__init__(*args, **kwargs)
        for field in self.disabled_fields:
            self.fields[field].disabled = True


class AddInDiarioForm(forms.ModelForm):
    disabled_fields = ('projeto')

    class Meta:
        model = Diario
        fields = '__all__'
        exclude = [
            'cts_executados',
            'bugs_encontrados',
            'cts_cancelados',
            'observacao',
            'data_execucao'
        ]

        def __init__(self, *args, **kwargs):
            super(DiarioForm, self).__init__(*args, **kwargs)
            for field in self.disabled_fields:
                self.fields[field].disabled = True