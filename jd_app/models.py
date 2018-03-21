#! /usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/3/17 上午2:52
import json
import arrow
from run import db
from sqlalchemy.orm import relationship
from common.service import Commons

db_base = db.Column


class BaseModel(Commons, object):
    """模型基类，为每个模型添加创建时间和更新时间"""
    now = Commons.now()

    def __init__(self):
        super(BaseModel, self).__init__()

    create_time = db.Column(db.DATETIME, default=now)
    update_time = db.Column(db.DATETIME, default=now, onupdate=now)


class JingFenClass(BaseModel, db.Model):
    """
    京粉类别
    """
    __tablename__ = "jingfen_class"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jd_uid = db.Column(db.String(512), unique=True, nullable=True)
    name = db.Column(db.String(512), unique=True, nullable=False)
    sub_name = db.Column(db.String(512), nullable=False, default='')
    url = db.Column(db.String(512), nullable=False, default='')
    pic_url = db.Column(db.String(512), nullable=False, default='')
    type = db.Column(db.Integer, unique=False, nullable=False, default=0)
    content_skus = db.Column(db.Text, nullable=True, default='')
    products = db.relationship('Product', backref='jingfenclass')  # 分类下的所有产品

    def __init__(self, name=None, jd_uid=None):
        self.create_time = self.now
        self.update_time = self.now
        self.name = name
        self.jd_uid = jd_uid

    def to_dict(self):
        """将对象转换为字典数据"""
        class_dict = {
            "class_id": self.id,
            "name": self.name,
            "sub_name": self.sub_name,
            "jd_uid": self.jd_uid,
            "url": self.url,
            "pic_url": self.pic_url,
            "type": self.type,
            "create_time": arrow.get(self.create_time).format(),
            "content_skus": json.loads(self.create_time)
        }
        return class_dict

        # def __repr__(self):
        #     return self.name


class Product(BaseModel, db.Model):
    """
    京粉产品
    """

    __tablename__ = "jingfen_products"
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, index=True)
    title = db.Column(db.Text, nullable=False, default='')
    sku = db.Column(db.String(512), nullable=True, unique=True, index=True)
    spu = db.Column(db.String(512), nullable=True, unique=True)
    price = db_base(db.Float, nullable=True, default=0)
    bonus_rate = db_base(db.Float, nullable=False, default=0)
    prize_amout = db_base(db.Float, nullable=False, default=0)
    image_url = db_base(db.Text, nullable=True)
    url = db_base(db.Text, nullable=True)
    link = db_base(db.Text, nullable=True)
    ticket_id = db_base(db.String(512), nullable=True)
    ticket_total_number = db_base(db.Integer, nullable=True, default=0)
    ticket_used_number = db_base(db.Integer, nullable=True, default=0)
    ticket_amount = db_base(db.Float, nullable=True, default=0)
    start_time = db_base(db.DateTime, default=Commons.now(), nullable=True)
    end_time = db_base(db.DateTime, default=Commons.now(), nullable=True)
    ticket_valid = db_base(db.Boolean, default=False)
    good_come = db_base(db.Integer, default=0)
    jingfen_class_id = db_base(db.Integer, db.ForeignKey('jingfen_class.id'))
    jingfen_class = relationship(
        'JingFenClass')  # jingfen_calss 映射到JingFenClass 这个对象

    def __init__(self,
                 jingfenclass_id,
                 title,
                 sku,
                 price,
                 bonus_rate,
                 prize_amount,
                 start_time=None,
                 end_time=None,
                 spu=None,
                 image_url=None,
                 url=None,
                 link=None,
                 ticket_id=None,
                 ticket_total_number=None,
                 ticket_used_number=None,
                 ticket_amount=None,
                 ticket_valid=None,
                 good_come=None):
        self.jingfen_class_id = jingfenclass_id
        self.title = title
        self.sku = sku
        self.price = price
        self.bonus_rate = bonus_rate
        self.prize_amout = prize_amount
        self.start_time = start_time if start_time else Commons.now()
        self.end_time = end_time if end_time else Commons.now()
        self.spu = spu
        self.image_url = image_url
        self.url = url
        self.link = link
        self.ticket_id = ticket_id
        self.ticket_total_number = ticket_total_number
        self.ticket_used_number = ticket_used_number
        self.ticket_amount = ticket_amount
        self.ticket_valid = ticket_valid
        self.good_come = good_come

        # pass

        # def __repr__(self):
        #     return self.title

        # def to_dict(self):
        #     product_dict = {
        #         "jd"
        #     }
