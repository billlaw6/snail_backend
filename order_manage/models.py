from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
# from pygments.lexers import get_lexer_by_name
# from pygments.formatters.html import HtmlFormatter
# from pygments import highlight


class Merchandise(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=100)
    pinyin = models.CharField(max_length=50, blank=True, null=False, default='')
    brand = models.CharField(_('brand'), max_length=50, null=False, default='', blank=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2,
                                default=0.00)
    old_price = models.DecimalField(_('old_price'), max_digits=9,
                                    decimal_places=2, blank=True, default=0.00)
    is_active = models.BooleanField(_('is_active'), default=False)
    sold_amount = models.PositiveIntegerField(_('sold_amount'), null=False,
                                              default=10000)
    is_bestseller = models.BooleanField(_('is_bestseller'), default=False)
    end_datetime = models.DateTimeField(_('end_datetime'), default=timezone.now)
    description = models.TextField(_('description'), blank=True, null=False, default='')
    meta_keywords = models.CharField(_('meta keywords'), max_length=255,
                                     help_text=_('Comma-delimited set of \
                                     SEO keywords for meta tag'), blank=True,
                                     null=False, default='')
    meta_description = models.CharField(_('meta description'), max_length=255,
                                        help_text=_('Content for description \
                                        meta tag'), blank=True, null=False, default='')
    manufacturer = models.CharField(_('manufacturer'), max_length=300,
                                    blank=True, default='')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated_at'), default=timezone.now)
    owner = models.ForeignKey(User, related_name='merchandises',
                              on_delete=models.CASCADE, blank=True, default='')
    highlighted = models.TextField()

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name


class SubMerchandise(models.Model):
    merchandise = models.ForeignKey(Merchandise,
                                    related_name=_('submerchandises'),
                                    blank=False, null=False,
                                    on_delete=models.CASCADE)
    name = models.CharField(_('name'), unique=True, max_length=100)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2,
                                default=0.00)
    image = models.ImageField(_('image'), upload_to='merchandise_photo',
                              blank=False, null=False)
    min_amount = models.PositiveSmallIntegerField(_('min_amount'), null=False,
                                              default=1)
    max_amount = models.PositiveSmallIntegerField(_('max_amount'), null=False,
                                              default=10)
    description = models.TextField(_('description'), blank=True,
                                   null=False, default='')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    class Meta:
        ordering = ('merchandise', 'name', )

    def __str__(self):
        return self.merchandise.name + '-' + self.name


class MerchandisePicture(models.Model):
    merchandise = models.ForeignKey(Merchandise, related_name=_('pictures'),
                                    blank=False, null=False,
                                    on_delete=models.CASCADE)
    name = models.CharField(_('name'), unique=True, max_length=100)
    pinyin = models.CharField(max_length=50, blank=True, null=False, default='')
    image = models.ImageField(_('image'), upload_to='merchandise_photo',
                              blank=False, null=False)
    order = models.PositiveSmallIntegerField(_('order'), null=False, default=1)
    description = models.TextField(_('description'), blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    class Meta:
        ordering = ('merchandise', 'order', )

    def __str__(self):
        return self.merchandise.name + '-' + self.name


class Express(models.Model):
    code = models.CharField(_('code'), unique=True, max_length=100)
    name = models.CharField(_('name'), unique=True, max_length=100)
    pinyin = models.CharField(max_length=50, blank=True, null=False, default='')
    is_active = models.BooleanField(_('is_active'), default=False)
    description = models.TextField(_('description'), blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name


class Payment(models.Model):
    code = models.CharField(_('code'), unique=True, max_length=100)
    name = models.CharField(_('name'), unique=True, max_length=100)
    pinyin = models.CharField(max_length=50, blank=True, null=False, default='')
    is_active = models.BooleanField(_('is_active'), default=False)
    description = models.TextField(_('description'), blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name


class OrderStatus(models.Model):
    code = models.CharField(_('code'), unique=True, max_length=100)
    name = models.CharField(_('name'), unique=True, max_length=100)
    pinyin = models.CharField(max_length=50, blank=True, null=False, default='')
    is_active = models.BooleanField(_('is_active'), default=False)
    description = models.TextField(_('description'), blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_no = models.CharField(max_length=50, unique=True, blank=True,
                             default='')
    sum_amount = models.PositiveSmallIntegerField(_('sum_amount'), null=False,
                                              default=0)
    sum_price = models.DecimalField(_('sum_price'), max_digits=9,
                                     decimal_places=2, blank=False,
                                     null=False, default=0.00)
    payment = models.ForeignKey(Payment, related_name=_('orders'),
                                to_field='code', blank=False, null=False)
    buyer = models.CharField(_('buyer'), max_length=100, blank=False,
                             null=False, default='zhangsan')
    cell_phone = models.CharField(_('cell_phone'), max_length=15, null=False,
                                  default='', blank=True)
    city = models.CharField(_('city'), max_length=200, blank=False, null=False)
    address = models.CharField(_('address'), max_length=300, blank=False,
                               default='')
    comment = models.CharField(_('comment'), max_length=300, blank=True,
                               default='')
    status = models.ForeignKey(OrderStatus, related_name=_('orders'),
                               default=1)
    express = models.ForeignKey(Express, related_name=_('orders'),
                                to_field='code', null=False, default='')
    express_no = models.CharField(_('express_no'), max_length=50,
                                  blank=True, null=False, default='')
    express_info = models.TextField(_('express_info'), blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), blank=True, default=timezone.now)

    class Meta:
        ordering = ('created_at',)
        index_together = ['order_no', 'created_at', 'express_no']
        unique_together = (('cell_phone', 'address', 'comment'))

    def __str__(self):
        return self.order_no + '-' + self.buyer + '-' + str(self.cell_phone)

    # def save(self, *args, **kwargs):
    #     """
    #     city字段array型数据单独处理
    #     """
    #     city = json.dumps(self.city)
    #     super(Order, self).save(*args, **kwargs)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name=_(
        'order_detail'), blank=False, null=False)
    submerchandise = models.ForeignKey(SubMerchandise, related_name=_(
        'order_details'), blank=False, null=False)
    name = models.CharField(_('name'), max_length=100)
    amount = models.PositiveSmallIntegerField(_('amount'), null=False,
                                              default=1)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2,
                                default=0.00)
    created_at = models.DateTimeField(_('created_at'), blank=True,
                                      default=timezone.now)


class Location(models.Model):
    country_region_code = models.CharField(
        _('country_region_code'), max_length=10)
    country_region_name = models.CharField(
        _('country_region_name'), max_length=30)
    country_region_py_code = models.CharField(
        _('country_region_py_code'),
        max_length=30, null=False, default='', blank=True)
    country_region_quanpin = models.CharField(
        _('country_region_quanpin'),
        max_length=200, null=False, default='', blank=True)
    state_code = models.CharField(
        _('state_code'),
        max_length=10,
        null=False, default='',
        blank=True)
    state_name = models.CharField(
        _('state_name'),
        max_length=30,
        null=False, default='',
        blank=True)
    state_py_code = models.CharField(
        _('state_py_code'),
        max_length=100, null=False, default='', blank=True)
    state_quanpin = models.CharField(
        _('state_quanpin'),
        max_length=200, null=False, default='', blank=True)
    city_code = models.CharField(
        _('city_code'),
        max_length=10,
        null=False, default='',
        blank=True)
    city_name = models.CharField(
        _('city_name'),
        max_length=30,
        null=False, default='',
        blank=True)
    city_py_code = models.CharField(
        _('city_py_code'),
        max_length=100, null=False, default='', blank=True)
    city_quanpin = models.CharField(
        _('city_quanpin'),
        max_length=200, null=False, default='', blank=True)
    region_code = models.CharField(
        _('region_code'),
        max_length=10, null=False, default='', blank=True)
    region_name = models.CharField(
        _('region_name'),
        max_length=30, null=False, default='', blank=True)
    region_py_code = models.CharField(
        _('region_py_code'),
        max_length=100, null=False, default='', blank=True)
    region_quanpin = models.CharField(
        _('region_quanpin'),
        max_length=200, null=False, default='', blank=True)
    longitude = models.FloatField(_('longitude'), null=False, default=0.0, blank=True)
    latitude = models.FloatField(_('latitude'), null=False, default=0.0, blank=True)
    detail_location = models.CharField(
        _('detail_location'),
        max_length=200, null=False, default='', blank=True)

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        index_together = [
            'country_region_code',
            'state_code',
            'city_code',
            'region_code']

    def __str__(self):
        return self.country_region_name + '|' + self.state_name + '|' + self.city_name + '|' + self.region_name


class AllLocation(models.Model):
    country_region_code = models.CharField(
        _('country_region_code'), max_length=10)
    country_region_name = models.CharField(
        _('country_region_name'), max_length=30)
    country_region_py_code = models.CharField(
        _('country_region_py_code'),
        max_length=30, null=False, default='', blank=True)
    country_region_quanpin = models.CharField(
        _('country_region_quanpin'),
        max_length=200, null=False, default='', blank=True)
    province_code = models.CharField(
        _('province_code'),
        max_length=10,
        null=False, default='',
        blank=True)
    province_name = models.CharField(
        _('province_name'),
        max_length=30,
        null=False, default='',
        blank=True)
    province_py_code = models.CharField(
        _('province_py_code'),
        max_length=100, null=False, default='', blank=True)
    province_quanpin = models.CharField(
        _('province_quanpin'),
        max_length=200, null=False, default='', blank=True)
    city_code = models.CharField(
        _('city_code'),
        max_length=10,
        null=False, default='',
        blank=True)
    city_name = models.CharField(
        _('city_name'),
        max_length=30,
        null=False, default='',
        blank=True)
    city_py_code = models.CharField(
        _('city_py_code'),
        max_length=100, null=False, default='', blank=True)
    city_quanpin = models.CharField(
        _('city_quanpin'),
        max_length=200, null=False, default='', blank=True)
    district_code = models.CharField(
        _('district_code'),
        max_length=10, null=False, default='', blank=True)
    district_name = models.CharField(
        _('district_name'),
        max_length=30, null=False, default='', blank=True)
    district_py_code = models.CharField(
        _('district_py_code'),
        max_length=100, null=False, default='', blank=True)
    district_quanpin = models.CharField(
        _('district_quanpin'),
        max_length=200, null=False, default='', blank=True)
    longitude = models.FloatField(_('longitude'), null=False, default=0.0, blank=True)
    latitude = models.FloatField(_('latitude'), null=False, default=0.0, blank=True)
    detail_location = models.CharField(
        _('detail_location'),
        max_length=200, null=False, default='', blank=True)

    class Meta:
        verbose_name = _('AllLocation')
        verbose_name_plural = _('AllLocations')
        index_together = [
            'country_region_name',
            'province_name',
            'city_name',
            'district_name']

    def __str__(self):
        return self.country_region_name + '|' + self.province_name + '|' + self.city_name + '|' + self.district_name


class VisitLog(models.Model):
    from_ip = models.GenericIPAddressField(_('from_ip'))
    visit_url = models.URLField(_('visit_url'))
    user = models.ForeignKey(User, null=False, default='')
    visit_date = models.DateTimeField(null=False, default='')
    browser = models.CharField(
        _('browser'),
        max_length=64,
        null=False, default='',
        blank=True)
    longitude = models.FloatField(_('longitude'), null=False, default=0, blank=True)
    latitude = models.FloatField(_('latitude'), null=False, default=0, blank=True)

    class Meta:
        ordering = ('visit_date', 'from_ip',)
        verbose_name = _('VisitLog')
        verbose_name_plural = _('VisitLogs')

    def __str__(self):
        return self.user.username + '-' + self.from_ip + '-' + self.visit_date


class Comment(models.Model):
    merchandise = models.ForeignKey(Merchandise, related_name=_('comments'),
                                    blank=False, null=False,
                                    on_delete=models.CASCADE)
    cell_phone = models.CharField(_('cell_phone'), max_length=15, null=False, default='',
                                  blank=True)
    author = models.CharField(_('author'), max_length=100)
    content = models.TextField(_('content'), blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.cell_phone + '-' + self.name + '-' + self.content
