from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class Merchandise(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=100)
    pinyin = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(_('brand'), max_length=50, null=True, blank=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2, default=0.00)
    old_price = models.DecimalField(_('old_price'), max_digits=9, decimal_places=2, blank=True, default=0.00)
    is_active = models.BooleanField(_('is_active'), default=False)
    is_bestseller = models.BooleanField(_('is_bestseller'), default=False)
    description = models.TextField(_('description'), blank=True, null=True)
    meta_keywords = models.CharField(_('meta keywords'), max_length=255, help_text=_('Comma-delimited set of SEO keywords for meta tag'), blank=True, null=True)
    meta_description = models.CharField(_('meta description'), max_length=255, help_text=_('Content for description meta tag'), blank=True, null=True)
    manufacturer = models.CharField(_('manufacturer'), max_length=300, blank=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)
    # owner = models.ForeignKey(User, related_name = 'merchandises')
    owner = models.ForeignKey(User, related_name = 'merchandises', on_delete=models.CASCADE)
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Merchandise, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)
    def __str__(self):
        return self.name

class MerchandisePicture(models.Model):
    merchandise = models.ForeignKey(Merchandise, related_name = _('belong_to_merchandise'), blank=False, null=False)
    name = models.CharField(_('name'), unique=True, max_length=100)
    pinyin = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(_('image'), upload_to='merchandise_photo', blank=True)
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    class Meta:
        ordering = ('created_at',)
    def __str__(self):
        return self.name

class Express(models.Model):
    code = models.CharField(_('code'), unique=True, max_length=100)
    name = models.CharField(_('name'), unique=True, max_length=100)
    pinyin = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(_('is_active'), default=False)
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    class Meta:
        ordering = ('created_at',)
    def __str__(self):
        return self.name
PAYMENT_CHOICES = (('hdfk', _('hdfk')),('zfb', _('zhifubao')),('wx', _('weixin')),)

STATUS_CHOICES = (
    ('0', _('xiadan')),
    ('-1', _('chedan')),
    ('1', _('yifahuo')),
    ('2', _('yishouhuo')),
    ('3', _('yijiesuan')),)

class Order(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    merchandise = models.ForeignKey(Merchandise, related_name = _('order_merchandise'), blank=False, null=False)
    amount = models.PositiveSmallIntegerField(_('amount'), null=False, default=1)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2, default=0.00)
    payment = models.CharField(_('payment'), choices=PAYMENT_CHOICES, default='', max_length=50)
    buyer = models.CharField(_('buyer'), max_length=100, blank=False, null=False, default='zhangsan')
    cell_phone = models.CharField(_('cell_phone'), max_length=15, null=True, blank=True )
    state = models.CharField(_('state'), max_length=50, blank=True, default='')
    city = models.CharField(_('city'), max_length=50, blank=True, default='')
    region = models.CharField(_('region'), max_length=50, blank=True, default='')
    address = models.CharField(_('address'), max_length=300, blank=False, default='')
    comment = models.CharField(_('comment'), max_length=300, blank=True, default='')
    status = models.CharField(_('status'), choices=STATUS_CHOICES, default='', max_length=5)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    express = models.ForeignKey(Express, related_name = _('express_company'), blank=True, null=True)
    express_no = models.CharField(_('express_no'), default='', max_length=50, blank=True, null=True)
    express_info = models.TextField(_('express_info'), blank=True, null=True)

    class Meta:
        ordering = ('created_at',)

class Location(models.Model):
    country_region_code = models.CharField(_('country_region_code'), max_length=10)
    country_region_name = models.CharField(_('country_region_name'), max_length=30)
    country_region_py_code = models.CharField(_('country_region_py_code'), max_length=30, null=True, blank=True )
    country_region_quanpin = models.CharField(_('country_region_quanpin'), max_length=200, null=True, blank=True)
    state_code = models.CharField(_('state_code'), max_length=10, null=True, blank=True)
    state_name = models.CharField(_('state_name'), max_length=30, null=True, blank=True)
    state_py_code = models.CharField(_('state_py_code'), max_length=100, null=True, blank=True)
    state_quanpin = models.CharField(_('state_quanpin'), max_length=200, null=True, blank=True)
    city_code = models.CharField(_('city_code'), max_length=10, null=True, blank=True)
    city_name = models.CharField(_('city_name'), max_length=30, null=True, blank=True)
    city_py_code = models.CharField(_('city_py_code'), max_length=100, null=True, blank=True)
    city_quanpin = models.CharField(_('city_quanpin'), max_length=200, null=True, blank=True)
    region_code = models.CharField(_('region_code'), max_length=10, null=True, blank=True)
    region_name = models.CharField(_('region_name'), max_length=30, null=True, blank=True)
    region_py_code = models.CharField(_('region_py_code'), max_length=100, null=True, blank=True)
    region_quanpin = models.CharField(_('region_quanpin'), max_length=200, null=True, blank=True)
    longitude = models.FloatField(_('longitude'), null=True, blank=True)
    latitude = models.FloatField(_('latitude'), null=True, blank=True)
    detail_location = models.CharField(_('detail_location'), max_length=200, null=True, blank=True)
    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        index_together = ['country_region_code','state_code','city_code','region_code']
    def __str__(self):
        return self.country_region_name


class VisitLog(models.Model):
    from_ip = models.GenericIPAddressField(_('from_ip'))
    visit_url = models.URLField(_('visit_url'))
    user = models.ForeignKey(User, null=True)
    visit_date = models.DateTimeField(null=True)
    browser = models.CharField(_('browser'), max_length=64, null=True, blank=True)
    longitude = models.FloatField(_('longitude'), null=True, blank=True)
    latitude = models.FloatField(_('latitude'), null=True, blank=True)
    class Meta:
        verbose_name = _('TourLog')
        verbose_name_plural = _('TourLogs')
    def __str__(self):
        return self.user.username+self.location.country_region_name
