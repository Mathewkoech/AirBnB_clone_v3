#!/usr/bin/python3
"""
routes/ CRUD operations for handling city objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """
    retrieves all city objects from state
    :return: json of all cities in state or 404
    """
    city_list = []
    state_obj = storage.get("State", state_id)
    for obj in states_obj.values():
        city_list.append(obj.to_json())

    return jsonify(city_list)


@app_views.route("/states/<stae_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """
    create city route
    :return: newly created state obj
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("State", str(state_id)):
        abort(404)
    if "name" not in city_json:
        abort(400, 'Missing name')

    new_city = City(**city_json)
    new_city.save()
    respond = jsonify(new_city.to_json())
    respond.status_code = 201

    return respond


@app_views.route("/cities/city_id>",  methods=["GET"], strict_slashes=False)
def city_by_id(city_id):
    """
    gets a specific city object by ID
    :param city_id: city object id
    :return: city obj with the specified id or error
    """

    get_obj = storage.get("City", str(city_id))

    if get_obj is None:
        abort(404)

    return jsonify(get_obj.to_json())


@app_views.route("/cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    updates specific City object by ID
    :param city_id: city object ID
    :return: city object and 200 on success, or 400 or 404 on failure
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    get_obj = storage.get("City", str(city_id))
    if get_obj is None:
        abort(404)
    for key, val in city_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(get_obj, key, val)
    get_obj.save()
    return jsonify(get_obj.to_json())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """
    deletes city by id
    :param city_id: city object id
    :return: empty dict with 200 or 404 if not found
    """
    # fetch passed object
    get_obj = storage.get("City", str(city_id))

    if get_obj is None:
        abort(404)

    storage.delete(get_obj)
    storage.save()

    return jsonify({})
