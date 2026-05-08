from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Listing, Wishlist, CATEGORY_CHOICES
from .forms import ListingForm
from chat.models import Message
from accounts.models import CustomUser

CATEGORIES = [c[0] for c in CATEGORY_CHOICES]


@login_required
def home_view(request):
    listings  = Listing.objects.all().order_by('-created_at')
    category  = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    query     = request.GET.get('q', '')
    sort      = request.GET.get('sort', 'newest')

    if category:
        listings = listings.filter(category=category)
    if min_price:
        listings = listings.filter(price__gte=min_price)
    if max_price:
        listings = listings.filter(price__lte=max_price)
    if query:
        listings = listings.filter(title__icontains=query) | listings.filter(description__icontains=query)
    if sort == 'price_asc':
        listings = listings.order_by('price')
    elif sort == 'price_desc':
        listings = listings.order_by('-price')

    wishlist_ids = set(
        request.user.wishlist.values_list('listing_id', flat=True)
    )

    return render(request, 'marketplace/home.html', {
        'listings':     listings,
        'wishlist_ids': wishlist_ids,
        'categories':   CATEGORIES,
    })


@login_required
def sell_view(request):
    form = ListingForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        listing        = form.save(commit=False)
        listing.seller = request.user
        listing.save()
        messages.success(request, 'Listing posted successfully! 🎉')
        return redirect('home')
    return render(request, 'marketplace/sell.html', {
        'form':       form,
        'categories': CATEGORIES,
    })


@login_required
def detail_view(request, pk):
    listing     = get_object_or_404(Listing, pk=pk)
    in_wishlist = Wishlist.objects.filter(user=request.user, listing=listing).exists()
    return render(request, 'marketplace/detail.html', {
        'listing':     listing,
        'in_wishlist': in_wishlist,
    })


@login_required
def toggle_wishlist(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    listing      = get_object_or_404(Listing, pk=pk)
    obj, created = Wishlist.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        obj.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})


@login_required
def mark_sold(request, pk):
    listing        = get_object_or_404(Listing, pk=pk, seller=request.user)
    listing.status = 'sold'
    listing.save()
    messages.success(request, f'"{listing.title}" marked as sold!')
    return redirect('dashboard')


@login_required
def mark_available(request, pk):
    listing        = get_object_or_404(Listing, pk=pk, seller=request.user)
    listing.status = 'available'
    listing.save()
    messages.success(request, f'"{listing.title}" relisted as available!')
    return redirect('dashboard')


@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    listing.delete()
    messages.success(request, 'Listing deleted.')
    return redirect('dashboard')


@login_required
def dashboard_view(request):
    my_listings = Listing.objects.filter(seller=request.user).order_by('-created_at')
    wishlist    = Wishlist.objects.filter(user=request.user).select_related('listing')
    sold_count  = my_listings.filter(status='sold').count()

    # Items the user has SENT messages about (as buyer)
    contacted_ids      = Message.objects.filter(sender=request.user).values_list('listing_id', flat=True).distinct()
    contacted_listings = Listing.objects.filter(pk__in=contacted_ids)

    # Messages RECEIVED by this user (as seller)
    received = Message.objects.filter(
        receiver=request.user
    ).values('listing_id', 'sender_id').distinct()

    buyer_conversations = []
    seen = set()
    for msg in received:
        key = (msg['listing_id'], msg['sender_id'])
        if key not in seen:
            seen.add(key)
            listing = Listing.objects.filter(pk=msg['listing_id']).first()
            buyer   = CustomUser.objects.filter(pk=msg['sender_id']).first()
            if listing and buyer:
                buyer_conversations.append({
                    'listing': listing,
                    'buyer':   buyer,
                })

    return render(request, 'marketplace/dashboard.html', {
        'my_listings':          my_listings,
        'wishlist':             wishlist,
        'contacted_listings':   contacted_listings,
        'buyer_conversations':  buyer_conversations,
        'sold_count':           sold_count,
    })