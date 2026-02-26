from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Viloyat/Hudud nomi")
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hudud"
        verbose_name_plural = "Hududlar"
        ordering = ['name']
