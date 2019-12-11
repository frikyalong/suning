## 步骤分析

```
苏宁做了反爬处理，即不会把一些重要信息直接作为response返回，而且在网页加载结束之后，通过js在将对应的值赋值上去。

一个页面它打算渲染出120个产口， 首先他先渲染出60个坑，这60个坑， 他只渲染出框架， 前30个会渲染出图片， 名字， 但关键信息没有， 这是为了让
百度这种搜索引擎索引到他的产品， 但不让竞争对手爬到到价格， 有没有货， 这些敏感信息， 等用户划到页面中部， 再渲染下面30个。
这是第一步

第二步， 每当用户滑动1/2行(1行或2行， 我试了几回， 他们这个好像是随机的， 有时是1行， 有时是2行)，他会发送一个jsonp 请求， 他这1/2行的5/10个产品的敏感数据渲染出来。
url例子: https://ds.suning.com/ds/generalForTile/000000000126064388____R9000367_00016B011,000000000193530581____R9000367_00016B011,000000000103720815____R9000367_00016B011,000000010639318036_____,000000000131207309____R9000367_00016B011,000000000136298631____R9000367_00016B011,000000000163962086____R9000367_00016B011,000000000619510997____R9000367_00016B011,000000000773368977____R9000367_00016B011,000000000147225193____R9000367_00016B011-021-2-0000000000-1--ds0000000001311.jsonp?callback=ds0000000001311
返回值中的shoppingCart这个字段表示是否有货

苏宁服务 这个在url中 ct 这个参数
收货地：
pageload后 会发出一个 web.jsonp请求， city参数在这里。 用区号表示
https://search.suning.com/emall/abtest/v1/web.jsonp?callback=callAbtest&p=search&f=ACAABAABCAAA&v=22%2C12%2C7%2C1%2C27%2C4%2C3%2C18%2C3%2C4%2C2%2C1&city=021&_=1575364927392
city: 021

苏宁用了jsonp的方法做了价格的获取
每次得到5个值，页面上一行也是5个商品

他们的做法是，当每次鼠标向下移动，下一行商品出现的时候，执行一个jsonp方法，将对应的内容进行绑定
苏宁服务 ct=1
shoppingCart=1 有货


第二次分析：
每个页面会加载4次， 第一资是pageload， 前30个产品， user向下滑动， 异步请求下30个产品的html（不包含价格， 是否有货）。 这时请求的是html， 不是json数据。
再把把回的html动态绑定到页面中， 当用户划到某一行， 再用li中的信息拼出price request url, 通过jsonp动态绑定。
```

## 解决方法
```
每一页分4次请求每次30个
先拿product id, brand_id, threegroup_id, 再拼get detail url
手机区号数据集

获取product_id url， 返回值里只有id, name, 没有价格， 是否有货，拿到返回结果后， parse 出product_id， 再拼出获取详细信息的url。
https://search.suning.com/emall/searchV1Product.do?keyword=%E9%AB%98%E6%B4%81%E4%B8%9D&ci=0&pg=01&cp=0&il=0&st=0&iy=0&hf=brand_Name_FacetAll:%E9%AB%98%E6%B4%81%E4%B8%9D&ct=1&isNoResult=0&n=1&sc=0&sesab=ACAABAABCAAA&id=IDENTIFYING&cc=010&paging=1&sub=0&jzq=69
https://search.suning.com/emall/searchV1Product.do?keyword=%E9%AB%98%E6%B4%81%E4%B8%9D&ci=0&pg=01&cp=0&il=0&st=0&iy=0&hf=brand_Name_FacetAll:%E9%AB%98%E6%B4%81%E4%B8%9D&ct=1&isNoResult=0&n=1&sc=0&sesab=ACAABAABCAAA&id=IDENTIFYING&cc=010&paging=2&sub=0&jzq=69
https://search.suning.com/emall/searchV1Product.do?keyword=%E9%AB%98%E6%B4%81%E4%B8%9D&ci=0&pg=01&cp=0&il=0&st=0&iy=0&hf=brand_Name_FacetAll:%E9%AB%98%E6%B4%81%E4%B8%9D&ct=1&isNoResult=0&n=1&sc=0&sesab=ACAABAABCAAA&id=IDENTIFYING&cc=010&paging=2&sub=0&jzq=69

https://search.suning.com/emall/searchV1Product.do?keyword=%E9%AB%98%E6%B4%81%E4%B8%9D&ci=0&pg=01&cp=0&il=0&st=0&iy=0&hf=brand_Name_FacetAll:%E9%AB%98%E6%B4%81%E4%B8%9D&ct=1&isNoResult=0&n=1&sc=0&sesab=ACAABAABCAAA&id=IDENTIFYING&cc=0412&paging=3&sub=0&jzq=69

https://search.suning.com/emall/searchV1Product.do?
keyword=%E9%AB%98%E6%B4%81%E4%B8%9D&
ci=0&
pg=01&
cp=0&
il=0&
st=0&
iy=0&
hf=brand_Name_FacetAll:%E9%AB%98%E6%B4%81%E4%B8%9D&
ct=1&  --- 苏宁服务
isNoResult=0&
n=1&
sc=0&
sesab=ACAABAABCAAA&
id=IDENTIFYING&
cc=010&  --- city
paging=1&  ---- page
sub=0&
jzq=69

获取detail url
https://ds.suning.com/ds/generalForTile/000000000945059170____362508_00016B011,  000000000945067305____362508_00016B011,000000000945067303_____00016B011,            000000000945067302_____00016B011-021-2-0000000000-1--ds0000000004251.jsonp?callback=ds0000000004251
https://ds.suning.com/ds/generalForTile/000000000105675991____R9000367_00016B011,000000000134938829____R9000367_00016B011,00000000011377607851____R9000367_00016B011,00000000011293408762____R9000367_00016B011,000000000945071319_____00016B011,000000000945059170____362508_00016B011,000000000945067305____362508_00016B011,000000000945067303_____00016B011,000000000945067302_____00016B011-010-2-0000000000-1--ds0000000004251.jsonp?callback=ds0000000004251
        product_id   threegroup_id  brand_id
000000000945059170____362508_00016B011,
000000000945067305____362508_00016B011,
000000000945067303____{}_00016B011,
000000000945067302____{}_00016B011-021-2-0000000000-1--ds0000000004251.jsonp?callback=ds0000000004251
在res-info中有相应信息：
<span class="def-price" datasku="945067303|||||0000000000" brand_id="00016B011" threegroup_id="">
000000000{product_id}____{threegroup_id}_{brand_id}
000000000{product_id}______{brand_id}
-{area_code}-2-0000000000-1--ds0000000004251.jsonp?callback=ds0000000004251
fuck!


https://ds.suning.com/ds/generalForTile/000000000103720844____R9000368_00016B011,000000000134938829____R9000367_00016B011,000000000675046017____R9000367_00016B011,000000011377607851____R9000367_00016B011,000000011293408762____R9000367_00016B011,000000000945059170____362508_00016B011,000000000945067305____362508_00016B011,000000000945067303_____00016B011,000000000945067302_____00016B011-021-2-0000000000-1--ds0000000001214.jsonp?callback=ds0000000001214
https://ds.suning.com/ds/generalForTile/000000000103720844____R9000368_00016B011,000000000134938829____R9000367_00016B011,000000000675046017____R9000367_00016B011,000000011377607851____R9000367_00016B011,000000011293408762____R9000367_00016B011-021-2-0000000000-1--ds0000000004251.jsonp?callback=ds0000000004251








https://ds.suning.com/ds/generalForTile/000000000103720844____R9000368_00016B011,000000000134938829____R9000367_00016B011,000000000675046017____R9000367_00016B011,00000000011377607851____R9000367_00016B011,00000000011293408762____R9000367_00016B011-021-2-0000000000-1--ds0000000004251.jsonp?callback=ds0000000004251


000000000103720844
00000000011377607851
000000011377607851


18



2019-12-07 15:12:54
69cd05637219 4d81d6cf34fc 3abd18f60a8e 29604fd47dc9
```