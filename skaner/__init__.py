from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from skaner.models import (
    DBSESSION,
    BASE,
    )

from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from skaner.security import security_callback

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    session_factory = UnencryptedCookieSessionFactoryConfig('skanersessionsecret', timeout=3600)
    authn_policy = AuthTktAuthenticationPolicy(
        'skanerauthnsecret', callback=security_callback)
    authz_policy = ACLAuthorizationPolicy()

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSESSION.configure(bind=engine)
    BASE.metadata.bind = engine
    config = Configurator(settings=settings,
                          session_factory = session_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('scan', '/scan')
    config.add_route('list_products', '/lista')
    config.add_route('add_product', '/dodaj')
    config.add_route('add_product\'', '/dodaj/{code}')
#    config.add_route('add_product_with_code\'', '/dodaj/{code}')
    config.add_route('export_database', '/export')
    config.add_route('edit_product\'', '/edycja/{code}')
    config.add_route('delete_product\'', '/usun/{code}')
    config.scan()
    return config.make_wsgi_app()
