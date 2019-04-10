# 云片短信回调实例

## 短信回复回调
[link](https://www.yunpian.com/doc/zh_CN/domestic/push_reply.html)

## 短信状态回调
[link](https://www.yunpian.com/doc/zh_CN/domestic/push_report.html)

> 用户回调取数据时可能会有问题，回传的数据被编码过了，像'{"'等字符都被转义了，
需要先转回原本的字符，再进行json反序列化，从而取到对应的数据

## explame:
```
reply_data = request.form.get('sms_reply') # 取到已经转义的字符串
reply_dict = json.loads(urllib.parse.unquote(reply_data)) # 将字符串还原并反序列化
```