# This is all of the views that the Microbug application supports

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import logging
import json
import settings
import sys
from compiled_version_store import CompiledVersionStore
from primary_version_store import PrimaryVersionStore
from pending_version_store import PendingVersionStore
from microbug.models import Program, Version
import re
from django.template.defaultfilters import slugify

# Get a version store we can keep uploaded files in.
compiled_version_store = CompiledVersionStore(settings.COMPILED_PYTHON_PROGRAMS_DIRECTORY)
primary_version_store = PrimaryVersionStore(settings.PRIMARY_STORE_DIRECTORY)
pending_queue_store = PendingVersionStore(settings.PENDING_PYTHON_QUEUE_DIRECTORY)

# Get the logger for these views
logger = logging.getLogger(__name__)

# The main page
def index(request):
    return render(request, 'microbug/index.html', {})

# Create a new program
def create_program(request):
    return render(request, 'microbug/create_program.html', {'programs': programs})

# View a single program
def program(request, program_id):
    viewed_program = get_object_or_404(Program, pk=program_id)
    return render(request, 'microbug/program.html', {'program': viewed_program})

# List all of the Programs available on the system
def programs(request):
    programs = Program.objects.all()
    return render(request, 'microbug/programs.html', {'programs': programs})

# Show the tutorials
def tutorial(request, tutorial_name, page_number=1):
    return render(request, 'microbug/tutorial_multiple_toolboxes.html', {})

# Downloads a compiled .hex program
def download(request, program_id, program_name=None):
    program = get_object_or_404(Program, pk=program_id)

    # Program name defaults to the name in the DB.
    if program_name is None:
        program_name = program.name

    # Obtain the data from the compiled store, if it's not there then return a HTTP
    # error
    content = compiled_version_store.hex(program.version.base_filename())
    if content is None:
        return HttpResponseNotFound("No compiled version found")

    response = HttpResponse(content, content_type='application/octet-stream')
    saved_filename = "%s.hex" % slugify(program_name)
    logger.debug("Saving as '{0}'".format(saved_filename))

    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(saved_filename)

    return response
##########################################

# Called when the user clicks the 'build_code' button in the editor.
@csrf_exempt
def build_code(request):
    # Check we're a POST request
    if request.method != 'POST':
        return HttpResponseBadRequest('Must be a POST request')

    # Grab the JSON from the request body and make it nicer
    try:
        json_obj = json.loads(request.body)
    except ValueError:
        logger.error("Build_code could not process Json: %s" % str(request))
        return HttpResponseBadRequest("Could not process request, not a valid Json object?")

    # Reserve the ID for the primary store
    (numeric_id, random_uuid) = primary_version_store.reserve_new_id()

    # Count the number of lines of code
    python_code = json_obj['repr']['code']
    lines_of_code = _count_lines(python_code)

    # Pull out program details from request
    program_name = json_obj['program_name']
    program_id = json_obj['program_id']

    # Check if we've been provided with a Program ID, if so find the program now so we can
    # maintain the version links
    new_program = None
    if program_id:
        new_program = get_object_or_404(Program, pk=program_id)

    # Write the new Version to the database
    version = Version(id=numeric_id, store_uuid=random_uuid, lines_of_code_count=lines_of_code)
    if new_program:
        version.previous_version = new_program.version
        json_obj['previous_version'] = new_program.version
    version.save()

    # If we didn't obtain a Program from the ID we'll create one now, if we did we'll update it
    # to point to new version
    if new_program:
        new_program.version = version
        new_program.name = program_name
    else:
        new_program = Program(version=version, name=program_name)
    new_program.save()

    # Add the program details to the JSON
    json_obj['program_id'] = new_program.id

    # Write it to both of the stores
    pretty_json = _prettify_json(json_obj)
    primary_version_store.write_new_version(pretty_json, numeric_id, random_uuid)
    pending_queue_store.write_new_version(python_code, numeric_id, random_uuid)

    # Return the program's ID
    return HttpResponse(str(new_program.id))

# Rename a program at the user's request
@csrf_exempt
def rename_program(request):
    # Check we're a POST request
    if request.method != 'POST':
        return HttpResponseBadRequest('Must be a POST request')

    # Grab the JSON from the request body and make it nicer
    try:
        json_obj = json.loads(request.body)
    except ValueError:
        logger.error("Rename_Program could not process Json: %s" % str(request))
        return HttpResponseBadRequest("Could not process request, not a valid Json object?")

    # Perform the actual rename
    target_program = get_object_or_404(Program, pk=json_obj['program_id'])
    target_program.name = json_obj['program_name']
    target_program.save()

    return HttpResponse('Renamed successfully')

# Convert JSON to a prettified version
def _prettify_json(json_obj):
    return json.dumps(json_obj, sort_keys=True, indent=4, separators=(',', ': '))

# Counts the number of lines in a piece of text
def _count_lines(text):
    return len(re.split('[\n\r]+', text))-1
