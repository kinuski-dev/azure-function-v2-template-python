import json
import azure.functions as func

blueprint_func_1_method_2 = func.Blueprint()
@blueprint_func_1_method_2.function_name(name='func_1_method_2')
@blueprint_func_1_method_2.route(
    route='func_1/method_2', methods=['GET']
)

def func_1_method_2(req: func.HttpRequest) -> func.HttpResponse:
    resp = {"func_1": "method_2"}

    return func.HttpResponse(
        body=json.dumps(resp),
        status_code=200,
        mimetype="application/json"
    )
