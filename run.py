#!/usr/bin/python
# coding: utf-8
from flask import Flask, jsonify
import decimal
import os
from sqlalchemy import create_engine
from flask import render_template
from jd_app.common.utils import format_app_num
from jd_app.config import DB_URI
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from jd_app.common.response_code import RET
from jd_app import config
from flask_session import Session

engine = create_engine(DB_URI)


def creat_app():
    app = Flask(__name__)
    app.config.from_object(config)
    return app


app = creat_app()
db = SQLAlchemy(app)


def manager():
    db.init_app(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    return manager.run()


@app.route("/")
def get_tuijian():
    with engine.connect() as con:
        re = con.execute(
            """
            select sku, title, price, bonus_rate, prize_amout, ticket_amount, case when bonus_rate and ticket_amount then bonus_rate*price+ticket_amount else 0 end as ab, case when bonus_rate then  bonus_rate * prize else 0 end as a, case when ticket_amount then ticket_amount else 0 end as b from jingfen_products where price < 200 order by ab desc;

            """
        )
        bid_list = [
            {"id": x[0], "title": x[1].decode('utf-8'), "price": format_app_num(x[2], f=0),
             "bonus_rate": format(format_app_num(x[3] * 100, f=0)),
             "prize_amout": format_app_num(x[4], f=2), "ticket_amount": format_app_num(x[5], f=0), "url": x[7],
             "image_url": x[6]} for x in re]
    return render_template("home.html", bid_list=bid_list)


@app.route("/1")
def hello_world():
    with engine.connect() as con:
        re = con.execute(
            """select sku, title, price, bonus_rate, prize_amout, ticket_amount , image_url, url
                from jingfen_products 
                where price < 100  and bonus_rate > 0.02 
                and ticket_amount
                order by bonus_rate desc;""")
        bid_list = [
            {"id": x[0], "title": x[1].decode('utf-8'), "price": format_app_num(x[2], f=0),
             "bonus_rate": format(format_app_num(x[3] * 100, f=0)),
             "prize_amout": format_app_num(x[4], f=2), "ticket_amount": format_app_num(x[5], f=0), "url": x[7],
             "image_url": x[6]} for x in re]

    return render_template("home.html", bid_list=bid_list)


@app.route("/2")
def get_home_filter_query():
    query_list = [
        {"name": "返利", "value": "bonus"},
        {"name": "优惠券", "value": "ticket_amount"},
        {"name": "佣金", "value": "prize_amount"}
    ]
    return jsonify(error=RET.OK, data={"data": query_list})


@app.route("/3")
def get_bid_by_prize_amout():
    with engine.connect() as con:
        where = "price < 100 and prize_amout > 10"
        order_by = "prize_amout desc"
        re = con.execute(
            """select sku, title, price, bonus_rate, prize_amout, ticket_amount , image_url, url
                from jingfen_products 
                where {where} 
                order by {order_by};""".format(where=where, order_by=order_by))
        bid_list = [
            {"id": x[0], "title": x[1].decode('utf-8'), "price": format_app_num(x[2], f=0),
             "bonus_rate": format(format_app_num(x[3] * 100, f=0)),
             "prize_amout": format_app_num(x[4], f=2), "ticket_amount": format_app_num(x[5], f=0), "url": x[7],
             "image_url": x[6]} for x in re]
    return render_template("home.html", bid_list=bid_list)


@app.route("/tuijian")
def get_tuijian_bids():
    with engine.connect() as con:
        where = "price < 100 and prize_amout > 10"
        order_by = "prize_amout desc"
        re = con.execute(
            """select sku, title, price, bonus_rate, prize_amout, ticket_amount , image_url, url
                from jingfen_products 
                where {where} 
                order by {order_by};""".format(where=where, order_by=order_by))
        bid_list = [
            {"id": x[0], "title": x[1].decode('utf-8'), "price": format_app_num(x[2], f=0),
             "bonus_rate": format(format_app_num(x[3] * 100, f=0)),
             "prize_amout": format_app_num(x[4], f=2), "ticket_amount": format_app_num(x[5], f=0), "url": x[7],
             "image_url": x[6]} for x in re]
    return render_template("home.html", bid_list=bid_list)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
