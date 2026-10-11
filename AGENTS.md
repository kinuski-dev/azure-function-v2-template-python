# AGENTS.md

NEVER MAKE ANY CHANGES TO THIS FILE. You may suggest changes, but they always require a manual approval.

This file guides AI agents working in this repository. This file doesn't fully replace the [README.md](README.md).

## What this repository is

A starter template for an HTTP API built on the **Azure Functions Python v2 programming model** (decorators and blueprints, no `function.json`). It has two "functions" (`func_1`, `func_2`), each with two "methods" (`method_1`, `method_2`). Each method is its own Azure Function, exposed at `/api/<func>/<method>`. People copy the template into a new Function App and replace the placeholder handlers. It is possible to create a new Azure Functions repository using the template - all code will be copied automatically.

Targets Python 3.13, `azure-functions>=2.3.0`, the Linux Function App and extension bundle `[4.*, 5.0.0)`.

## Layout

```text
function_app.py                      # creates the FunctionApp and registers every blueprint
functions/<func_N>/method_N.py       # one blueprint + one HTTP handler per file
host.json                            # runtime config (extension bundle, App Insights sampling)
local.settings.json                  # local-only app settings (committed on purpose, no secrets)
requirements.txt                     # azure-functions only; never add azure-functions-worker
azfunc_deployment_pipeline_azdo.yaml # Azure DevOps CI/CD: DEV stage, then PROD stage
tests/                               # sample tests
```

`functions/` and its subfolders have no `__init__.py`; Python imports them as namespace packages.

## How a method is wired

Every `method_N.py` follows the same pattern:

```python
blueprint_func_1_method_1 = func.Blueprint()
@blueprint_func_1_method_1.function_name(name="func_1_method_1")
@blueprint_func_1_method_1.route(route="func_1/method_1", methods=['GET', 'POST'])

def func_1_method_1(req: func.HttpRequest) -> func.HttpResponse:
    ...
    return func.HttpResponse(body=json.dumps(resp), status_code=200, mimetype="application/json")
```

`function_app.py` then imports the blueprint and calls `app.register_functions(...)`.

### Adding a method or function

1. Create `functions/<func_X>/<method_Y>.py` by copying an existing method file.
2. Rename consistently to `blueprint_<func_X>_<method_Y>`, `function_name(name="<func_X>_<method_Y>")`, `route="<func_X>/<method_Y>"` and `def <func_X>_<method_Y>(...)`.
3. Import and register the blueprint in `function_app.py`.
4. Update the structure and routing sections in `README.md`.

**Function names must be unique across the whole app.** Two handlers both named `method_1` or both registered as `function_name("method_1")` cause a binding error at startup, even when their routes differ.

## Conventions

- Handlers return JSON through `func.HttpResponse(..., mimetype="application/json")` built with `json.dumps`.
- POST handlers read the body with `req.get_json()` and return `400` with `{"error": ...}` when it raises `ValueError`. See `functions/func_1/method_1.py`.
- `http_auth_level` is set once in `function_app.py`. It is currently `ANONYMOUS`; `FUNCTION` is left commented out next to it.
- Keep the blank line between the decorators and `def`, and the quoting style, consistent with the surrounding files.
- Only add third-party packages to `requirements.txt`, not standard library modules.

## Local development (Windows)

```powershell
\python\python313\python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\activate
func start --python          # http://localhost:7071/api/<func>/<method>
```

- `func start` needs Azure Functions Core Tools v4
- `func start` may need a local storage emulator, if `AzureWebJobsStorage` is `UseDevelopmentStorage=true`. Use Azurite or the legacy Azure Storage Emulator. This template does not need a local storage emulator; the reference is included in the README.md file for people's convenience.
- To check a handler without the Functions host, build the blueprint and call the user function directly:

  ```python
  fn = blueprint_func_1_method_1._function_builders[0].build()
  resp = fn.get_user_function()(func.HttpRequest(method="POST", url="/api/func_1/method_1", body=b'{"a": 1}'))
  ```

## CI/CD

`azfunc_deployment_pipeline_azdo.yaml` runs on every commit to `main`:

- **deployDev** sets up Python 3.13 and installs `requirements.txt` into `./.python_packages/lib/site-packages`. That exact path is required, otherwise the deployed app silently has no packages. The stage then zips the working directory, publishes it as artifact `AzFunc` and zip-deploys it to `azfunc-my-v2-function-dev`.
- **deployProd** depends on `deployDev` succeeding. It downloads the same artifact and deploys it to `azfunc-my-v2-function-prod`. `deployToProd` defaults to `true` and there's no approval gate, so a successful DEV deploy goes straight on to PROD.

Subscription names and app names in the pipeline are placeholders.

When changing the Python version, keep `UsePythonVersion` `versionSpec`, both `runtimeStack: 'PYTHON|x.y'` values and the README venv instructions in step.
