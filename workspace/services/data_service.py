from models.data_model import DataModel
from utils.pagination import paginate

data_model = DataModel()

def get_paginated_data(page, pageSize):
    total_records = len(data_model.data)
    paginated_data = paginate(data_model.data, page, pageSize)
    response_data = paginated_data.to_dict(orient='records')
    total_pages = (total_records + pageSize - 1) // pageSize
    return {
        "page": page,
        "pageSize": pageSize,
        "totalItem": total_records,
        "totalPages": total_pages,
        "data": response_data
    }

def get_revenue_per_product(page, pageSize):
    revenue_per_product = data_model.data.groupby('PRODUCTCODE')['Revenue'].sum().sort_values(ascending=False)
    paginated_data = paginate(revenue_per_product, page, pageSize)
    response_data = paginated_data.to_dict()
    total_records = len(revenue_per_product)
    total_pages = (total_records + pageSize - 1) // pageSize
    return {
        "page": page,
        "pageSize": pageSize,
        "totalItem": total_records,
        "totalPages": total_pages,
        "data": response_data
    }

def get_revenue_per_product(page, pageSize):
    total_units_sold = data_model.data.groupby('PRODUCTCODE')['QUANTITYORDERED'].sum().sort_values(ascending=False)
    paginated_data = paginate(total_units_sold, page, pageSize)
    response_data = paginated_data.to_dict()
    total_records = len(total_units_sold)
    total_pages = (total_records + pageSize - 1) // pageSize

    return {
        "page": page,
        "pageSize": pageSize,
        "totalItem": total_records,
        "totalPages": total_pages,
        "data": response_data
    }


def avg_price_per_product(page, pageSize):
    avg_price_per_product = data_model.data.groupby('PRODUCTCODE')['PRICEEACH'].mean().sort_values(ascending=False)
    paginated_data = paginate(avg_price_per_product, page, pageSize)
    response_data = paginated_data.to_dict()
    total_records = len(avg_price_per_product)
    total_pages = (total_records + pageSize - 1) // pageSize
    return {
        "page": page,
        "pageSize": pageSize,
        "totalItem": total_records,
        "totalPages": total_pages,
        "data": response_data
    }


def orders_per_product(page, pageSize):
    total_orders_per_product = data_model.data.groupby('PRODUCTCODE')['ORDERNUMBER'].nunique().sort_values(ascending=False)
    paginated_data = paginate(total_orders_per_product, page, pageSize)
    response_data = paginated_data.to_dict()
    total_records = len(total_orders_per_product)
    total_pages = (total_records + pageSize - 1) // pageSize
    return {
        "page": page,
        "pageSize": pageSize,
        "totalItem": total_records,
        "totalPages": total_pages,
        "data": response_data
    }


def revenue_per_city(page, pageSize):
    city_revenue = data_model.data.groupby('City')['Revenue'].sum().sort_values(ascending=False).head(5)
    paginated_data = paginate(city_revenue, page, pageSize)
    response_data = paginated_data.to_dict()
    total_records = len(city_revenue)
    total_pages = (total_records + pageSize - 1) // pageSize
    return {
        "page": page,
        "pageSize": pageSize,
        "totalItem": total_records,
        "totalPages": total_pages,
        "data": response_data
    }


def revenue_per_month(page, pageSize):
   # حساب الإيرادات الشهرية
    monthly_revenue = data_model.data.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()
    # تحويل الـ DataFrame إلى شكل يمكن لـ JSON التعامل معه
    monthly_revenue['YearMonth'] = monthly_revenue['Year'].astype(str) + '-' + monthly_revenue['Month'].astype(str)
    # حذف الأعمدة الأصلية
    monthly_revenue = monthly_revenue[['YearMonth', 'Revenue']]

    paginated_data = paginate(monthly_revenue, page, pageSize)
    total_records = len(monthly_revenue)
    total_pages = (total_records + pageSize - 1) // pageSize
    response_data = paginated_data.to_dict(orient='records')
    return {
        "page": page,
        "pageSize": pageSize,
        "totalItem": total_records,
        "totalPages": total_pages,
        "data": response_data
    }

def monthly_metrics(page, pageSize):
     # حساب الإيرادات الشهرية، إجمالي الوحدات المباعة ومتوسط السعر لكل وحدة لكل شهر
    monthly_metrics = data_model.data.groupby(['Year', 'Month']).agg(
        TotalRevenue=('Revenue', 'sum'),
        TotalUnitsSold=('QUANTITYORDERED', 'sum'),
        AveragePricePerUnit=('PRICEEACH', 'mean')
    ).reset_index()

    # تحويل الأعمدة السنة والشهر إلى تنسيق قابل للقراءة
    monthly_metrics['YearMonth'] = monthly_metrics['Year'].astype(str) + '-' + monthly_metrics['Month'].astype(str)

    # حذف الأعمدة الأصلية
    monthly_metrics = monthly_metrics[['YearMonth', 'TotalRevenue', 'TotalUnitsSold', 'AveragePricePerUnit']]

    paginated_data = paginate(monthly_metrics, page, pageSize)
    total_records = len(monthly_metrics)
    total_pages = (total_records + pageSize - 1) // pageSize

    start_index = (page - 1) * pageSize
    end_index = start_index + pageSize
    paginated_data = monthly_metrics.iloc[start_index:end_index]

    response_data = paginated_data.to_dict(orient='records')
    return {
        "page": page,
        "pageSize": pageSize,
        "totalItem": total_records,
        "totalPages": total_pages,
        "data": response_data
    }

