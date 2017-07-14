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
                    createVar['dt' + str(district.id)] = etree.SubElement(createVar['cti' + str(city.id)], 'District')
                    createVar['dt' + str(district.id)].set('Name', district.district_name)
                    createVar['dt' + str(district.id)].set('Code', district.district_code)
                    createVar['dt' + str(district.id)].set('PY_Code', district.district_py_code)
                    createVar['dt' + str(district.id)].set('QuanPin', district.district_quanpin)
                    createVar['dt' + str(district.id)].set('Lon', str(district.longitude))
                    createVar['dt' + str(district.id)].set('Lat', str(district.latitude))
    tree = etree.ElementTree(root)
    tree.write('China_custom.xml', pretty_print=True, xml_declaration=True,
               encoding='utf-8')


def load_locations():
    """非业务操作，用于载入QQ上下载的全国城市字典表"""
    p_dir = os.path.dirname(os.path.abspath(__file__))
    tree = etree.ElementTree(file=os.path.join(p_dir, "China.xml"))
    root = tree.getroot()
    count = 0
    crs = root.findall('CountryRegion')

    # 遍历国家节点
    for cr in crs:
        # 在国家节点中检索全部州省子节点
        sts = cr.findall('State')
        # 如果当前国家节点没有州省子节点，直接输出和存储当前国家节点信息
        if len(sts) == 0:
            count = count + 1
            # print("%s: %s, %s, %s, %s" % (cr.tag, cr.get('Name'), lazy_pinyin(cr.get('Name')), lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER), cr.get('Code')))
            # 存储节点信息
            location = Location.objects.create( \
                country_region_code = cr.get('Code'),\
                country_region_name = cr.get('Name'),\
                country_region_py_code = ''.join(lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER)),\
                country_region_quanpin = ''.join(lazy_pinyin(cr.get('Name')))\
            )
            location.save()
        # 如果当前国家节点有州省子节点，继续判断州省子节点情况
        else:
            for st in sts:
                # 在州省子节点中检索全部城市子节点
                cts = st.findall('City')
                # 如果当前州省节点没有城市子节点，直接输出和存储当前州省节点信息
                if len(cts) == 0:
                    count = count + 1
                    # print("%s: %s, %s, %s: %s, %s" % (cr.tag, cr.get('Name'), cr.get('Code'), st.tag, st.get('Name'), st.get('Code')))
                    # 处理州省节点Name和Code为空的情况
                    state_name = st.get('Name')
                    if state_name != None:
                        state_py_code = ''.join(lazy_pinyin(st.get('Name'), style=pypinyin.FIRST_LETTER))
                        state_quanpin = ''.join(lazy_pinyin(st.get('Name')))
                    else:
                        state_py_code = ''
                        state_quanpin = ''
                    # 存储节点信息
                    location = Location.objects.create( \
                        country_region_code = cr.get('Code'),\
                        country_region_name = cr.get('Name'),\
                        country_region_py_code = ''.join(lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER)),\
                        country_region_quanpin = ''.join(lazy_pinyin(cr.get('Name'))),\
                        state_code = st.get('Code'),\
                        state_name = st.get('Name'),\
                        state_py_code = state_py_code,\
                        state_quanpin = state_quanpin\
                    )
                    location.save()
                # 如果当前州省节点有城市子节点，继续判断城市子节点情况
                else:
                    for ct in cts:
                        # 在城市节点中检索全部区县子节点
                        rgs = ct.findall('Region')
                        # 如果当前城市节点没有区县子节点，直接输出和存储当前城市节点信息
                        if len(rgs) == 0:
                            count = count + 1
                            # print("%s: %s, %s, %s, %s, %s: %s, %s, %s: %s, %s" % (cr.tag, cr.get('Name'), ''.join(lazy_pinyin(cr.get('Name'))), ''.join(lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER)), cr.get('Code'), st.tag, st.get('Name'), st.get('Code'), ct.tag, ct.get('Name'), ct.get('Code')))
                            state_name = st.get('Name')
                            if state_name != None:
                                state_py_code = ''.join(lazy_pinyin(st.get('Name'), style=pypinyin.FIRST_LETTER))
                                state_quanpin = ''.join(lazy_pinyin(st.get('Name')))
                            else:
                                state_py_code = ''
                                state_quanpin = ''
                            city_name = ct.get('Name')
                            if city_name != None:
                                city_py_code = ''.join(lazy_pinyin(ct.get('Name'), style=pypinyin.FIRST_LETTER))
                                city_quanpin = ''.join(lazy_pinyin(ct.get('Name')))
                            else:
                                city_py_code = ''
                                city_quanpin = ''
                            location = Location.objects.create( \
                                country_region_code = cr.get('Code'),\
                                country_region_name = cr.get('Name'),\
                                country_region_py_code = ''.join(lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER)),\
                                country_region_quanpin = ''.join(lazy_pinyin(cr.get('Name'))),\
                                state_code = st.get('Code'),\
                                state_name = st.get('Name'),\
                                state_py_code = state_py_code,\
                                state_quanpin = state_quanpin,\
                                city_code = ct.get('Code'),\
                                city_name = ct.get('Name'),\
                                city_py_code = city_py_code,\
                                city_quanpin = city_quanpin\
                            )
                            location.save()
                            # print("%s items found" % count)
                        else:
                            for rg in rgs:
                                count = count + 1
                                # print("%s: %s, %s, %s, %s, %s: %s, %s, %s: %s, %s, %s: %s, %s" % (cr.tag, cr.get('Name'), ''.join(lazy_pinyin(cr.get('Name'))), ''.join(lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER)), cr.get('Code'), st.tag, st.get('Name'), st.get('Code'), ct.tag, ct.get('Name'), ct.get('Code'), rg.tag, rg.get('Name'), rg.get('Code')))
                                state_name = st.get('Name')
                                if state_name != None:
                                    state_py_code = ''.join(lazy_pinyin(st.get('Name'), style=pypinyin.FIRST_LETTER))
                                    state_quanpin = ''.join(lazy_pinyin(st.get('Name')))
                                else:
                                    state_py_code = ''
                                    state_quanpin = ''
                                city_name = ct.get('Name')
                                if city_name != None:
                                    city_py_code = ''.join(lazy_pinyin(ct.get('Name'), style=pypinyin.FIRST_LETTER))
                                    city_quanpin = ''.join(lazy_pinyin(ct.get('Name')))
                                else:
                                    city_py_code = ''
                                    city_quanpin = ''
                                region_name = rg.get('Name')
                                if region_name != None:
                                    region_py_code = ''.join(lazy_pinyin(rg.get('Name'), style=pypinyin.FIRST_LETTER))
                                    region_quanpin = ''.join(lazy_pinyin(rg.get('Name')))
                                else:
                                    region_py_code = ''
                                    region_quanpin = ''
                                location = Location.objects.create( \
                                    country_region_code = cr.get('Code'),\
                                    country_region_name = cr.get('Name'),\
                                    country_region_py_code = ''.join(lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER)),\
                                    country_region_quanpin = ''.join(lazy_pinyin(cr.get('Name'))),
                                    state_code = st.get('Code'),\
                                    state_name = st.get('Name'),\
                                    state_py_code = state_py_code,\
                                    state_quanpin = state_quanpin,\
                                    city_code = ct.get('Code'),\
                                    city_name = ct.get('Name'),\
                                    city_py_code = city_py_code,\
                                    city_quanpin = city_quanpin,\
                                    region_code = rg.get('Code'),\
                                    region_name = rg.get('Name'),\
                                    region_py_code = region_py_code,\
                                    region_quanpin = region_quanpin
                                )
                                location.save()
                                # print("%s items found" % count)

def load_all_locations():
    """非业务操作，用于载入QQ上下载的全国城市字典表"""
    p_dir = os.path.dirname(os.path.abspath(__file__))
    tree = etree.ElementTree(file=os.path.join(p_dir, "China_all.xml"))
    root = tree.getroot()
    count = 0
    crs = root.findall('CountryRegion')

    # 遍历国家节点
    for cr in crs:
        # 在国家节点中检索全部州省子节点
        sts = cr.findall('Province')
        # 如果当前国家节点没有州省子节点，直接输出和存储当前国家节点信息
        if len(sts) == 0:
            count = count + 1
            # print("%s: %s, %s, %s, %s" % (cr.tag, cr.get('Name'), lazy_pinyin(cr.get('Name')), lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER), cr.get('Code')))
            # 存储节点信息
            location = AllLocation.objects.create( \
                country_region_code = cr.get('Code'),\
                country_region_name = cr.get('Name'),\
                longitude = cr.get('Lon'),\
                latitude = cr.get('Lat'),\
                country_region_py_code = ''.join(lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER)),\
                country_region_quanpin = ''.join(lazy_pinyin(cr.get('Name')))\
            )
            location.save()
        # 如果当前国家节点有州省子节点，继续判断州省子节点情况
        else:
            for st in sts:
                # 在州省子节点中检索全部城市子节点
                cts = st.findall('City')
                # 如果当前州省节点没有城市子节点，直接输出和存储当前州省节点信息
                if len(cts) == 0:
                    count = count + 1
                    # print("%s: %s, %s, %s: %s, %s" % (cr.tag, cr.get('Name'), cr.get('Code'), st.tag, st.get('Name'), st.get('Code')))
                    # 处理州省节点Name和Code为空的情况
                    state_name = st.get('Name')
                    if state_name != None:
                        state_py_code = ''.join(lazy_pinyin(st.get('Name'), style=pypinyin.FIRST_LETTER))
                        state_quanpin = ''.join(lazy_pinyin(st.get('Name')))
                    else:
                        state_py_code = ''
                        state_quanpin = ''
                    # 存储节点信息
                    location = AllLocation.objects.create( \
                        country_region_code = cr.get('Code'),\
                        country_region_name = cr.get('Name'),\
                        country_region_py_code = ''.join(lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER)),\
                        country_region_quanpin = ''.join(lazy_pinyin(cr.get('Name'))),\
                        state_code = st.get('Code'),\
                        state_name = st.get('Name'),\
                        state_py_code = state_py_code,\
                        state_quanpin = state_quanpin\
                    )
                    location.save()
                # 如果当前州省节点有城市子节点，继续判断城市子节点情况
                else:
                    for ct in cts:
                        # 在城市节点中检索全部区县子节点
                        rgs = ct.findall('Region')
                        # 如果当前城市节点没有区县子节点，直接输出和存储当前城市节点信息
                        if len(rgs) == 0:
                            count = count + 1
                            # print("%s: %s, %s, %s, %s, %s: %s, %s, %s: %s, %s" % (cr.tag, cr.get('Name'), ''.join(lazy_pinyin(cr.get('Name'))), ''.join(lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER)), cr.get('Code'), st.tag, st.get('Name'), st.get('Code'), ct.tag, ct.get('Name'), ct.get('Code')))
                            state_name = st.get('Name')
                            if state_name != None:
                                state_py_code = ''.join(lazy_pinyin(st.get('Name'), style=pypinyin.FIRST_LETTER))
                                state_quanpin = ''.join(lazy_pinyin(st.get('Name')))
                            else:
                                state_py_code = ''
                                state_quanpin = ''
                            city_name = ct.get('Name')
                            if city_name != None:
                                city_py_code = ''.join(lazy_pinyin(ct.get('Name'), style=pypinyin.FIRST_LETTER))
                                city_quanpin = ''.join(lazy_pinyin(ct.get('Name')))
                            else:
                                city_py_code = ''
                                city_quanpin = ''
                            location = AllLocation.objects.create( \
                                country_region_code = cr.get('Code'),\
                                country_region_name = cr.get('Name'),\
                                country_region_py_code = ''.join(lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER)),\
                                country_region_quanpin = ''.join(lazy_pinyin(cr.get('Name'))),\
                                state_code = st.get('Code'),\
                                state_name = st.get('Name'),\
                                state_py_code = state_py_code,\
                                state_quanpin = state_quanpin,\
                                city_code = ct.get('Code'),\
                                city_name = ct.get('Name'),\
                                city_py_code = city_py_code,\
                                city_quanpin = city_quanpin\
                            )
                            location.save()
                            # print("%s items found" % count)
                        else:
                            for rg in rgs:
                                count = count + 1
                                # print("%s: %s, %s, %s, %s, %s: %s, %s, %s: %s, %s, %s: %s, %s" % (cr.tag, cr.get('Name'), ''.join(lazy_pinyin(cr.get('Name'))), ''.join(lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER)), cr.get('Code'), st.tag, st.get('Name'), st.get('Code'), ct.tag, ct.get('Name'), ct.get('Code'), rg.tag, rg.get('Name'), rg.get('Code')))
                                state_name = st.get('Name')
                                if state_name != None:
                                    state_py_code = ''.join(lazy_pinyin(st.get('Name'), style=pypinyin.FIRST_LETTER))
                                    state_quanpin = ''.join(lazy_pinyin(st.get('Name')))
                                else:
                                    state_py_code = ''
                                    state_quanpin = ''
                                city_name = ct.get('Name')
                                if city_name != None:
                                    city_py_code = ''.join(lazy_pinyin(ct.get('Name'), style=pypinyin.FIRST_LETTER))
                                    city_quanpin = ''.join(lazy_pinyin(ct.get('Name')))
                                else:
                                    city_py_code = ''
                                    city_quanpin = ''
                                region_name = rg.get('Name')
                                if region_name != None:
                                    region_py_code = ''.join(lazy_pinyin(rg.get('Name'), style=pypinyin.FIRST_LETTER))
                                    region_quanpin = ''.join(lazy_pinyin(rg.get('Name')))
                                else:
                                    region_py_code = ''
                                    region_quanpin = ''
                                location = AllLocation.objects.create( \
                                    country_region_code = cr.get('Code'),\
                                    country_region_name = cr.get('Name'),\
                                    country_region_py_code = ''.join(lazy_pinyin(cr.get('Name'), style=pypinyin.FIRST_LETTER)),\
                                    country_region_quanpin = ''.join(lazy_pinyin(cr.get('Name'))),
                                    state_code = st.get('Code'),\
                                    state_name = st.get('Name'),\
                                    state_py_code = state_py_code,\
                                    state_quanpin = state_quanpin,\
                                    city_code = ct.get('Code'),\
                                    city_name = ct.get('Name'),\
                                    city_py_code = city_py_code,\
                                    city_quanpin = city_quanpin,\
                                    region_code = rg.get('Code'),\
                                    region_name = rg.get('Name'),\
                                    region_py_code = region_py_code,\
                                    region_quanpin = region_quanpin
                                )
                                location.save()
                                # print("%s items found" % count)



