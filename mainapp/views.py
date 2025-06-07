from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView, ListView, DetailView
from .models import Pizza, Order, Cart
from Accounts.models import CustomUser
from django.contrib import messages
from django.http import JsonResponse
import json


class HomePage(ListView):
    model = Pizza
    context_object_name = 'pizza'
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            cart_total_items = Cart.objects.filter(user=user).count()
        else:
            cart_total_items = 0  # Default for unauthenticated users
        
        context["cart_total"] = cart_total_items  # Store total cart items count
        return context
    

def mycart(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    cart_items = Cart.objects.filter(user=user)

    total_amount = sum(item.get_total_price() for item in cart_items)  # Updated dynamically
    total_count = sum(item.quantity for item in cart_items)  # Updated dynamically

    return render(request, 'cart.html', {
        'cart': cart_items,
        'total_amount': total_amount,
        'total_count': total_count
    })

def update_cart(request, cart_id):
    """Updates the quantity of a cart item and recalculates total count and amount."""
    cart_item = get_object_or_404(Cart, id=cart_id)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            quantity = data.get("quantity")

            # Validate quantity
            if not isinstance(quantity, int) or quantity < 1:
                return JsonResponse({"error": "Invalid quantity"}, status=400)

            # Update quantity
            cart_item.quantity = quantity
            cart_item.save()

            # Recalculate totals
            cart_items = Cart.objects.filter(user=cart_item.user)
            total_amount = sum(item.pizza.price * item.quantity for item in cart_items)
            total_count = sum(item.quantity for item in cart_items)

            return JsonResponse({"total_amount": total_amount, "total_count": total_count})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def confirm_order(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    cart_items = Cart.objects.filter(user=user)

    if request.method == "POST":
        cart_items.delete()  # Clear cart after successful order
        messages.success(request, "Order placed successfully!")
        return redirect('home')  # Redirect to home page after order

    return redirect('checkout', user_id=user.id)


def checkout(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    cart_items = Cart.objects.filter(user=user)

    if not cart_items:
        messages.warning(request, "Your cart is empty!")
        return redirect('my_cart', user_id=user.id)

    total_amount = sum(item.get_total_price() for item in cart_items)

    # Example: Redirect to a checkout page
    return render(request, 'checkout.html', {
        'cart': cart_items,
        'total_amount': total_amount,
        'user': user
    })

class PizzaDetails(DetailView):
    model = Pizza
    context_object_name = 'pizza'
    template_name = 'pizza_view.html'

def add_cart(request, pizza_id, user_id):
    if request.method == 'POST':
        count = 1 
        pizza = get_object_or_404(Pizza, id=pizza_id)
        user = get_object_or_404(CustomUser, id=user_id)
        cart = Cart(pizza = pizza, user = user, quantity = count)
        cart.save()
        return redirect('home')

def confirm_order(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    cart_items = Cart.objects.filter(user=user)

    if request.method == "POST":
        cart_items.delete()  # Clear cart after successful order
        messages.success(request, "Order placed successfully!")
        return redirect('home')  # Redirect to home page after order

    return redirect('checkout', user_id=user.id)




def pizza_order(request, id, user_id):
    if request.method == 'POST':
        try:
            count = int(request.POST.get('count', 0))  # Convert to integer
            if count <= 0:
                return HttpResponseBadRequest("Invalid pizza count.")

            pizza = get_object_or_404(Pizza, id=id)
            user = get_object_or_404(CustomUser, id=user_id)

            order = Order(pizza=pizza, customer=user, count=count)
            order.save()  # The model's save method will handle `order_number` and `total`

            return redirect('home')

        except ValueError:
            return HttpResponseBadRequest("Invalid count format.")

    return HttpResponseBadRequest("Invalid request method.")

def view_orders(request, id):
    try:
        user = CustomUser.objects.get(id = id)
        orders = Order.objects.filter(customer = user)
    except Order.DoesNotExist:
        orders = False
    return render(request, 'orders.html' , {'orders' : orders})

def delete_cart(request,cart_id):
    if request.method == 'POST':
        cart = Cart.objects.get(id = cart_id)
        cart.delete()
        return redirect('my_cart',user_id = request.user.id)
    return render(request, 'cart.html')