aa = {'13': {'number': '2', 'info': {'p_price': 111.0, 'city__name': '佛山市', 'p_business': 1, 'p_name': '合伙企业注册', 'p_category__name': '合伙企业注册', 'area__name': '顺德区'}},}

for k,v in aa.items():
    print(v)
    print(v['number'])
    print(v['info']['p_price'])