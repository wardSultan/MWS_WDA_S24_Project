


from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
app = Flask(__name__)

# تحميل البيانات
data = pd.read_csv(r'.\sales_data_sample.csv', encoding='ISO-8859-1')

# تنظيف البيانات
data = data.dropna()
data['Revenue'] = data['QUANTITYORDERED'] * data['PRICEEACH']

# التأكد من تحويل عمود التاريخ إلى نوع datetime
data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'])
data['Month'] = data['ORDERDATE'].dt.month
data['Year'] = data['ORDERDATE'].dt.year
data['City'] = data['CITY'].apply(lambda x: x)

# Pagination function
def paginate(queryset, page, pageSize):
    start = (page - 1) * pageSize
    end = start + pageSize
    return queryset[start:end]

# 1. عرض البيانات الأولية مع البحث والصفحات
@app.route('/data', methods=['GET'])
def get_data():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    
    # إجمالي السجلات بعد الفلترة
    total_records = len(data)
    
    # حساب إجمالي الصفحات
    total_pages = (total_records + pageSize - 1) // pageSize
    
    # تطبيق الـ pagination
    paginated_data = paginate(data, page, pageSize)
   
    # تحويل البيانات إلى قائمة سجلات
    response_data = paginated_data.to_dict(orient='records')
    
    # إعداد الاستجابة
    response = {
        "page": page,
        "pageSize": pageSize,
        "totalItem": total_records,  # إجمالي السجلات بعد الفلترة
        "totalPages": total_pages,  # إجمالي عدد الصفحات
        "data": response_data,  # البيانات المفصلة
    }

    return jsonify(response)

  
        

# 2. إجمالي الإيرادات لكل منتج مع دعم الصفحات
@app.route('/revenue-per-product', methods=['GET'])
def revenue_per_product():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    
    # حساب إجمالي الإيرادات لكل منتج
    total_revenue_per_product = data.groupby('PRODUCTCODE')['Revenue'].sum().sort_values(ascending=False)
    
    # حساب إجمالي السجلات
    total_records = len(total_revenue_per_product)
    
    # حساب عدد الصفحات الكلي
    total_pages = (total_records + pageSize - 1) // pageSize  # تقريب للأعلى
    
    # تطبيق الـ pagination
    paginated_data = paginate(total_revenue_per_product, page, pageSize)
    
    # تحويل البيانات إلى القاموس
    response_data = paginated_data.to_dict()
 
    # إعداد الاستجابة
    response = {
        "page": page,
        "pageSize": pageSize,
        "totalItem":len(total_revenue_per_product),
        "totalPages": total_pages,       # إجمالي الصفحات
        "data": response_data,           # البيانات المقسمة
    }

    return jsonify(response)



# 3. إجمالي الوحدات المباعة لكل منتج
@app.route('/units-sold-per-product', methods=['GET'])
def units_sold_per_product():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    
    total_units_sold = data.groupby('PRODUCTCODE')['QUANTITYORDERED'].sum().sort_values(ascending=False)
     # حساب إجمالي السجلات
    total_records = len(total_units_sold)
    
    # حساب عدد الصفحات الكلي
    total_pages = (total_records + pageSize - 1) // pageSize  # تقريب للأعلى

    paginated_data = paginate(total_units_sold, page, pageSize)

    response_data = paginated_data.to_dict()

    response = {
        "page": page,
        "pageSize": pageSize,
        "totalItem":len(total_units_sold),
        "totalPages": total_pages,       # إجمالي الصفحات
        "data": response_data,           # البيانات المقسمة
    }

    return jsonify(response)

# 4. متوسط السعر لكل وحدة لكل منتج
@app.route('/avg-price-per-product', methods=['GET'])
def avg_price_per_product():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))

    avg_price_per_product = data.groupby('PRODUCTCODE')['PRICEEACH'].mean().sort_values(ascending=False)
    
   
      # حساب إجمالي السجلات
    total_records = len(avg_price_per_product)
    
    # حساب عدد الصفحات الكلي
    total_pages = (total_records + pageSize - 1) // pageSize  # تقريب للأعلى

    paginated_data = paginate(avg_price_per_product, page, pageSize)

    response_data = paginated_data.to_dict()

    response = {
        "page": page,
        "pageSize": pageSize,
        "totalItem":len(avg_price_per_product),
        "totalPages": total_pages,       # إجمالي الصفحات
        "data": response_data,           # البيانات المقسمة
    }

    return jsonify(response)

# 5. إجمالي عدد الطلبات لكل منتج
@app.route('/orders-per-product', methods=['GET'])
def orders_per_product():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    
    total_orders_per_product = data.groupby('PRODUCTCODE')['ORDERNUMBER'].nunique().sort_values(ascending=False)
    
     # حساب إجمالي السجلات
    total_records = len(total_orders_per_product)
    
    # حساب عدد الصفحات الكلي
    total_pages = (total_records + pageSize - 1) // pageSize  # تقريب للأعلى

    paginated_data = paginate(total_orders_per_product, page, pageSize)

    response_data = paginated_data.to_dict()

    response = {
        "page": page,
        "pageSize": pageSize,
        "totalItem":len(total_orders_per_product),
        "totalPages": total_pages,       # إجمالي الصفحات
        "data": response_data,           # البيانات المقسمة
    }

    return jsonify(response)

# 6. إيرادات كل مدينة
@app.route('/revenue-per-city', methods=['GET'])
def revenue_per_city():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    
    city_revenue = data.groupby('City')['Revenue'].sum().sort_values(ascending=False).head(5)
    
     # حساب إجمالي السجلات
    total_records = len(city_revenue)
    
    # حساب عدد الصفحات الكلي
    total_pages = (total_records + pageSize - 1) // pageSize  # تقريب للأعلى

    paginated_data = paginate(city_revenue, page, pageSize)

    response_data = paginated_data.to_dict()

    response = {
        "page": page,
        "pageSize": pageSize,
        "totalItem":len(city_revenue),
        "totalPages": total_pages,       # إجمالي الصفحات
        "data": response_data,           # البيانات المقسمة
    }

    return jsonify(response)

# 7. إيرادات كل شهر
@app.route('/revenue-per-month', methods=['GET'])
def revenue_per_month():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
 
    # حساب الإيرادات الشهرية
    monthly_revenue = data.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()

    # تحويل الـ DataFrame إلى شكل يمكن لـ JSON التعامل معه
    monthly_revenue['YearMonth'] = monthly_revenue['Year'].astype(str) + '-' + monthly_revenue['Month'].astype(str)
    
    # حذف الأعمدة الأصلية
    monthly_revenue = monthly_revenue[['YearMonth', 'Revenue']]

    # حساب إجمالي السجلات
    total_records = len(monthly_revenue)
    
    # حساب عدد الصفحات الكلي
    total_pages = (total_records + pageSize - 1) // pageSize  # تقريب للأعلى

    # تقسيم البيانات
    paginated_data = paginate(monthly_revenue, page, pageSize)

    response_data = paginated_data.to_dict(orient='records')


  
    response = {
        "page": page,
        "pageSize": pageSize,
        "totalItem": total_records,
        "totalPages": total_pages, 
        "data": response_data,
    }

    return jsonify(response)

@app.route('/monthly-metrics', methods=['GET'])
def monthly_metrics():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))

    # حساب الإيرادات الشهرية، إجمالي الوحدات المباعة ومتوسط السعر لكل وحدة لكل شهر
    monthly_metrics = data.groupby(['Year', 'Month']).agg(
        TotalRevenue=('Revenue', 'sum'),
        TotalUnitsSold=('QUANTITYORDERED', 'sum'),
        AveragePricePerUnit=('PRICEEACH', 'mean')
    ).reset_index()

    # تحويل الأعمدة السنة والشهر إلى تنسيق قابل للقراءة
    monthly_metrics['YearMonth'] = monthly_metrics['Year'].astype(str) + '-' + monthly_metrics['Month'].astype(str)

    # حذف الأعمدة الأصلية
    monthly_metrics = monthly_metrics[['YearMonth', 'TotalRevenue', 'TotalUnitsSold', 'AveragePricePerUnit']]

    # حساب إجمالي السجلات وعدد الصفحات
    total_records = len(monthly_metrics)
    total_pages = (total_records + pageSize - 1) // pageSize

    # تقسيم البيانات للصفحة المطلوبة
    start_index = (page - 1) * pageSize
    end_index = start_index + pageSize
    paginated_data = monthly_metrics.iloc[start_index:end_index]

    # تحويل البيانات إلى صيغة JSON
    response_data = paginated_data.to_dict(orient='records')

    response = {
        "page": page,
        "pageSize": pageSize,
        "totalItems": total_records,
        "totalPages": total_pages,
        "data": response_data,
    }
    return jsonify(response)

# تشغيل التطبيق
if __name__ == '__main__':

    app.debug = True
    CORS(app)
    app.run(host='0.0.0.0',port=3000)
 