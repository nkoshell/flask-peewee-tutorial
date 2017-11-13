import copy

from flask import abort, request
from flask.views import MethodView
from peewee import Model
from playhouse.shortcuts import model_to_dict

from backend.utils import json_response


class BaseModelView(MethodView):
    _model = None

    def __init__(self, model=None):
        self.check_model(model)
        self._model = model

    @property
    def model(self):
        return self._model

    @property
    def model_meta(self):
        return self.get_model_meta(self.model)

    @staticmethod
    def check_model(model):
        if not issubclass(model, Model):
            raise ValueError('Arg `model` must be `peewee.Model` subclass, got %r' % model)
        return model

    @staticmethod
    def get_model_meta(model):
        return copy.copy(model._meta)

    @classmethod
    def get_url_rules(cls, model, endpoint=None, url=None, pk='instance_id', pk_type='int',
                      *cls_args, **cls_kwargs):
        cls.check_model(model)
        if endpoint is None:
            model_meta = cls.get_model_meta(model)
            endpoint = model_meta.name
        if url is None:
            url = '/%s/' % endpoint

        single_resource_url = '%(url)s/<%(pk_type)s:%(pk)s>/' % dict(
            url=url.rstrip('/'),
            pk=pk,
            pk_type=pk_type
        )

        view_func = cls.as_view(endpoint, model=model, *cls_args, **cls_kwargs)

        # Ordering
        url_rules = [
            {'rule': url, 'view_func': view_func, 'defaults': {pk: None}, 'methods': ['GET', ]},
            {'rule': url.rstrip('/'), 'view_func': view_func, 'methods': ['POST', ]},
            {'rule': url, 'view_func': view_func, 'methods': ['POST', ]},
            {'rule': single_resource_url.rstrip('/'), 'view_func': view_func, 'methods': ['GET', 'PUT', 'DELETE', ]},
            {'rule': single_resource_url, 'view_func': view_func, 'methods': ['GET', 'PUT', 'DELETE', ]},
        ]
        return url_rules

    @classmethod
    def register(cls, app, model, *args, **kwargs):
        url_rules = cls.get_url_rules(model, *args, **kwargs)
        for url_rule in url_rules:
            app.add_url_rule(**url_rule)


class ApiModelView(BaseModelView):
    decorators = [
        json_response,
    ]

    def get(self, instance_id=None):
        if instance_id is not None:
            try:
                instance = self.model.get(self.model_meta.primary_key == instance_id)
            except self.model.DoesNotExist:
                abort(404, '%s with id=%r does not exist' % (self.model_meta.name, instance_id))
            else:
                return model_to_dict(instance)
        return self.list()

    def list(self):
        query = self.model.select()
        filters = self.get_filters()
        if filters:
            query = query.filter(**filters)
        instances = [model_to_dict(instance) for instance in query]
        return instances

    @staticmethod
    def get_filters():
        filters = {}
        for k, v in request.args.items():
            if '__' in k:
                if k.endswith('in'):
                    v = v.split(',')
                filters[k] = v
        return filters
