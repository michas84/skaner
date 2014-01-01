#encoding:utf8

#from pyramid.response import Response
from pyramid.view import view_config
from pyramid.response import Response

from skaner.models import (
#    DBSESSION,
    Product,
    )

from pyramid.httpexceptions import (
    HTTPFound,
)
import transaction
import csv
import cStringIO

@view_config(route_name='home', renderer='templates/welcome.pt')
def home(request):
    return {}

@view_config(route_name='list_products', renderer='templates/list.pt')
def list(request):
    theList = Product.get_all()
    return {'theList': theList}

@view_config(route_name='scan', renderer='templates/scan.pt')
def scan(request):
    code = None
    if 'scan' in request.params:
        code = request.params['code']
        if Product.product_exists(code):
            #return redirect to edit?
            redirect = HTTPFound(location = request.route_url('edit_product\'', code=code))
        else:
            #add?
            request.session['code'] = code
            redirect = HTTPFound(location = request.route_url('add_product\'', code=code))

        return redirect

    return {}

#TODO
@view_config(route_name='add_product', renderer='templates/add.pt')
@view_config(route_name='add_product\'', renderer='templates/add.pt')
def add(request):

    name = None
    vat = None
    if 'code' in request.session and request.session['code'] != None:
        code = request.session['code']
        request.session['code'] = None
    else:
        code = None

    if 'add' in request.params:
        code = request.params['code']
        name = request.params['name']
        vat = request.params['vat']
        product = Product(name, code, vat)
        try:
            Product.create(product)
            transaction.commit()
            redirect = HTTPFound(location = request.route_url('list_products'))
            return redirect
        except Exception as e:
            transaction.abort()
            request.session.flash("Błąd przy zapisywaniu. {0}".format(e).decode('utf-8'), 'message')
            return {'result': 'fail'}

    return {'name': name, 'code': code, 'vat': vat}

@view_config(route_name='edit_product\'', renderer='templates/add.pt')
def edit(request):
    pass

@view_config(route_name='delete_product\'')
def delete(request):
    code = request.matchdict['code']
    Product.delete(code)
    request.session.flash("Produkt z kodem kreskowym {0} skasowany.".format(code))
    redirect = HTTPFound(location = request.route_url('list_products'))
    return redirect

@view_config(route_name='export_database')
def export_database(request):
    products = Product.get_all()
    output = cStringIO.StringIO()
    writer = csv.writer(output, dialect=csv.excel)

    for product in products:
        writer.writerow([
        product.name,
        product.code,
        product.vat])

    response = Response(body=output.getvalue(),
                        content_type='text/csv',
                        content_disposition='attachment; filename=kody.csv',
                        charset='utf8')
    return response


