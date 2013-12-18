from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSESSION = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
BASE = declarative_base()


class Product(BASE):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    code = Column(Text, unique=True)
    vat = Column(Integer)

    def __init__(self, name, code, vat):
        self.name = name
        self.code = code
        self.vat = vat

    @classmethod
    def create(cls, product):
        DBSESSION.add(product)

    @classmethod
    def get_all(cls):
        return DBSESSION.query(Product).all()

    @classmethod
    def product_exists(cls, code):
        if DBSESSION.query(Product).filter(Product.code == code).all():
            return True
        else:
            return False

    @classmethod
    def find_by_code(cls, code):
        return DBSESSION.query(Product).filter(Product.code == code).first()

    @classmethod
    def delete(cls, code):
        DBSESSION.delete(DBSESSION.query(Product).filter(Product.code == code).first())

    @classmethod
    def edit(cls, code):
        pass

