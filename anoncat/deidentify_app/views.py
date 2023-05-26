from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

from .forms import DeidentifyForm
from .models import DeidentifiedText
import os
from medcat.cat import CAT
from medcat.utils.ner import deid_text


cat = CAT.load_model_pack(settings.DEID_MODEL) # Load a model

# Create your views here.
def deidentify(request):
    if request.method == 'POST' and request.is_ajax():
        form = DeidentifyForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text']
            redact = form.cleaned_data['redact']
            
            # Deidentify the input_text here using the MedCAT deid method
            output_text = deid_text(cat, input_text, redact=redact)
            
            # Return the processed output as JSON response
            return JsonResponse({'output_text': output_text})
        else:
            # Return form errors as JSON response
            return JsonResponse({'error': form.errors})
    else:
        form = DeidentifyForm()
    
    return render(request, 'frontend/deidentify_demo.html', {'form': form})


"""
def old_deidentify(request):
    if request.method == 'POST':
        form = DeidentifyForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text']
            redact = form.cleaned_data['redact']

            # Deidentify the input_text here using the MedCAT deid method
            output_text = deid_text(cat, input_text, redact=redact)

            deidentified_text = DeidentifiedText.objects.create(
                input_text=input_text,
                output_text=output_text
            )
            return render(request, 'deidentify_demo.html', {'form': form, 'output_text': output_text})
    else:
        form = DeidentifyForm()
        return render(request, 'deidentify_demo.html', {'form': form})

"""

