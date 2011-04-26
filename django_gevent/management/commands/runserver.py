# -*- coding: utf-8 -*-
# <django_gevent - django tool set to work with gevent>
# Copyright (C) <2011>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from gevent import monkey
from gevent import __version__ as gevent_version
from gevent.wsgi import WSGIServer

monkey.patch_all()

import os
import sys

from django.core.management.commands import runserver
from optparse import make_option

original_run = runserver.run

def run_with_gevent(addr, port, wsgi_handler, *args, **kw):
    address = (addr, int(port))

    print 'GEvent %s is enabled' % gevent_version
    WSGIServer(address, wsgi_handler).serve_forever()

class Command(runserver.Command):
    option_list = runserver.Command.option_list + (
        make_option('--no-gevent', '-G',
                    action='store_true',
                    dest='no_gevent',
                    default=False,
                    help='runs the server without GEvent support'),
    )

    def handle(self, *args, **options):
        gevent_enabled = not options['no_gevent']
        if gevent_enabled:
            runserver.run = run_with_gevent
        else:
            runserver.run = original_run

        super(Command, self).handle(*args, **options)
