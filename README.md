# Introduction 
The repository is a simple template for an Azure Function App-based API implementation with two functions and two methods for each function.

The purpose is to have an easy-to-use API routing starter pack. Copy-paste the template to a new Azure Function app or use it as a model.

# Project and Repository Sctructure
    ├── functions            - root folder for the functions and their methods
        ├── func_1           - function 1 folder
            ├── _commons.py  - shared classes, functions, definitions
            ├── method_1.py  - method 1 implementation
            ├── method_2.py  - method 2 implementation
        ├── func_2           - function 2 folder
            ├── _commons.py  - shared classes, functions, definitions
            ├── method_1.py  - method 1 implementation
            ├── method_2.py  - method 2 implementation
    ├── tests                - tests (not included in the template)
    ├── function_app.py      - functions & methods registry
    ├── host.json            - Function app coniguration options
    ├── local.settings.json  - app settings and connection strings for local execution
    ├── README.md            - this readme file
    ├── requirements.txt     - Azure Functions prerequisites

# Azure Function Routing
    ├── /api/func_1          - function 1
        ├── /method_1        - method 1
        ├── /method_2        - method 2
    ├── /api/func2          - function 2
        ├── /method_1        - method 1
        ├── /method_2        - method 2

For example,  
func_1_method_1: [GET] http://localhost:7071/api/func_1/method_1  
func_1_method_2: [GET] http://localhost:7071/api/func_1/method_2  
func_2_method_1: [GET] http://localhost:7071/api/func_2/method_1  
func_2_method_2: [GET] http://localhost:7071/api/func_2/method_2  

## Unique method function names
NB! The names for functions implemented in the `method_N.py` files and published in the `function_app.py` must be unique across the entire Function service app.

Although the routing may look like `/func_1/method_1` and `/func_2/method_1`, the function defition must be like `def func_1_method_1():` and `def func_2_method_1():`. Defining both functions as `def method_1():` will cause a binding error.

# Local development and debugging
## Environment
- Create new virtual environment: `\python\python310\python -m venv .venv`, assuming that Python 3.10 is installed to Windows' C:\python\python310
- Upgrade pip: `.venv\Scripts\python.exe -m pip install --upgrade pip`
- Install packages in requirememts.txt: `.venv\Scripts\python -m pip install -r requirements.txt`
- Activate virtual environment (venv): `.venv\Scripts\activate`

## Run locally
- Start function locally for debugging: `func start --python`
- The function listens at `http://localhost:7071/api/<routing>`
- Stop local debugging: hit `Ctrl+C`

## Errors and Warnings
**Error:**

*Microsoft.Azure.WebJobs.Extensions.Http: Could not load file or assembly 'System.Net.Http.Formatting, Version=5.2.8.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35'. The system cannot find the file specified. Value cannot be null. (Parameter 'provider')*

**Solution**:
- install/reinstall/update ASP.NET Core x64 6.0.26
- install/reinstall/update Azure Functions Core Tools x64 4.0.5455

---

**Warning** in local debug mode:

*Customer packages not in sys path. This should never happen!*

**Solution:** Can be safely ignored

# Useful resources
- [Azure Functions V2 Python developer guide](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Develop Azure Functions locally using Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
