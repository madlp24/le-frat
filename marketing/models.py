from django.db import models
from django.utils.translation import gettext_lazy as _


class NewsletterSubscriber(models.Model):
    """Someone who asked to hear from Le Frat.

    `source` tells apart the general footer sign-up from the merch waiting
    list, so the drop can be announced to the people who asked for it.
    """

    FOOTER = "footer"
    MERCH = "merch"
    SOURCE_CHOICES = [
        (FOOTER, _("Newsletter")),
        (MERCH, _("Merch waiting list")),
    ]

    email = models.EmailField(unique=True)
    source = models.CharField(
        max_length=20, choices=SOURCE_CHOICES, default=FOOTER
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email
