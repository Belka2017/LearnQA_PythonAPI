import requests

URL = 'https://playground.learnqa.ru/ajax/api/compare_query_type'
metod_1 = ['GET', 'POST', 'PUT', 'DELETE']
metod_for_use_1 = [requests.get, requests.post, requests.put, requests.delete]
metod_for_use_2 = [requests.head, requests.patch, requests.options]

# Делает http-запрос любого типа без параметра method
for m in metod_for_use_1:
    resp1 = m(URL)
    print(f"1. For {m.__name__.upper()} status_code = {resp1.status_code} and response = {resp1.text}")

# Делает http-запрос не из списка без параметра method
for m in metod_for_use_2:
    resp2 = m(URL)
    print(f"2. For {m.__name__.upper()} status_code = {resp2.status_code} and response = {resp2.text}")

# Делает http-запрос с правильным параметром method
method_map = {
    "GET": requests.get,
    "POST": requests.post,
    "PUT": requests.put,
    "DELETE": requests.delete
}

for m_name, m in method_map.items():
    key = "params" if m == requests.get else "data"
    kwargs = {key: {"method": m_name}}
    resp3 = m(URL, **kwargs)
    print(f"3. For method {m.__name__.upper()} status_code = {resp3.status_code} and response = {resp3.text}")

# Цикл на все возможные сочетания реальных типов запроса и параметра method
for method_to_use in metod_for_use_1:
    for method_str in metod_1:
        key = "params" if method_to_use == requests.get else "data"
        kwargs = {key: {"method": method_str}}
        resp4 = method_to_use(URL, **kwargs)

        txt = resp4.text
        a = resp4.request.method
        if method_str != a and "success" in txt:
            print(f"4. Incorrect operation. For method {a} with method = {method_str} server response is {txt}")
        elif method_str == a and "Wrong" in txt:
            print(f"4. Incorrect operation. For method {a} with method = {method_str} server response is {txt}")