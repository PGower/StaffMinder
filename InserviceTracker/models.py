from django.db import models


class InserviceStandard(models.Model):
    number = models.IntegerField(unique=True,
                                 help_text='A unique number that identifies this inservice standard.')
    label = models.CharField(max_length=255,
                             help_text='A short description of this inservice standard.')
    description = models.TextField(blank=True, null=True,
                                   help_text='An optional description for this inservice standard.')

    class Meta:
        ordering = ['number']


class InserviceRecord(models.Model):
    date = models.DateField(help_text='The date the inservice occured.')
    duration = models.IntegerField(help_text='Duration in minutes of the inservice.')
    presenter = models.CharField(max_length=255, help_text='Name of the inservice presenter.')
    title = models.CharField(max_length=255, help_text='Title of the inservice.')
    description = models.TextField(blank=True, null=True, help_text='Optional description of the inservice.')
    venue = models.TextField(blank=True, null=True, help_text='Optional venue that the inservice occured.')
    standards = models.ManyToManyField('InserviceStandard', related_name='records')
    staff_member = models.ForeignKey('StaffInformation.StaffMember', related_name='inservice_records')

    class Meta:
        ordering = ['date']
