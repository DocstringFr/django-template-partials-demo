from django.shortcuts import render
from django.http import HttpResponse
import random
from .models import Like


def index(request):
    """Vue principale avec template partials et HTMX."""

    like, _ = Like.objects.get_or_create(id=1)

    cart = request.session.get("cart") or {}

    # Produits pour affichage avec quantité présente dans le panier
    products_view = []
    for p in PRODUCTS:
        products_view.append({
            **p,
            "qty": cart.get(str(p["id"]), 0),
        })

    context = {
        'like_count': like.count,
        'is_online': False,
        'status_text': 'Hors ligne',
        'status_color': 'bg-red-500',
        'status_icon': '🔴',
        'products': products_view,
        'cart_count': sum(cart.values()) if cart else 0,
    }

    return render(request, 'demo/index.html', context=context)
    

def update_content(request):
    """Vue qui retourne seulement un partial mis à jour."""

    quotes = [
        "Abonne-toi à la chaîne.",
        "Certifie tes compétences avec notre programme TOSA.",
        "Teste tes connaissances avec nos tests de compétences.",
        "Finance ta certification TOSA avec le CPF.",
    ]
    
    colors = ['bg-blue-100', 'bg-green-100', 'bg-yellow-100', 'bg-pink-100', 'bg-purple-100']
    
    context = {
        'quote': random.choice(quotes),
        'color': random.choice(colors),
        'timestamp': __import__('datetime').datetime.now().strftime('%H:%M:%S')
    }
    
    # Utilisation de template partials avec le nom du fragment
    return render(request, 'demo/index.html#dynamic-content', context)


def like_counter(request):
    """Vue qui retourne seulement un partial mis à jour."""

    like, _ = Like.objects.get_or_create(id=1)
    like.count += 1
    like.save()

    context = {
        'like_count': like.count
    }

    return render(request, 'demo/index.html#like-counter', context=context)


def online_status(request):
    """Vue qui retourne le statut en ligne/hors ligne avec simulation aléatoire."""

    is_online = random.random() < 0.3
    
    context = {
        'is_online': is_online,
        'status_text': 'En ligne' if is_online else 'Hors ligne',
        'status_color': 'bg-green-500' if is_online else 'bg-red-500',
        'status_icon': '🟢' if is_online else '🔴'
    }
    
    return render(request, 'demo/index.html#online-status', context=context)


# Produits en mémoire pour la démo (id, nom, prix)
PRODUCTS = [
    {"id": 1, "name": "T-shirt Django", "price": 19.9},
    {"id": 2, "name": "Mug HTMX", "price": 12.5},
    {"id": 3, "name": "Sticker Tailwind", "price": 3.0},
    {"id": 4, "name": "Chaussettes Python", "price": 9.9},
]


def _get_cart(request):
    cart = request.session.get("cart")
    if cart is None:
        cart = {}
        request.session["cart"] = cart
    return cart


def _save_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True


def _get_cart_count(cart):
    return sum(cart.values()) if cart else 0


def _get_product(product_id):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None


def add_to_cart(request, product_id: int):
    """Ajoute un article au panier (session) et retourne le partial du badge.
    Inclut un élément OOB pour mettre à jour la quantité du produit."""
    cart = _get_cart(request)
    product = _get_product(product_id)
    if product is not None:
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        _save_cart(request, cart)
    context = {
        'cart_count': _get_cart_count(cart),
        'product_id': product_id,
        'product_qty': cart.get(str(product_id), 0),
    }
    return render(request, 'demo/index.html#cart-icon', context=context)


def remove_from_cart(request, product_id: int):
    """Retire un article du panier (session) et retourne le partial du badge.
    Inclut un élément OOB pour mettre à jour la quantité du produit."""
    cart = _get_cart(request)
    key = str(product_id)
    if key in cart:
        if cart[key] > 1:
            cart[key] -= 1
        else:
            del cart[key]
        _save_cart(request, cart)
    context = {
        'cart_count': _get_cart_count(cart),
        'product_id': product_id,
        'product_qty': cart.get(str(product_id), 0),
    }
    return render(request, 'demo/index.html#cart-icon', context=context)