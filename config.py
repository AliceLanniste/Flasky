#coding:utf-8
import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY='hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN=True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	FLASKY_MAIL_SUBJECT_PREFIX='[flasky]'
	FLASKY_MAIL_SENDER='Flasky <lannistepen@163.com>'
	FLASKY_ADMIN=''

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG=True
	SQLALCHEMY_DATABASE_URI=\
	    'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')


    

class TestingConfig(Config):
	TESTING=True
	SQLALCHEMY_DATABASE_URI=\
	    'sqlite:///'+os.path.join(basedir,'data-test.sqlite')


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI=\
	    'sqlite:///'+os.path.join(basedir,'data.sqlite')

config={
	'development':DevelopmentConfig,
	'testing':TestingConfig,
	'production':ProductionConfig,

	'default':DevelopmentConfig
}	



