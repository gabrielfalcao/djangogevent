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
from django.http import HttpResponse
from django.views.generic.base import TemplateView, View
from example.models import Project, Build, got_build_output
from django.utils import simplejson

class Index(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['builds'] = Build.objects.order_by('-id')
        return context

class JsonView(View):
    def render_json(self, dictionary):
        data = simplejson.dumps(dictionary)
        return HttpResponse(data, mimetype='text/json')

class NewBuild(JsonView):
    def post(self, request, *args, **kw):
        p, created = Project.objects.get_or_create(
            name=request.POST['name'],
            backend='git://',
            build_command=request.POST['command']
        )
        b = Build.objects.create(
            project=p
        )
        b.start()

        return self.render_json({
            'build': b.id
        })

class PushBuild(JsonView):
    def get(self, request, id):
        got_build_output.wait()
        return self.render_json({'log': Build.get_fresh_log(id)})
