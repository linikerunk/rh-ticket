from .models import JustificativaAusencia

from django import forms


class JustificativaAusenciaForm(forms.ModelForm):
    AUSENCIA = (
    ("Falta", "Falta"),
    ("Atraso", "Atraso"),
    ("Saída Antecipada", "Saida Antecipada"),
    ("Saída Intermediária", "Saída Intermediária"),
    )

    JUSTIFICATIVA_AUSENCIA = (
    ('Débido em Banco de HS', 'Débido em Banco de HS'),
    ('Descanso de Jornadas', 'Descanso de Jornadas'),
    ('Serviço Externo', 'Serviço Externo'),
    ('Viagem à Trabalho', 'Viagem à Trabalho'),
    ('Treinamento Externo', 'Treinamento Externo'),
    ('Folga TRE', 'Folga TRE'),
    )

    tipo_de_ausencia = forms.ChoiceField(required=True, choices=AUSENCIA)
    justificativa = forms.ChoiceField(required=True, choices=JUSTIFICATIVA_AUSENCIA)


    class Meta:
        model = JustificativaAusencia
        fields = ['data_inicio', 'data_fim', 'tipo_de_ausencia',
                  'justificativa', 'observacao', 'ticket']
        labels = {
            'data_inicio': 'Data início ausência : '
        }
    
    #  # this function will be used for the validation 
    # def clean(self): 
  
    #     # data from the form is fetched using super function 
    #     super(JustificativaAusenciaForm, self).clean() 
          
    #     # extract the username and text field from the data 
    #     data_inicio = self.cleaned_data.get('data_inicio') 
    #     data_fim = self.cleaned_data.get('data_fim') 


  
        # # conditions to be met for the username length 
        # if len(username) < 5: 
        #     self._errors['username'] = self.error_class([ 
        #         'Minimum 5 characters required']) 
        # if len(text) <10: 
        #     self._errors['text'] = self.error_class([ 
        #         'Post Should Contain a minimum of 10 characters']) 
  
        # # return any errors if found 
        # return self.cleaned_data 