import json
import azure.functions as func

blueprint_func_1_method_1 = func.Blueprint()
@blueprint_func_1_method_1.function_name(name='func_1_method_1')
@blueprint_func_1_method_1.route(
    route='func_1/method_1', methods=['GET']
)

def func_1_method_1(req: func.HttpRequest) -> func.HttpResponse:
    resp = {"func_1": "method_1"}

    return func.HttpResponse(
        body=json.dumps(resp),
        status_code=200,
        mimetype="application/json"
    )
