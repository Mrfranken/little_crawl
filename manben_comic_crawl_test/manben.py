import requests
from urllib.parse import parse_qs, urlparse
'''
此脚本已不可用
'''

url_list = [
    'http://manhua1032-61-174-50-99.cdndm5.com/34/33991/521588/2_5237.jpg?cid=521589&key=87da850923c6eb9e837d61ed182d5800',
    'http://manhua1032-61-174-50-99.cdndm5.com/34/33991/521588/3_3559.jpg?cid=521589&key=87da850923c6eb9e837d61ed182d5800',
    'http://manhua1032-61-174-50-99.cdndm5.com/34/33991/521588/4_2797.jpg?cid=521589&key=87da850923c6eb9e837d61ed182d5800',
    'http://manhua1032-61-174-50-99.cdndm5.com/34/33991/521588/5_5635.jpg?cid=521589&key=87da850923c6eb9e837d61ed182d5800']

for url in url_list:
    parser = urlparse(url)
    scheme = parser.scheme
    netloc = parser.netloc
    path = parser.path
    query_para = dict([(k, v[0]) for k, v in parse_qs(urlparse(url).query).items()])
    query_para.update({'cid': int(query_para.get('cid'))})
    url1 = scheme + "://" + netloc + path
    outcome = requests.get(url=url1, params=query_para).content
    with open(r'D:\pic{}.jpg'.format(url_list.index(url)), 'wb') as f:
        f.write(outcome)
        f.close()
