from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

status = (("Pending","pending"),("In-progressed","in-progressed"),("Closed","closed"))

class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(max_length=50, choices=status, default='Pending')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.title, self.status)

    def save(self, *args, **kwargs):
        if not self.id:  # If id is not set, generate it based on the latest id in the database
            latest_ticket = Ticket.objects.order_by('-id').first()
            if latest_ticket:
                self.id = latest_ticket.id + 1
            else:
                self.id = 1

        super().save(*args, **kwargs)  # Call the real save() method

    def clean(self):
        if not self.title:
            raise ValidationError(_('Title cannot be null.'))
        if not self.content:
            raise ValidationError(_('Content cannot be null.'))
        if not self.user:
            raise ValidationError(_('User cannot be null.'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]