from django.db import models
from django.contrib.auth.models import User

status = (("Pending","pending"),("Closed","closed"))

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null = True)
    content = models.TextField()
    status = models.CharField(choices=status,max_length=155, default="pending")
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