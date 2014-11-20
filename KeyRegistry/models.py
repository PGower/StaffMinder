from django.db import models

KEY_TYPES = [(0, 'MK'), (1,'ST'), (2, 'Z')]

class DoorKey(models.Model):
    number = models.IntegerField()
    kind = models.CharField(max_length=255, choices=KEY_TYPES)
    last_sighted = models.DateField(blank=True, null=True)
    is_lost = models.BooleanField(default=False)
    owner = models.ForeignKey('StaffInformation.StaffMember', related_name='keys')

    class Meta:
        ordering = ['kind', 'number']
        unique_together = [('kind', 'number'), ('number', 'kind', 'owner')]
        verbose_name = 'Key'
        verbose_name_plural = 'Keys'
