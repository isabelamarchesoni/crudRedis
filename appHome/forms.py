from django import forms

class TaskForm(forms.Form):
    titulo = forms.CharField(max_length=100, required=True)
    descricao = forms.CharField(widget=forms.Textarea, required=True)
    status = forms.ChoiceField(choices=[('Pendente', 'Pendente'), ('Em Progresso', 'Em Progresso'), ('Concluída', 'Concluída')], required=True)