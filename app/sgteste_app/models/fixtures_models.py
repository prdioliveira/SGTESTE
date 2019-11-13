from django.db import models


class StatusProjeto(models.Model):
    class Meta:
        db_table = 'status'
        verbose_name = 'status'
        managed = True

    status = models.CharField(max_length=25)

    def __str__(self):
        return self.status