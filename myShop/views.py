from django.shortcuts import render

def thanks(request):
    return render(request, 'thanks_page.html', {})
