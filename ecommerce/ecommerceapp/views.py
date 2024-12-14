from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, 
    CreateView, 
    DetailView
)
from django.urls import reverse_lazy
from django.db.models import Q
from math import ceil
from ecommerceapp.models import Contact, Product, OrderUpdate, Orders
import base64
import json
import requests
import time
from django.conf import settings
import midtransclient
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import logging





class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        allProds = []
        catprods = Product.objects.values('category', 'id')
        cats = {item['category'] for item in catprods}
        
        for cat in cats:
            prod = Product.objects.filter(category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n/4) - (n//4))
            allProds.append([prod, range(1, nSlides), nSlides])
        
        context['allProds'] = allProds
        return context

class ContactView(CreateView):
    model = Contact
    template_name = 'contact.html'
    fields = ['name', 'email', 'desc', 'phone_number']
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        self.object = form.save()
        
        messages.success(self.request, 'We will get back to you soon...')
        
        return super().form_valid(form)

class ProductView(TemplateView):
    template_name = 'product.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ambil parameter dari request
        search_query = self.request.GET.get('search', '')
        category_filter = self.request.GET.get('category', '')
        sort_by = self.request.GET.get('sort', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')

        products = Product.objects.all()

        if search_query:
            products = products.filter(
                Q(product_name__icontains=search_query) | 
                Q(desc__icontains=search_query)
            )

        if category_filter:
            products = products.filter(category=category_filter)

        if min_price and max_price:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
                products = products.filter(price__range=(min_price, max_price))
            except ValueError:
                pass
        elif min_price:
            try:
                min_price = float(min_price)
                products = products.filter(price__gte=min_price)
            except ValueError:
                pass
        elif max_price:
            try:
                max_price = float(max_price)
                products = products.filter(price__lte=max_price)
            except ValueError:
                pass

        if sort_by == 'price_asc':
            products = products.order_by('price')
        elif sort_by == 'price_desc':
            products = products.order_by('-price')
        elif sort_by == 'newest':
            products = products.order_by('-id')

        allProds = []
        catprods = products.values('category', 'id')
        cats = {item['category'] for item in catprods}
        
        for cat in cats:
            prod = products.filter(category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n/4) - (n//4))
            allProds.append([prod, range(1, nSlides), nSlides])
        
        context['allProds'] = allProds
        
        context['categories'] = list(set(Product.objects.values_list('category', flat=True)))
        
        context['search_query'] = search_query
        context['selected_category'] = category_filter
        context['sort_by'] = sort_by
        context['min_price'] = min_price
        context['max_price'] = max_price

        return context

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class CheckoutView(LoginRequiredMixin, CreateView):
    model = Orders
    template_name = 'checkout.html'
    fields = ['items_json', 'name', 'amount', 'email', 'address1', 
            'address2', 'city', 'state', 'zip_code', 'phone']
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        try:
            print("Received POST request")
            print("Request headers:", request.headers)
            print("Request POST data:", request.POST)
            print("Is AJAX:", request.headers.get('X-Requested-With') == 'XMLHttpRequest')

            items_json = json.loads(request.POST.get('itemsJson', '{}'))
            item_details = []

            for key, item in items_json.items():
                qty, name, price, image = item
                item_details.append({
                    'id': key,
                    'price': int(price),
                    'quantity': qty,
                    'name': name
                })

            post_data = request.POST.copy()
            post_data['items_json'] = post_data.get('itemsJson', '')
            post_data['amount'] = post_data.get('amt', '')

            form = self.get_form_class()(post_data)
            
            print("Form validation:", form.is_valid())
            
            if form.is_valid():
                form.instance.user = request.user
                form.instance.oid = f"ORDER-{int(time.time())}"  # Generate unique order ID
                form.instance.paymentstatus = 'PENDING'

                # Simpan order
                order = form.save()
                
                print(f"Order created: {order.order_id}")
                print(f"Order amount: {order.amount}")

                update = OrderUpdate.objects.create(
                    order_id=order.order_id, 
                    update_desc="Order placed successfully"
                )

                try:
                    snap = midtransclient.Snap(
                        is_production=settings.MIDTRANS_IS_PRODUCTION,
                        server_key=settings.MIDTRANS_SERVER_KEY,
                        client_key=settings.MIDTRANS_CLIENT_KEY
                    )

                    param = {
                        "transaction_details": {
                            "order_id": str(order.oid),
                            "gross_amount": int(order.amount)
                        },
                        "credit_card": {
                            "secure": True
                        },
                        "customer_details": {
                            "first_name": order.name,
                            "email": order.email,
                            "phone": order.phone or "081234567890",
                            "billing_address": {
                                "first_name": order.name,
                                "address": order.address1,
                                "city": order.city,
                                "postal_code": order.zip_code,
                                "country_code": "IDN"
                            }
                        },
                        "item_details": item_details or [
                            {
                                "id": "item1",
                                "price": int(order.amount),
                                "quantity": 1,
                                "name": "Order Payment"
                            }
                        ],
                        "enabled_payments": [
                            'credit_card', 
                            'bca', 
                            'bni', 
                            'mandiri', 
                            'gopay', 
                            'shopeepay'
                        ]
                    }

                    print("Midtrans Payload:", param)

                    transaction = snap.create_transaction(param)
                    
                    print("Midtrans Transaction Token:", transaction.get('token'))

                    order.payment_token = transaction['token']
                    order.save()

                    return JsonResponse({
                        'status': 'success',
                        'midtrans_token': transaction['token'],
                        'order_id': order.oid
                    })

                except midtransclient.MidtransAPIError as midtrans_api_error:
                    print(f"Midtrans API Error: {midtrans_api_error}")
                    print(f"Error Response: {midtrans_api_error.raw_response}")
                    
                    order.delete()
                    
                    return JsonResponse({
                        'status': 'error', 
                        'message': f"Payment Gateway Error: {str(midtrans_api_error)}"
                    }, status=400)

                except Exception as e:
                    print(f"Unexpected Error: {e}")
                    return JsonResponse({
                        'status': 'error', 
                        'message': "Terjadi kesalahan tidak terduga"
                    }, status=500)

            else:
                print("Form Errors:", form.errors)
                return JsonResponse({
                    'status': 'error',
                    'errors': dict(form.errors)
                }, status=400)

        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            print(f"Unexpected Error: {e}")
            return JsonResponse({
                'status': 'error', 
                'message': "Terjadi kesalahan tidak terduga"
            }, status=500)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'detail-product.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'
    

class OrderSuccessView(TemplateView):
    template_name = 'order_success.html'


@csrf_exempt
def midtrans_payment_handler(request):
    try:
        notification_body = request.body.decode('utf-8')
        notification_dict = json.loads(notification_body)
        
        snap = midtransclient.Snap(
            is_production=settings.MIDTRANS_IS_PRODUCTION,
            server_key=settings.MIDTRANS_SERVER_KEY
        )
        
        status = snap.transaction.notification(notification_dict)
        
        order = Orders.objects.get(oid=status['order_id'])
        
        if status['transaction_status'] == 'capture':
            order.payment_status = 'PAID'
        elif status['transaction_status'] in ['deny', 'cancel', 'expire']:
            order.payment_status = 'FAILED'
        
        order.save()
        
        OrderUpdate.objects.create(
            order_id=order.order_id,
            update_desc=f"Payment status updated to {order.payment_status}"
        )
        
        return JsonResponse({'status': 'success'})
    
    except Exception as e:
        logger.error(f"Midtrans Callback Error: {e}")
        return JsonResponse({'status': 'error'}, status=400)
@csrf_exempt
def update_payment_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            status = data.get('status')

            order = Orders.objects.get(oid=order_id)
            order.payment_status = status
            order.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Payment status updated'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)