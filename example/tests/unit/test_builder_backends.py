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
from sure import that
from example.builders import Registry

def test_backend_registry_find_definitions():
    "creating builders should be as easy as declaring classes"
    assert that(Registry.total()).equals(0)

    class Builder1(Registry):
        name = 'First'
        scheme = 'builder1://'

    assert that(Registry.total()).equals(1)
    assert that(Registry.get('builder1://')).equals(Builder1)

def test_the_backend_registry_should_be_easy_to_erase():
    u"the backend registry should be easy to erase"

    class Builder2(Registry):
        name = 'Second'
        scheme = 'builder2://'

    assert Registry.total() >= 1, \
        'there should have one or more builders defined on the registry'

    Registry.clear()

    assert that(Registry.total()).equals(0)

def test_object_should_do_something():
    u"Registry should be represented as choices for ChoiceFields"
    assert that("this").equals("this")

    class Builder1(Registry):
        name = 'Git Builder'
        scheme = 'builder1://'

    class Builder2(Registry):
        name = 'Mercurial Builder'
        scheme = 'builder2://'

    assert that(Registry.as_choices()).equals((
        ('Git Builder', 'builder1://'),
        ('Mercurial Builder', 'builder2://'),
    ))

def test_defining_a_scheme_to_a_builder_should_be_obligatory():
    u"defining a scheme to a Builder should be obligatory"

    def defining_without_scheme():
        class SomeBuilder(Registry):
            scheme = "asd://"

    def defining_with_scheme_nonstring():
        class SomeBuilderElse(Registry):
            scheme = 123
            scheme = "asd://"

    assert that(defining_without_scheme).raises('The builder "SomeBuilder" does not define a "scheme" attribute.')
    assert that(defining_with_scheme_nonstring).raises('The attribute "scheme" of builder "SomeBuilderElse" must be a string.')

def test_defining_a_scheme_to_a_builder_should_be_obligatory():
    u"defining a scheme to a Builder should be obligatory"

    def defining_without_scheme():
        class SomeBuilder(Registry):
            name = "Another"

    def defining_with_scheme_nonstring():
        class SomeBuilderElse(Registry):
            name = "Yet Another"
            scheme = 123

    assert that(defining_without_scheme).raises('The builder "SomeBuilder" does not define a "scheme" attribute.')
    assert that(defining_with_scheme_nonstring).raises('The attribute "scheme" of builder "SomeBuilderElse" must be a string.')
