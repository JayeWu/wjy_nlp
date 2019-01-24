import os
import shutil
import traceback

import gevent
from scrapy import Request, Selector
import json
import logging
import random
import re
import time
import sqlalchemy
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 刮取看准网的结构化信息，并存入数据库

dir_kanzhun = 'D:\\rde\\data\\gs_html\\看准网'


DB_URL = 'mysql+pymysql://root:84411350@localhost:3306/enterprise?charset=utf8'

engine = create_engine(DB_URL, encoding='utf8', echo=False,  pool_pre_ping=True)

Base = declarative_base()

# 定义User对象:
class Company(Base):
    # 表的名字:
    __tablename__ = 'company'
    # 表的结构:
    id = Column('id', Integer, primary_key=True)
    co_abbre_name = Column(String(255), nullable=False, unique=True)
    co_type = Column(String(255))
    co_city = Column(String(255))
    co_addr = Column(String(255))
    period = Column(String(255))
    province = Column(String(255))
    co_CEO = Column(String(255))
    co_form = Column(String(255))
    co_found_time = Column(String(255))
    status = Column(String(255))
    full_name = Column(String(255))
    com_rep = Column(String(255))
    com_cap = Column(String(255))
    # co_info = Column(String(10000))
    website = Column(String(255))
    co_members = Column(String(255))
    scope_business = Column(String(10000))


# Base.metadata.create_all(engine)


def kanzhun_scraper():
    filelist = os.listdir(dir_kanzhun)

    for file in filelist:
        text = open(os.path.join(dir_kanzhun, file), 'r', encoding='utf8').read()
        sel = Selector(text=text)
        #  简称
        co_abbre_name = (sel.xpath('//div[@class="co_name t_center"]/text()').extract_first() or
                         ''.join(re.findall('(?<=【).*(?=】)', file)) or "unknown").strip()
        co_abbre_name = "" if re.match('(暂无|--)', co_abbre_name) else co_abbre_name

        #  行业
        co_type = (sel.xpath('//div[@class="co_base"]/span[@class="type"]/text()').extract_first() or "").strip()
        co_type = "" if re.match('(暂无|--)', co_type) else co_type
        #  员工数
        co_members = (sel.xpath('//div[@class="co_base"]/span[@class="members"]/text()').extract_first() or "").strip()
        co_members = "" if re.match('(暂无|--)', co_members) else co_members
        #  成立时间
        co_found_time = (sel.xpath('//div[@class="co_base_info"]/em[1]/text()').extract_first() or "").strip()
        co_found_time = ''.join(re.findall('(?<=成立时间).*', co_found_time)).strip()
        co_found_time = "" if re.match('(暂无|--)', co_found_time) else co_found_time
        #  公司地址
        co_addr = (sel.xpath('//div[@class="co_addr"]/text()').extract_first() or "").strip()
        co_addr = co_addr.replace('公司地址', '')
        # 总部城市
        co_city = (sel.xpath('//div[@class="co_base_info"]/em[2]/text()').extract_first() or "").strip()
        co_city = "" if re.match('(暂无|--|CEO.*)', co_city) else co_city
        # CEO
        co_CEO = (sel.xpath('//div[@class="co_base_info"]/em[3]/text()').extract_first() or "").strip()
        co_CEO = ''.join(re.findall('(?<=CEO).*', co_CEO)).strip()
        co_CEO = "" if re.match('(暂无|--)', co_CEO) else co_CEO
        # 网址
        website = (sel.xpath('//div[@class="website"]/span/text()').extract_first() or "").strip()
        website = "" if re.match('(暂无|--)', website) else website
        #  工商信息---
        commerce = sel.xpath('//div[@class="commerce"]')
        #  注册资金
        com_cap = (commerce.xpath(
            './div[@class="profile"]/p[@class="tit"]/span[@class="com_cap"]/em/text()').extract_first() or "").strip()
        com_cap = "" if re.match('(暂无|--)', com_cap) else com_cap
        #  法人代表
        com_rep = (commerce.xpath(
            './div[@class="profile"]/p[@class="tit"]/span[3]/em/text()').extract_first() or "").strip()
        com_rep = "" if re.match('(暂无|--)', com_rep) else com_rep

        commerce_cont_sel = commerce.xpath('./div[@class="commerce_cont"]/p')

        commerce_cont = ('\r\n'.join([''.join([x.strip() for x in s.xpath('./*/text()').extract()]) for s in
                                      commerce_cont_sel]) if commerce_cont_sel else "").strip()
        #  全称
        full_name = ''.join(re.findall('(?<=公司全称:).*', commerce_cont)).strip()
        full_name = "" if re.match('(暂无|--)', full_name) else full_name
        #  企业类型
        co_form = ''.join(re.findall('(?<=企业类型:).*', commerce_cont)).strip()
        co_form = "" if re.match('(暂无|--)', co_form) else co_form

        #  经营状态
        status = ''.join(re.findall('(?<=经营状态:).*', commerce_cont)).strip()
        status = "" if re.match('(暂无|--)', status) else status

        #  总部省份
        province = ''.join(re.findall('(?<=总部城市:).*', commerce_cont)).strip()
        province = "" if re.match('(暂无|--)', province) else province

        #  经营期限
        period = ''.join(re.findall('(?<=经营期限:).*', commerce_cont)).strip()
        period = "" if re.match('(暂无|--)', period) else period

        # #  注册地址
        # co_addr1 = ''.join(re.findall('(?<=注册地址:).*', commerce_cont)).strip()
        # co_addr1 = "" if re.match('(暂无|--)', co_addr) else co_addr


        #  经营范围
        scope_business = ''.join(re.findall('(?<=经营范围:).*', commerce_cont)).strip()
        scope_business = "" if re.match('(暂无|--)', scope_business) else scope_business

        paras = sel.xpath('//div[@class="co_info"]/text()').extract()
        paras = [x.strip() for x in paras]
        #  公司简介
        co_info = '\r\n'.join(paras)
        # print(com_rep)
        print(full_name)
        # print('\n')
        # print(
        #     (co_abbre_name, co_city, co_addr, period, province, co_CEO, co_form, co_found_time, status, full_name,
        #      com_rep,
        #      com_cap, co_info)
        # )

        # new_comp = Company()
        # new_comp.website = website
        # new_comp.co_found_time = co_found_time
        # new_comp.co_abbre_name = co_abbre_name
        # new_comp.co_city = co_city
        # new_comp.co_addr = co_addr
        # new_comp.period = period
        # new_comp.province = province
        # new_comp.co_CEO = co_CEO
        # new_comp.co_form = co_form
        # new_comp.status = status
        # new_comp.full_name = full_name
        # new_comp.com_rep = com_rep
        # new_comp.com_cap = com_cap
        # new_comp.co_info = co_info
        # new_comp.co_type = co_type
        # new_comp.co_members = co_members
        # new_comp.scope_business = scope_business
        # try:
        #     Session = sessionmaker(bind=engine)
        #     sess = Session()
        #     comp = sess.query(Company).filter_by(co_abbre_name=co_abbre_name).first()
        #     print(comp)
        #     print("-----------")
        #     if comp:
        #         comp.co_type = co_type
        #         comp.co_city = co_city
        #         sess.commit()
        #     else:
        #         sess.add(new_comp)
        #         sess.commit()
        # except Exception as e:
        #     traceback.print_exc()





# kanzhun_scraper()
