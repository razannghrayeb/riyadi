from django import forms
from .models import Game

class GameAdminForm(forms.ModelForm):
    thumbnail_upload = forms.ImageField(required=False, label='Upload Thumbnail')

    class Meta:
        model = Game
        fields = '__all__'

    def save(self, commit=True):
        game = super(GameAdminForm, self).save(commit=False)
        if self.cleaned_data.get('thumbnail_upload'):
            game.set_thumbnail_file(self.cleaned_data['thumbnail_upload'])

        if commit:
            game.save()
            self.save_m2m()

        return game
