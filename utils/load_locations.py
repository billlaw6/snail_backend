# -*- encoding: utf-8 -*-
import pypinyin
import lxml.etree as etree
from pypinyin import lazy_pinyin
from order_manage.models import Location

def load_locations():
    """非业务操作，用于载入QQ上下载的全国城市字典表"""
    tree = etree.ElementTree(file="/root/projects/snail_backend/utils/China.xml")
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




