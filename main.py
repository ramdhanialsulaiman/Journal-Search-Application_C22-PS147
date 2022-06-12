import pymysql
from app import app
from flask import jsonify
from flask import flash,request
from config import mysql
from flaskext.mysql import MySQL
import tensorflow as tf 
import Prediction
model=tf.keras.models.load_model("my_model.h5")

vocab_size = 10000
embedding_dim = 64
max_length = 200
trunc_type = 'post'
padding_type = 'post'
oov_tok = '<OOV>'
TRAINING_SPLIT = .8


#saat mengklik 1 kategori
@app.route('/kategori', methods=["GET"])
def kategori_jurnal():
    label=request.args.get('label')
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT title FROM data_jurnal WHERE label=%s",label)
    result= cursor.fetchall()
    response=jsonify(result)
    conn.close()
    if result:
        return jsonify(result)
    else :
        response: jsonify('data tidak ditemukan')
        return response

#saat masuk kedalam 1 kategori, lalu melakukan searching
@app.route('/kategori/', methods=['GET'])
def cari_jurnal_dalamKategori():
    cursor=None;
    label=request.args.get('label')
    title="%"+request.args.get('title')+"%"
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM data_jurnal WHERE label=%s AND title LIKE %s",(label,title))
    result=cursor.fetchall()
    if result:
        return jsonify(result)
    else:
        response: jsonify('data tidak ditemukan')
        return response

#pencarian secara umum (bisa dimasukin sesuai keyword judul)/dibagian menu
@app.route('/search/', methods=['GET'])
def cari_jurnal():
    cursor=None;
    title="%"+request.args.get('title')+"%"
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM data_jurnal WHERE  title LIKE %s",title)
    result=cursor.fetchall()
    if result:
        return jsonify(result)
    else:
        response: jsonify('data tidak ditemukan')
        return response

#mengupload jurnal
@app.route('/upload', methods=['POST'])
def upload_jurnal():
    try:
      _json=request.json
      print(_json)
      _authors=_json['authors']
      _title=_json['title']
      #x = Prediction.predict(_title, padding_type, trunc_type ,max_length) 
      _link=_json['link']
      #_label= x 
      if _authors and _title and _link and request.method=='POST':
        sql=("INSERT INTO data_jurnal (authors,title,link,label) VALUES (%s,%s,%s,%s)")
        data=(_authors, _title, _link,'')
        connection=mysql.connect()
        cursor=connection.cursor()
        cursor.execute(sql,data)
        connection.commit()
        #connection=mysql.connect()
        #cursor=connection.cursor()
        #cursor.execute("SELECT * from data_jurnal WHERE title=%s", _title)
        _label = Prediction.predict(_title, padding_type, trunc_type ,max_length)
        #connection=mysql.connect()
        #cursor=connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("UPDATE data_jurnal SET label=%s WHERE link=%s", (_label, _link))
        connection.commit()
        cursor.close()
        connection.close()

        response=jsonify('Jurnal berhasil ditambahkan')
        response.status_code=200
        #cursor.close()
        #connection.close()
      else:
        response=jsonify('belum berhasil')
        response.status_code=400

    except Exception as e:
        print(e)
        response=jsonify('belum berhasil')
    finally:
        return response
           
if __name__ == "__main__":
    app.run(debug=False)