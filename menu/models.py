from django.db import models
from django.urls import reverse


class Menu(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Menu')

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    menu = models.ForeignKey(to=Menu,
                             on_delete=models.CASCADE,
                             related_name='items')
    parent = models.ForeignKey('self',
                               blank=True,
                               null=True,
                               related_name='children',
                               on_delete=models.CASCADE,
                               verbose_name='Parent')
    title = models.CharField(max_length=255,
                             verbose_name='Title')
    url = models.SlugField(unique=True,
                           verbose_name='URL')
    named_url = models.CharField(
        max_length=255,
        verbose_name='Named URL',
        blank=True,
        null=True,
        unique=True
    )

    def get_absolute_url(self):
        if self.named_url:
            return reverse('pages:page_by_named_url', args=(self.named_url,))
        else:
            return reverse('pages:page_by_url', args=(self.url,))

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.title
