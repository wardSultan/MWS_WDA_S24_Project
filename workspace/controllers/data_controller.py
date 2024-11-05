from flask import Blueprint, request, jsonify
from services import data_service

bp = Blueprint('data', __name__)

@bp.route('/data', methods=['GET'])
def get_data():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    response = data_service.get_paginated_data(page, pageSize)
    return jsonify(response)

@bp.route('/revenue-per-product', methods=['GET'])
def revenue_per_product():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    response = data_service.get_revenue_per_product(page, pageSize)
    return jsonify(response)


# 3. إجمالي الوحدات المباعة لكل منتج
@bp.route('/units-sold-per-product', methods=['GET'])
def units_sold_per_product():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    response = data_service.get_revenue_per_product(page, pageSize)
    return jsonify(response)


# 4. متوسط السعر لكل وحدة لكل منتج
@bp.route('/avg-price-per-product', methods=['GET'])
def avg_price_per_product():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    response = data_service.avg_price_per_product(page, pageSize)
    return jsonify(response)






# 5. إجمالي عدد الطلبات لكل منتج
@bp.route('/orders-per-product', methods=['GET'])
def orders_per_product():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    response = data_service.orders_per_product(page, pageSize)
    return jsonify(response)



# 6. إيرادات كل مدينة
@bp.route('/revenue-per-city', methods=['GET'])
def revenue_per_city():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    response = data_service.revenue_per_city(page, pageSize)
    return jsonify(response)

    

# 7. إيرادات كل شهر
@bp.route('/revenue-per-month', methods=['GET'])
def revenue_per_month():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    response = data_service.revenue_per_month(page, pageSize)
    return jsonify(response)
 



@bp.route('/monthly-metrics', methods=['GET'])
def monthly_metrics():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    response = data_service.monthly_metrics(page, pageSize)
    return jsonify(response)


