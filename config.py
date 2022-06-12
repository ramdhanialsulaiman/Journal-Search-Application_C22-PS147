from app import app
from flaskext.mysql import MySQL

mysql=MySQL()
app.config['MYSQL_DATABASE_USER']=''
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']=''
app.config['MYSQL_DATABASE_HOST']=''

#app.config['MYSQL_DATABASE_USER']='root'
#app.config['MYSQL_DATABASE_PASSWORD']=''
#app.config['MYSQL_DATABASE_DB']='dbjurnal'
#app.config['MYSQL_DATABASE_HOST']='localhost'

mysql.init_app(app)