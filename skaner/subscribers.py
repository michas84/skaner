""" pyramid event subscribers """

import logging
logger = logging.getLogger(__name__)
from pyramid.renderers import get_renderer
from pyramid.events import (
    BeforeRender,
    subscriber,
    )

@subscriber(BeforeRender)
def add_base_template(event):
    """ add base template macros for use in views """
    base = get_renderer('templates/layout.pt').implementation()
    skaner = get_renderer('templates/skaner.pt').implementation()
    event.update({'skaner' : skaner,
                  'base': base,})
