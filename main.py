
import psycopg2
import requests

from config import host,user,password,db_name
from bs4 import BeautifulSoup




url='https://bdu.fstec.ru/vul'


headers={
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
}

req=requests.get(url,headers=headers)
src=req.text

soup=BeautifulSoup(src,"lxml")
bdus=soup.find_all(class_='confirm-vul')
names=soup.find_all(class_='name')

cwes=[]

for link in bdus:
    href="https://bdu.fstec.ru"+link.get("href")
    req=requests.get(href,headers=headers)
    src=req.text

    soup=BeautifulSoup(src,"lxml")
    tr=soup.find(class_="table table-striped attr-view-table").find_all("tr")[7].find("a").text
    cwes.append(tr)
    
# print(cwes)



# with open ("pars.txt","w",encoding='UTF-8') as file:

#     for bdu,name,cwe in zip(bdus,names,cwes):
#         print("======================================================================================")
#         print(bdu.text,name.text,"https://bdu.fstec.ru"+bdu.get("href"),cwe)


#         file.write(f" {bdu.text} {name.text[1:-1]} {cwe} {'https://bdu.fstec.ru'+bdu.get('href')}\n") 

#         # срезы, f-строки, методы, ф-ии




try:
    connection=psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit=True

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f"Server version: {cursor.fetchall}")

    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS data (
    id serial PRIMARY KEY,
    BDU TEXT NOT NULL,
    DESCRYPTION TEXT NOT NULL,
    VULNERABILITY_SYSTEM_INDENTIFIERS TEXT NOT NULL,
    LINK TEXT NOT NULL

);""")
        print("[INFO] Table create successfully!")

    with connection.cursor() as cursor:
        for bdu,name,cwe in zip(bdus,names,cwes):
            data_site=(bdu.text ,name.text[1:-1],cwe ,'https://bdu.fstec.ru'+bdu.get('href'))
            cursor.execute(f'''INSERT INTO data(BDU,DESCRYPTION,VULNERABILITY_SYSTEM_INDENTIFIERS,LINK) VALUES ('{bdu.text}', '{name.text[1:-1]}','{cwe}','{'https://bdu.fstec.ru'+bdu.get('href')}');'''.format(*data_site))
        print("[INFO] INSERT successfully")  
    

except Exception as _ex:
    print("[INFO] Error while working with PostreSQL",_ex)
finally:
    connection.close()
    print("[INFO] PostgreSQL connection closed")















# data_site=[f" {bdu.text} {name.text[1:-1]} {cwe} {'https://bdu.fstec.ru'+bdu.get('href')}"]



# for bdu,name,cwe in zip(bdus,names,cwes):
#     data_site=(bdu.text ,name.text[1:-1],cwe ,'https://bdu.fstec.ru'+bdu.get('href'))
    
#     sql.execute('''INSERT INTO data(BDU,DESCRYPTION,VULNERABILITY_SYSTEM_INDENTIFIERS,LINK) VALUES (?,?,?,?)''',data_site)
#     db.commit()
# sql.execute("SELECT * FROM data")
# if sql.fetchall() is None:
#     sql.execute(f'''INSERT INTO data(BDU,ОПИСАНИЕ, ИДЕНТИФИКАТОРЫ СИСТЕМ УЯЗВИМОСТЕЙ,ССЫЛКА) VALUES (?,?,?,?)''',data_site)
#     db.commit()
#     print('База данных создана')
# else:
#     print('Такакя база уже имеется')
    
# for value in sql.execute("SELECT * FROM data"):
#     print(value)