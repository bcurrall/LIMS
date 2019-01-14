__author__ = "Ashok Ragavendran"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "ashok.ragavendran@gmail.com"
__maintainer__ = "Ashok Ragavendran"
__status__ = "Production"

from django.core.urlresolvers import reverse
from jinja2 import Environment


##from django.core.urls import reverse


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        ##'static': staticfiles_storage.url,
        ##'static': "file://Users/ashok//Documents/Research/CHGR/CSSForR/bootstrap-3.3.5-dist/css/bootstrap.min.cyborg.css",
        ##'static': "https://maxcdn.bootstrapcdn.com/bootswatch/3.3.7/slate/bootstrap.min.css",
        ##'static': "https://maxcdn.bootstrapcdn.com/bootswatch/3.3.7/cosmo/bootstrap.min.css",
        ##'static': "https://maxcdn.bootstrapcdn.com/bootswatch/3.3.7/yeti/bootstrap.min.css",
        ##'static': "https://maxcdn.bootstrapcdn.com/bootswatch/3.3.7/spacelab/bootstrap.min.css",
        ##'static': "https://maxcdn.bootstrapcdn.com/bootswatch/3.3.7/superhero/bootstrap.min.css",
        ##'static': "https://maxcdn.bootstrapcdn.com/bootswatch/3.3.7/flatly/bootstrap.min.css",
        ##'static': "https://maxcdn.bootstrapcdn.com/bootswatch/3.3.7/darkly/bootstrap.min.css",
        'static': "https://maxcdn.bootstrapcdn.com/bootswatch/3.3.7/cerulean/bootstrap.min.css",
        'url': reverse,
    })
    return env
