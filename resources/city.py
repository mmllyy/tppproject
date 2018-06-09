import json
import pymysql
with open('citys.json','rb') as f:
    citys = json.load(f)
    print(type(citys))
    print(citys)

    db = pymysql.connect(host='10.35.163.12',
                         port=3306,
                         user='root',
                         password='root',
                         db='tpp',
                         charset='utf8')
    cursor = db.cursor()

    print('数据库连接成功')
    values = citys.get('returnValue')
    for letter in values.keys():
        cursor.execute('insert letter(name) values(%s)',letter)
        cursor.execute('select id from letter where name=%s',letter)
        letter_id = cursor.fetchone()[0]
        print('添加成功'+letter,letter_id)

        for city in values.get(letter):
            cursor.execute('insert city values(%s,%s,%s,%s,%s,%s)',
                           (city.get('id'),
                            city.get('parentId'),
                            city.get('refionName'),
                            city.get('cityCode'),
                            city.get('pinYin'),
                            letter_id
                            ))
    db.commit()
