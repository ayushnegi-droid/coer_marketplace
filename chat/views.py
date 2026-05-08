from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from .models import Message
from marketplace.models import Listing
from accounts.models import CustomUser


@login_required
def chat_view(request, listing_id, buyer_id=None):
    listing = get_object_or_404(Listing, pk=listing_id)
    seller  = listing.seller

    # If the seller is opening the chat, get the buyer from URL or first message
    if request.user == seller:
        if buyer_id:
            buyer = get_object_or_404(CustomUser, pk=buyer_id)
        else:
            # Try to get buyer from existing messages
            first_msg = Message.objects.filter(
                listing=listing
            ).exclude(sender=seller).first()
            if first_msg:
                buyer = first_msg.sender
            else:
                django_messages.error(request, "No messages yet for this listing.")
                return redirect('dashboard')
    else:
        # Current user is the buyer
        buyer = request.user

    # Get full conversation between buyer and seller
    chat_messages = Message.objects.filter(
        listing=listing,
        sender__in=[buyer, seller],
        receiver__in=[buyer, seller]
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            # Figure out who is sending and who is receiving
            if request.user == seller:
                receiver = buyer
            else:
                receiver = seller
            Message.objects.create(
                listing=listing,
                sender=request.user,
                receiver=receiver,
                content=content,
            )
        # Redirect correctly based on who is chatting
        if request.user == seller:
            return redirect('chat_with_buyer', listing_id=listing_id, buyer_id=buyer.pk)
        return redirect('chat', listing_id=listing_id)

    return render(request, 'chat/chat.html', {
        'listing':  listing,
        'seller':   seller,
        'messages': chat_messages,
    })