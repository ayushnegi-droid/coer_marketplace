from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

CATEGORY_CHOICES = [
    ('Books', 'Books'),
    ('Electronics', 'Electronics'),
    ('Furniture', 'Furniture'),
    ('Clothing', 'Clothing'),
    ('Sports', 'Sports'),
    ('Stationery', 'Stationery'),
    ('Other', 'Other'),
]


class Listing(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
    ]

    seller      = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='listings')
    title       = models.CharField(max_length=200)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    category    = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image1      = models.ImageField(upload_to='listings/')
    image2      = models.ImageField(upload_to='listings/')
    image3      = models.ImageField(upload_to='listings/')
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_new(self):
        # Mark as new if listed within last 6 hours
        return (timezone.now() - self.created_at).total_seconds() < 21600


class Wishlist(models.Model):
    user    = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='wishlisted_by')
    added   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')

    def __str__(self):
        return f'{self.user.email} → {self.listing.title}'
