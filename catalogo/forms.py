import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


# form de renovacao de livros
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Insira uma data entre agora e 4 semanas (padrão 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        # Verifique se a data não está no passado.
        if data < datetime.date.today():
            raise ValidationError(_('Data inválida - renovação no passado'))
        # Verifique se uma data está no intervalo permitido (+4 semanas a partir de hoje).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Data inválida - renovação com mais de 4 semanas de antecedência '))

        # Remember to always return the cleaned data.
        return data


from catalogo.models import Livro


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.keys():
            self.fields[f].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Livro
        fields = [
            'titulo',
            'autor',
            'resumo',
            'isbn',
            'genero'
        ]


from catalogo.models import Autor

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
        initial = {'date_of_death': '11/06/2020'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.keys():
            # adicionada classes css em cada campo do form
            self.fields[f].widget.attrs.update({'class': 'form-control'})

