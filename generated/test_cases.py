import requests

def test_case_0():
    resp = requests.get('https://www.baidu.com')
    assert resp.status_code == 200

def test_case_1():
    resp = requests.get('https://www.baidu.com/404')
    assert resp.status_code == 404

