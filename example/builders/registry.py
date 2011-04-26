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
import os
import re
_registry = []

class BuilderSyntaxError(Exception):
    attr_missing = 'The builder "{0}" does not define a "{1}" attribute.'
    attr_nonstring = 'The attribute "{1}" of builder "{0}" must be a string.'

class RegistryMeta(type):
    def __init__(cls, name, bases, attrs):
        super(RegistryMeta, cls).__init__(name, bases, attrs)
        if name != 'Registry':
            for attrname in ('name', 'scheme'):
                if attrname not in attrs:
                    msg = BuilderSyntaxError.attr_missing.format(name, attrname)
                    raise BuilderSyntaxError(msg)
            if not isinstance(attrs[attrname], basestring):
                msg = BuilderSyntaxError.attr_nonstring.format(name, attrname)
                raise BuilderSyntaxError(msg)

            _registry.append((attrs['scheme'], cls))


class Registry(object):
    source = _registry
    __metaclass__ = RegistryMeta

    @classmethod
    def total(cls):
        return len(cls.source)

    @classmethod
    def get(cls, name, fallback=None):
        return dict(cls.source).get(name, fallback)

    @classmethod
    def clear(cls):
        while cls.source:
            cls.source.pop()

    @classmethod
    def as_choices(cls):
        choices = []
        for scheme, child in cls.source:
            choices.append((child.name, scheme))

        return choices
