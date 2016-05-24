#coding:utf-8
from flask import Flask,render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

bootstrap=Bootstrap()
moment=Moment()
db=SQLAlchemy()

def create_app(config_name):
	app=Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
#初始化
	bootstrap.init_app(app)
	moment.init_app(app)
	db.init_app(app)
#导入蓝图	
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/path')

	return app 
    	
    



  
	


