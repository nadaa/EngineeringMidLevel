from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123@localhost/featuresdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)


class Clients(db.Model):
	__tablename__='clients'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(50),nullable=False,unique=True)
	email=db.Column(db.String(100),unique=True)
	features=db.relationship('Features',backref='client')  

	def __init__(self,name, email):
	    self.name = name
	    self.email = email

class Products(db.Model):
	__tablename__='products'
	id=db.Column(db.Integer,primary_key=True)
	area=db.Column(db.String(50),unique=True,nullable=False)

	features=db.relationship('Features',backref='product')

	def __init__(self,area):
		self.area=area

class Features(db.Model):
	__tablename__='features'
	id= db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(100),nullable=False)
	desc=db.Column(db.String(1000))
	client_priority=db.Column(db.Integer,unique=True,nullable=False )
	target_dat=db.Column(db.DateTime,nullable=False)
	client_id=db.Column(db.Integer,db.ForeignKey('clients.id'))
	product_id=db.Column(db.Integer,db.ForeignKey('products.id'))

	def __init__(self,title,desc,client_priority,target_dat,client_id,product_id):
		self.title=title
		self.desc=desc
		self.client_priority=client_priority
		self.target_dat=target_dat
		self.client_id=client_id
		self.product_id=product_id


@app.route('/')
def home():
	return 'Home page'


@app.route('/clients',methods=['GET','POST'])
def clients():

	if(request.method=='GET'):
		return 'clients list'
	else:
		try:
			name=request.get_json()['name']
			email=request.get_json()['email']
			c=Clients(name,email)
			db.session.add(c)
			db.session.commit()
		except:
			return 'duplicate'
		return "client added"


@app.route('/products',methods=['GET','POST'])
def products():
	if(request.method=='GET'):
		return 'product area list'
	else:
		try:
			area=request.get_json()['area']
			p_area=Products(area)
			db.session.add(p_area)
			db.session.commit()
		except:
			return "duplicate"
		
		return 'product area was added'

# post a new feature
@app.route('/newfeature',methods=['POST'])
def addNewFeature():
	# read all feature properties 
	title=request.get_json()['title']
	desc=request.get_json()['desc']
	client_priority=request.get_json()['client_priority']
	target_date=request.get_json()['target_date']
	client_id=request.get_json()['client_id']
	product_id=request.get_json()['product_id']

	#create a new feature
	newFeature=Features(title,desc,client_priority,target_date,client_id,product_id)
	db.session.add(newfeature)
	db.commit()
	return 'new feature added'
	

# to display all features of a given client ( in order based on the priority)
@app.route('/features/<client>',methods=['GET'])
def getFeatures(client):
	# select * from features f  join clients c on c.id=f.client_id where c.name=client
	return 'get features based on a given client'


if(__name__=='__main__'):
	db.create_all()
	app.run(debug=True)