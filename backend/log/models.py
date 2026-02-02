from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view_product', 'View Product'),
        ('create_product', 'Create Product'),
        ('update_product', 'Update Product'),
        ('delete_product', 'Delete Product'),
        ('create_order', 'Create Order'),
        ('admin_action', 'Admin Action'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.JSONField(blank=True, null=True)  # For additional data
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
