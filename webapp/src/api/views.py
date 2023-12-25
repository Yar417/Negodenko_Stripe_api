from django.shortcuts import render, redirect
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
import stripe

from .models import Item
from django.views.generic import ListView, DetailView


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class HomePageView(ListView):
    model = Item
    template_name = 'home.html'
    # 5. html context for jinja {{ news }}
    context_object_name = 'items'
    # 6.sort
    ordering = ['id']

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(HomePageView, self).get_context_data(**kwargs)
        ctx['title'] = 'Home page'
        return ctx


class ItemView(DetailView):
    model = Item
    template_name = 'item.html'
    context_object_name = 'item'


@csrf_exempt
def create_checkout_session(request, id):
    if request.method == 'GET':
        item = Item.objects.get(pk=id)
        # locally testing
        domain_url = 'http://127.0.0.1:8000/'

        # domain_url = settings.DOMAIN_URL

        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + '/success/',
                cancel_url=domain_url + '/cancel/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
                }],
            )

            return JsonResponse({'sessionId': checkout_session['id']})

        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
