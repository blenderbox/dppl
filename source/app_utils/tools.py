from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json


def render_response(request, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)


def render_json(context):
    """ This is a shortcut to a JSON response.

    Args:
        context: A context dictionary that will be converted into JSON

    Returns:
        An HttpResponse with JSON
    """
    return HttpResponse(json.dumps(context), mimetype="application/json")
