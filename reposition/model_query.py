from . import models


def login_user_query(obj):
    phone = obj.cleaned_data.get('phone')
    password = obj.cleaned_data.get('password')
    user_obj = models.Users.objects.filter(phone=phone, password=password).values('id', 'name').first()
    if user_obj:
        return user_obj


def login_employee_query(obj):
    email = obj.get('email')
    password = obj.get('password')
    employee_obj = models.Employees.objects.filter(email=email, password=password).values('id', 'email', 'name').first()

    if employee_obj:
        return employee_obj


def query_all(tb_name):
    obj = tb_name.objects.all()
    return obj


def order_counts(phone):
    data = {}
    order_count = models.Orders.objects.raw(
        """SELECT t.id,t.order_state,COUNT(t.id) AS counts  FROM (SELECT id,order_code,order_state FROM orders WHERE phone=phone GROUP BY order_state,order_code) AS t  GROUP BY order_state""")
    for line in order_count:
        if line.order_state == 0:
            data['pending_pay'] = line.counts
        elif line.order_state == 1:
            data['to_be_service'] = line.counts
        elif line.order_state == 2:
            data['in_service'] = line.counts
        elif line.order_state == 3:
            data['service_completed'] = line.counts
        else:
            pass
    return data
