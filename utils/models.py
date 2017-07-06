from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Country(models.Model):
    country_code = models.CharField(
        _('country_code'), max_length=10)
    country_name = models.CharField(
        _('country_name'), max_length=30)
    country_py_code = models.CharField(
        _('country_py_code'),
        max_length=30, null=False, default='', blank=True)
    country_quanpin = models.CharField(
        _('country_quanpin'),
        max_length=200, null=False, default='', blank=True)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        index_together = ['country_py_code', 'country_name']

    def __str__(self):
        return self.country_name


class Province(models.Model):
    country = models.ForeignKey(Country, null=False)
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

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')
        index_together = ['province_py_code', 'province_name']

    def __str__(self):
        return self.province_name


class City(models.Model):
    province = models.ForeignKey(Province, null=False)
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

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        index_together = ['city_py_code', 'city_name']

    def __str__(self):
        return self.province.province_name + '|' + self.city_name


class District(models.Model):
    city = models.ForeignKey(City, null=False)
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
    longitude = models.FloatField(_('longitude'), null=False, default=0.0,
                                  blank=True)
    latitude = models.FloatField(_('latitude'), null=False, default=0.0,
                                 blank=True)
    detail_location = models.CharField(
        _('detail_location'),
        max_length=200, null=False, default='', blank=True)

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')
        index_together = ['district_py_code', 'district_name']

    def __str__(self):
        return self.city.city_name + '|' + self.district_name
