# main_forum/views/about.py

from django.views.generic import TemplateView
from django.shortcuts import render

class AboutView(TemplateView):
    """
    This view is used to render the about page.
    """

    template_name = 'about.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = 'About'
        return context