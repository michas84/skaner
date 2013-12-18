import logging
LOGGER = logging.getLogger(__name__)

def security_callback(userid, request):
    return userid
