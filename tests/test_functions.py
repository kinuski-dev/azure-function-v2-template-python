"""
Tests for the sample functions, run against the registered FunctionApp in function_app.py
"""
import json
import azure.functions as func
import pytest
from function_app import app

# Function name -> (route, allowed HTTP methods), as documented in README.md
EXPECTED_FUNCTIONS = {
    "func_1_method_1": ("func_1/method_1", {"GET", "POST"}),
    "func_1_method_2": ("func_1/method_2", {"GET"}),
    "func_2_method_1": ("func_2/method_1", {"GET", "POST"}),
    "func_2_method_2": ("func_2/method_2", {"GET"}),
}

POST_FUNCTIONS = [name for name, (_, methods) in EXPECTED_FUNCTIONS.items() if "POST" in methods]

# app.get_functions() must be called only once: repeated calls raise a duplicate function name error
REGISTERED_FUNCTIONS = {f.get_function_name(): f for f in app.get_functions()}


def get_function(name):
    assert name in REGISTERED_FUNCTIONS, f"{name} is not registered in function_app.py"
    return REGISTERED_FUNCTIONS[name]


def call(name, method, body=b""):
    route, _ = EXPECTED_FUNCTIONS[name]
    req = func.HttpRequest(method=method, url=f"/api/{route}", body=body)
    return get_function(name).get_user_function()(req)


def expected_resp(name):
    # "func_1_method_1" -> {"func_1": "method_1"}
    func_part, method_part = name.rsplit("_method_", 1)
    return {func_part: f"method_{method_part}"}


def test_registered_functions_match_readme():
    assert sorted(REGISTERED_FUNCTIONS) == sorted(EXPECTED_FUNCTIONS)


@pytest.mark.parametrize("name", EXPECTED_FUNCTIONS)
def test_route_and_methods(name):
    route, methods = EXPECTED_FUNCTIONS[name]
    trigger = get_function(name).get_trigger()

    assert trigger.route == route
    assert {str(m.value) for m in trigger.methods} == methods


@pytest.mark.parametrize("name", EXPECTED_FUNCTIONS)
def test_get_returns_json(name):
    resp = call(name, "GET")

    assert resp.status_code == 200
    assert resp.mimetype == "application/json"
    assert json.loads(resp.get_body()) == expected_resp(name)


@pytest.mark.parametrize("name", POST_FUNCTIONS)
def test_post_echoes_json_body(name):
    body = {"a": 1, "b": ["x", "y"]}
    resp = call(name, "POST", json.dumps(body).encode())

    assert resp.status_code == 200
    assert resp.mimetype == "application/json"
    assert json.loads(resp.get_body()) == {**expected_resp(name), "body": body}


@pytest.mark.parametrize("name", POST_FUNCTIONS)
@pytest.mark.parametrize("body", [b"not json", b""])
def test_post_invalid_json_returns_400(name, body):
    resp = call(name, "POST", body)

    assert resp.status_code == 400
    assert resp.mimetype == "application/json"
    assert json.loads(resp.get_body()) == {"error": "Request body must be valid JSON"}
