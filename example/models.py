# -*- coding: utf-8 -*-
import os
import re
import threading
from datetime import datetime
from gevent.event import Event
from subprocess import Popen, PIPE

from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User

from example.builders import Registry

got_build_output = Event()
build_started = Event()
build_finished = Event()

class GitBuilder(Registry):
    name = 'Git Builder'
    scheme = 'git://'

class Project(models.Model):
    name = models.CharField(max_length=100)
    backend = models.CharField(
        max_length=100,
        choices=Registry.as_choices()
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_changed = models.DateTimeField(null=True, blank=True)
    build_command = models.TextField()

class Build(models.Model):
    project = models.ForeignKey(Project)
    phase = models.CharField(max_length=1, choices=(
        ('Never Ran', '0'),
        ('Fetching', '1'),
        ('Building', '2'),
        ('Finished', '3'),
    ))

    succeeded = models.BooleanField(default=True)
    started_by = models.ForeignKey(User, null=True, blank=True)

    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    log = models.TextField(null=True, blank=True)

    def start(self):
        self.phase = '2'
        self.started_at = datetime.now()
        self.save()
        command = re.sub('\s+', ' ', self.project.build_command).strip()
        arguments = command.split()

        process = Popen(
            arguments,
            stdout=PIPE,
            stderr=PIPE,
            shell=True
        )
        build_started.set()
        build_started.clear()
        StdOutReader(self, process).start()
        self.save()

    def as_key(self):
        return "build#{0}".format(self.id)

    @classmethod
    def get_fresh_log(cls, id):
        b = cls()
        b.id = id
        key = b.as_key()
        return cache.get(key)

class StdOutReader(threading.Thread):
    def __init__(self, build, process):
        self.build = build
        self.process = process
        self.cache_key = build.as_key()
        super(StdOutReader, self).__init__()

    def run(self):
        for _line in self.process.stdout.readlines():
            line = _line + os.linesep
            last = cache.get(self.cache_key)
            if last is None:
                last = line
            else:
                last = last + line

            cache.set(self.cache_key, last)
            got_build_output.set()
            got_build_output.clear()

        self.build.succeeded = (self.process.wait() == 0)
        self.build.phase = '3'
        self.build.finished_at = datetime.now()
        self.build.log = cache.get(self.cache_key)
        self.build.save()

        build_finished.set()
        build_finished.clear()

