import json
import requests
from requests_toolbelt.multipart import MultipartEncoder

layout = {
    "vlVersion": "0.0.1",
    "subject": "title",
    "frames": [
        {
            "index": 1,
            "playTimes": 1,
            "attachments": [
                {
                    "index": 1,
                    "fileName": "text1.txt"
                },
                {
                    "index": 2,
                    "fileName": "img1.jpg"
                }
            ]
        }
    ]
}


def add_tpl(filepath):
    """
    :param filepath: 文件路径
    :return:
    """
    url = 'https://vsms.yunpian.com/v2/vsms/add_tpl.json'
    m_data = MultipartEncoder(
        fields={
            'apikey': 'xxxxxxx',
            'sign': 'xxxxxxxx',
            'layout': json.dumps(layout),
            'material': (filepath, open(filepath, 'rb'), 'application/octet-stream')
        },
    )
    headers = {
        'Content-Type': m_data.content_type
    }

    r = requests.post(url, data=m_data, headers=headers)
    print(r.text)
    print(r.request.headers)
    return 0

if __name__ == '__main__':
    add_tpl('./xxx.zip')
