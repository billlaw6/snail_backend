# -*- encoding: utf-8 -*-
import pypinyin
import lxml.etree as etree
import os
from pypinyin import lazy_pinyin
from utils.models import Country, Province, City, District


def load_districts():
    """非业务操作，用于将XML文件中的全国城市字典表导入数据库"""
    p_dir = os.path.dirname(os.path.abspath(__file__))
    tree = etree.ElementTree(file=os.path.join(p_dir, "China_all.xml"))
    root = tree.getroot()
    cts = root.findall('Country')

    # 遍历国家节点
    for ct in cts:
        # 存储节点信息
        country = Country.objects.create(
            country_name=ct.get('Name'),
            country_py_code=''.join(
                lazy_pinyin(
                    ct.get('Name'),
                    style=pypinyin.FIRST_LETTER)),
            country_quanpin=''.join(
                lazy_pinyin(
                    ct.get('Name'))))
        country.save()
        # 在国家节点中检索全部州省子节点
        pros = ct.findall('Province')
        # 如果当前国家节点没有州省子节点，直接输出和存储当前国家节点信息
        for pro in pros:
            # 存储节点信息
            province = Province.objects.create(
                country=country,
                province_name=pro.get('Name'),
                province_py_code=''.join(
                    lazy_pinyin(
                        pro.get('Name'),
                        style=pypinyin.FIRST_LETTER)),
                province_quanpin=''.join(
                    lazy_pinyin(
                        pro.get('Name'))))
            province.save()
            # 在州省子节点中检索全部城市子节点
            cts = pro.findall('City')
            for ct in cts:
                city = City.objects.create(
                    province=province,
                    city_name=ct.get('Name'),
                    city_py_code=''.join(
                        lazy_pinyin(
                            ct.get('Name'),
                            style=pypinyin.FIRST_LETTER)),
                    city_quanpin=''.join(
                        lazy_pinyin(
                            ct.get('Name'))))
                city.save()
                # 在城市节点中检索全部区县子节点
                dts = ct.findall('District')
                # 如果当前城市节点没有区县子节点，直接输出和存储当前城市节点信息
                for dt in dts:
                    district = District.objects.create(
                        city=city, district_name=dt.get('Name'),
                        longitude=dt.get('Lon'),
                        latitude=dt.get('Lat'),
                        district_py_code=''.join(
                            lazy_pinyin(
                                dt.get('Name'),
                                style=pypinyin.FIRST_LETTER)),
                        district_quanpin=''.join(lazy_pinyin(dt.get('Name'))))
                    district.save()

def write_xml():
    # 动态生成变量名
    createVar = locals()
    root = etree.Element('Location')
    countries = Country.objects.all()
    for country in countries:
        createVar['ct' + str(country.id)] = etree.SubElement(root, 'Country')
        createVar['ct' + str(country.id)].set('Name', country.country_name)
        createVar['ct' + str(country.id)].set('Code', country.country_code)
        createVar['ct' + str(country.id)].set('PY_Code', country.country_py_code)
        createVar['ct' + str(country.id)].set('QuanPin', country.country_quanpin)
        provinces = Province.objects.filter(country_id = country.id)
        for province in provinces:
            createVar['pro' + str(province.id)] = etree.SubElement(createVar['ct' + str(country.id)], 'Province')
            createVar['pro' + str(province.id)].set('Name', province.province_name)
            createVar['pro' + str(province.id)].set('Code', province.province_code)
            createVar['pro' + str(province.id)].set('PY_Code', province.province_py_code)
            createVar['pro' + str(province.id)].set('QuanPin', province.province_quanpin)
            cities = City.objects.filter(province_id=province.id)
            for city in cities:
                createVar['cti' + str(city.id)] = etree.SubElement(createVar['pro' + str(province.id)], 'City')
                createVar['cti' + str(city.id)].set('Name', city.city_name)
                createVar['cti' + str(city.id)].set('Code', city.city_code)
                createVar['cti' + str(city.id)].set('PY_Code', city.city_py_code)
                createVar['cti' + str(city.id)].set('QuanPin', city.city_quanpin)
                districts = District.objects.filter(city_id=city.id)
                for district in districts:
                    createVar['dt' + str(district.id)] = etree.SubElement(createVar['cti' + str(city.id)], 'district')
                    createVar['dt' + str(district.id)].set('Name', district.district_name)
                    createVar['dt' + str(district.id)].set('Code', district.district_code)
                    createVar['dt' + str(district.id)].set('PY_Code', district.district_py_code)
                    createVar['dt' + str(district.id)].set('QuanPin', district.district_quanpin)
                    createVar['dt' + str(district.id)].set('Lon', district.longitude)
                    createVar['dt' + str(district.id)].set('Lat', district.latitude)
    tree = etree.ElementTree(root)
    tree.write('China_custom.xml', pretty_print=True, xml_declaration=True,
               encoding='utf-8')
