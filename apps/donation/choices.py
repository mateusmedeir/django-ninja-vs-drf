from django.db import models


class DonationMethod(models.TextChoices):
    PIX = 'pix', 'Pix'
    CREDIT_CARD = 'credit_card', 'Credit card'
    BOLETO = 'boleto', 'Boleto'


class DonationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    CANCELED = 'canceled', 'Canceled'
