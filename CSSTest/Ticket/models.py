from django.db import models
from django.conf import settings

status = (("Pending","pending"),("Closed","closed"))

class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null = True)
    content = models.CharField(max_length= 1024, null = True)
    status = models.CharField(choices=status,max_length=155, default="Pending")
    noted = models.CharField(max_length= 1024, null = True)
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

    class Meta:
        ordering = ["-created"]