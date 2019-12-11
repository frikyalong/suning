import json, re


def build_jsonp_urls(url_codes, area_code):
    jsonp_urls = []
    url_template = "https://ds.suning.com/ds/generalForTile/{}-{}-2-0000000000-1--ds0000000004251.jsonp?callback=ds0000000004251"
    url_codes_lists = list_split(url_codes, 5)
    for url_codes_list in url_codes_lists:
        if len(url_codes_list) > 0:
            jsonp_url = url_template.format(','.join(url_codes_list), area_code)
            jsonp_urls.append(jsonp_url)
    return jsonp_urls


def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')
