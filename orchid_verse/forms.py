from django import forms
from .models import (
    OrchidPurchase, 
    OrchidEvent, 
    CultivatedOrchid
)


class OrchidPurchaseForm(forms.ModelForm):
    class Meta:
        model = OrchidPurchase
        fields = ['seller', 'purchase_date',
                   'order_number', 'actual_total_price', 
                   'receipt_photo', 'purchase_notes'
                   ]
        widgets = {
            'seller': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleziona il venditore',
            }),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'order_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numero ordine o codice interno',
            }),
            'actual_total_price': forms.NumberInput(attrs={'step': '0.01'}),
            'receipt_photo': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
            }),
            'purchase_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': "Note aggiuntive sull'acquisto, condizioni, dettagli…",
            })
        }


class OrchidEventForm(forms.ModelForm):
    class Meta:
        model = OrchidEvent
        fields = ['orchid', 'photo', 'date', 
                  'event_type', 'description']
        widgets = {
            'orchid': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleziona la pianta',
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrivi l’evento: fioritura, rinvaso, problema, ecc.',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['orchid'].queryset = CultivatedOrchid.objects.order_by('nickname','species__genus')
