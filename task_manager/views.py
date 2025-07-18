from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = 'homepage.html'

    def get(self, request, *args, **kwargs):
        # Для Rollbar
        try:
            a.hello()
        except Exception as e:
            import rollbar
            rollbar.report_exc_info(request=request)
        return super().get(request, *args, **kwargs)
