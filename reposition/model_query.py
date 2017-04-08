from . import models


def login_user_query(obj):
    phone = obj.cleaned_data.get('phone')
    password = obj.cleaned_data.get('password')
    user_obj = models.Users.objects.filter(phone=phone, password=password).values_list('id').first()
    if user_obj:
        return user_obj


def login_employee_query(obj):
    email = obj.get('email')
    password = obj.get('password')
    employee_obj = models.Employees.objects.filter(email=email, password=password).values_list('id').first()
    if employee_obj:
        return employee_obj


def query_all(tb_name):
    obj = tb_name.objects.all()
    return obj


def order_counts(phone):
    pending_pay = None
    to_be_service = None
    in_service = None
    service_completed = None
    order_count = models.Orders.objects.raw(
        """SELECT id,COUNT(id) as count,order_state FROM orders WHERE phone=phone GROUP BY order_state""")
    for line in order_count:
        if line.order_state == '待付款':
            pending_pay = line.count
        elif line.order_state == '待服务':
            to_be_service = line.count
        elif line.order_state == '服务中':
            in_service = line.count
        elif line.order_state == '服务完成':
            service_completed = line.count
        else:
            pass
    return pending_pay, to_be_service, in_service, service_completed
