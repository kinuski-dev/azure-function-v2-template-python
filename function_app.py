import azure.functions as func
from functions.func_1.method_1 import blueprint_func_1_method_1
from functions.func_1.method_2 import blueprint_func_1_method_2
from functions.func_2.method_1 import blueprint_func_2_method_1
from functions.func_2.method_2 import blueprint_func_2_method_2

app = func.FunctionApp(
    # http_auth_level=func.AuthLevel.FUNCTION
    http_auth_level=func.AuthLevel.ANONYMOUS
)

app.register_functions(blueprint_func_1_method_1)
app.register_functions(blueprint_func_1_method_2)

app.register_functions(blueprint_func_2_method_1)
app.register_functions(blueprint_func_2_method_2)
