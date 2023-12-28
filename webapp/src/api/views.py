from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from .models import Item, Order, Tax, Discount
from django.http.response import JsonResponse
from decimal import Decimal
import stripe
import json
import os


class SuccessView(TemplateView):
    template_name = "api/success.html"


class CancelView(TemplateView):
    template_name = "api/cancel.html"


class HomePageView(ListView):
    model = Item
    template_name = 'api/home.html'
    context_object_name = 'items'
    # sorting
    ordering = ['id']

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(HomePageView, self).get_context_data(**kwargs)
        ctx['title'] = 'Home page'
        return ctx


class ItemView(DetailView):
    model = Item
    template_name = 'api/item.html'
    context_object_name = 'item'


def calculate_discount(item_price, discout_name=None):
    """
    Calculating discounts for items and orders, its work from calculate_price function
    def calculate_price(item_price, tax_name=None):
        '''
            return calculate_discount(item_price)

        tax_rate = Decimal(tax.rate) / 100
        total_price = calculate_discount(item_price) * (1 + tax_rate)
        '''
    :param item_price
    :param discount_name
    :return: total_price or item_price (if discount == 0 )
    """
    try:
        if discout_name:
            discount = Discount.objects.get(name=discout_name)
        else:
            discount = Discount.objects.last()
    except Exception as e:
        print(str(e))
        return item_price
    discount_rate = Decimal(discount.rate) / 100
    total_price = item_price * (1 - discount_rate)
    return total_price


def calculate_price(item_price, tax_name=None):
    """
    Calculating taxes and discounts for items and orders
    'unit_amount': int(calculate_tax(item.price) * 100),
    :param item_price
    :param tax_name
    :return: total_price or item_price (if taxes == 0 )
    """
    try:
        if tax_name:
            tax = Tax.objects.get(name=tax_name)
        else:
            tax = Tax.objects.last()
    except Exception as e:
        print(str(e))
        return calculate_discount(item_price)
    tax_rate = Decimal(tax.rate) / 100
    total_price = calculate_discount(item_price) * (1 + tax_rate)
    return total_price


@csrf_exempt
def create_checkout_session(request, id):
    """
        This function creates a Stripe checkout session for a selected item.

        Parameters:
        - request: Django request object.
        - id: The id of the item for which the checkout session is being created.

        Returns:
        - JsonResponse: A JsonResponse object containing the session id or an error message.

        Process:
        1. Retrieves the item by its id.
        2. Sets up the domain and Stripe settings.
        3. Attempts to create a Stripe checkout session with the item data and tax.
        4. Returns a JsonResponse with the session id on success or an error message on failure.
        """
    if request.method == 'GET':
        item = Item.objects.get(pk=id)

        # _______________DOMAIN settings_______________
        # locally testing
        domain_url = 'http://127.0.0.1:8000/'
        # domain_url = settings.DOMAIN_URL

        # _______________STRIPE settings_______________

        stripe.api_key = str(os.getenv('STRIPE_SECRET_KEY'))
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success/',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': int(calculate_price(item.price) * 100),
                    },
                    'quantity': 1,
                }],
            )

            return JsonResponse({'sessionId': checkout_session['id']})

        except Exception as e:
            return JsonResponse({'error': str(e)})


class OrderView(TemplateView):
    template_name = 'api/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.all()
        return context


@csrf_exempt
def create_order_checkout_session(request):
    """
        This function creates a Stripe checkout session for an order.

        Parameters:
        - request: Django request object.

        Returns:
        - JsonResponse: A JsonResponse object containing the session id or an error message.

        Process:
        1. Checks if the request method is POST.
        2. Sets up the domain settings.
        3. Parses the request body to get the items for the order.
        4. Creates a new order and adds the items to it.
        5. Prepares the line items for the Stripe checkout session, including calculating the tax for each item.
        6. Sets up the Stripe settings.
        7. Attempts to create a Stripe checkout session with the line items.
        8. Returns a JsonResponse with the session id on success or an error message on failure.
        """
    if request.method == 'POST':
        # _______________DOMAIN settings_______________
        # locally testing
        domain_url = 'http://127.0.0.1:8000/'
        # domain_url = settings.DOMAIN_URL

        data = json.loads(request.body)
        order = Order.objects.create()
        for item_id in data['items']:
            numeric_id = item_id.split('item')[1]
            order.items.add(Item.objects.get(id=int(numeric_id)))

        line_items = []

        for item in order.items.all():
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': int(calculate_price(item.price) * 100),
                },
                'quantity': 1,
            })

        # _______________STRIPE settings_______________
        stripe.api_key = str(os.getenv('STRIPE_SECRET_KEY'))
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success/',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items,
            )

            return JsonResponse({'sessionId': checkout_session['id']})

        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': os.getenv('STRIPE_PUBLISHABLE_KEY')}
        return JsonResponse(stripe_config, safe=False)
