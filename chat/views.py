from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from .models import Message
from marketplace.models import Listing


@login_required
def chat_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    seller  = listing.seller
    buyer   = request.user

    # Prevent seller from chatting with themselves
    if buyer == seller:
        django_messages.error(request, "You can't chat about your own listing.")
        return redirect('detail', pk=listing_id)

    # Get full conversation between buyer and seller about this listing
    messages = Message.objects.filter(
        listing=listing
    ).filter(
        sender__in=[buyer, seller]
    ).filter(
        receiver__in=[buyer, seller]
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                listing=listing,
                sender=buyer,
                receiver=seller,
                content=content,
            )
        return redirect('chat', listing_id=listing_id)

    return render(request, 'chat/chat.html', {
        'listing':  listing,
        'seller':   seller,
        'messages': messages,
    })
