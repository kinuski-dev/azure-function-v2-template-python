# Azure Function Template v.2 with Blueprints for Python

## Introduction

This repository is a simple template for an Azure Function App-based API with two functions and two methods per function.

It provides an easy-to-use starter pack with defined blueprints and API routing. Copy and paste the template into a new Azure Function app or use it as a model when creating a new repository.

## Project and Repository Structure

```text
    ├── functions            - root folder for the functions and their methods
        ├── func_1           - function 1 folder
            ├── _commons.py  - shared classes, functions, definitions
            ├── method_1.py  - method 1 implementation
            ├── method_2.py  - method 2 implementation
        ├── func_2           - function 2 folder
            ├── _commons.py  - shared classes, functions, definitions
            ├── method_1.py  - method 1 implementation
            ├── method_2.py  - method 2 implementation
    ├── tests                - sample tests
    ├── function_app.py      - functions & methods registry
    ├── host.json            - Function app configuration options
    ├── local.settings.json  - app settings and connection strings for local execution
    ├── README.md            - this README file
    ├── requirements.txt     - Azure Functions prerequisites
    ├── AGENTS.md            - guidance for Agents
    ├── CLAUDE.md            - guidance for Claude; refers to AGENTS.md
```

## Azure Function Routing

```text
    ├── /api/func_1          - function 1
        ├── /method_1        - method 1
        ├── /method_2        - method 2
    ├── /api/func_2          - function 2
        ├── /method_1        - method 1
        ├── /method_2        - method 2
```

For example,  
func_1_method_1: [GET, POST] - http://localhost:7071/api/func_1/method_1  
func_1_method_2: [GET]       - http://localhost:7071/api/func_1/method_2  
func_2_method_1: [GET, POST] - http://localhost:7071/api/func_2/method_1  
func_2_method_2: [GET]       - http://localhost:7071/api/func_2/method_2  

### Unique method function names

NB! The names for functions implemented in the `method_N.py` files and published in the `function_app.py` must be unique across the entire Function service app.

Although the routing may look like `/func_1/method_1` and `/func_2/method_1`, the function definition must be like `def func_1_method_1():` and `def func_2_method_1():`. Defining both functions as `def method_1():` will cause a binding error.

## Local development and debugging

### AGENTS.md content

The AGENTS.md content describes this template. After you create an Azure Function using this template, you'll need to edit the file to match your application requirements.

### Virtual environment (venv)

- Create a new virtual environment: `py -3.14 -m venv .venv`
- Upgrade pip: `.venv\Scripts\python.exe -m pip install --upgrade pip`
- Install packages in requirements.txt: `.venv\Scripts\python -m pip install -r requirements.txt`
- Activate virtual environment (venv): `.venv\Scripts\activate`
- Deactivate virtual environment (venv): `deactivate`

### Azure Storage Emulator

CRON and diagnostics events stored locally require running the Storage Emulator. On Windows, the Storage Emulator is usually found at `C:\Program Files (x86)\Microsoft SDKs\Azure\Storage Emulator`. The Config file `AzureStorageEmulator.exe.config` defines Storage Service listeners as follows.

```xml
  <StorageEmulatorConfig>
    <services>
      <service name="Blob"  url="http://127.0.0.1:10000/"/>
      <service name="Queue" url="http://127.0.0.1:10001/"/>
      <service name="Table" url="http://127.0.0.1:10002/"/>
    </services>
    [...]
  </StorageEmulatorConfig>
```

Storage Emulator usage:

```text
AzureStorageEmulator.exe init           : Initialize the emulator database and configuration
AzureStorageEmulator.exe start          : Start the emulator
AzureStorageEmulator.exe stop           : Stop the emulator
AzureStorageEmulator.exe status         : Get current emulator status
AzureStorageEmulator.exe clear          : Delete all data in the emulator
AzureStorageEmulator.exe help [command] : Show general or command-specific help
```

### Run locally

- Start function locally for debugging: `func start --python [--verbose]`
- The function listens at `http://localhost:7071/api/<routing>`
- Stop local debugging: hit `Ctrl+C`

### Errors and Warnings

**Error:**

*Microsoft.Azure.WebJobs.Extensions.Http: Could not load file or assembly 'System.Net.Http.Formatting, Version=5.2.8.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35'. The system cannot find the file specified. Value cannot be null. (Parameter 'provider')*

**Solution**:

- install/reinstall/update ASP.NET Core x64 6.0.26
- install/reinstall/update Azure Functions Core Tools x64 4.0.5455

---

**Error:**

When the function starts: *ERROR: Error: No module named 'requests', Cannot find module. Please check the requirements.txt file for the missing module.* even though the requirements.txt is correct and `pip install -r requirements.txt` was executed.

**Solution:**

Make sure `venv` has been activated. If it doesn't help, delete and rebuild `venv`.

---

**Error:**

- The Azure Storage connection string is either empty or invalid. Unable to record diagnostic events, so the diagnostic logging service is being stopped.
- Azure.Core: No connection could be made because the target machine actively refused it. (127.0.0.1:10002)

**Solution:**

Make sure the Azure Storage Emulator is running.

---

**Warning** in local debug mode:

*Customer packages not in sys path. This should never happen!*

**Solution:** Can be safely ignored

## Azure

### CI/CD

#### WARNING

Make sure your deployment method does not ship files and folders listed in the `.funcignore` file.

#### Deployment and stages

AzDO YAML pipeline automatically deploys the code to the Function App when there is a new commit to the `main` branch.

- Stage 1 of the pipeline deploys to the Development subscription. Executes automatically.
- Stage 2 of the pipeline deploys to the Production subscription. Will execute if Stage 1 succeeds. Successful execution of Stage 1 is a prerequisite for Stage 2 - you must select both stages when executing the YAML pipeline manually in AzDO.

#### Python dependencies

Install Python dependencies into the pipeline working directory (`--target` in the example below); otherwise, the code will never appear in the Function App, and troubleshooting will be difficult because there will be no clear error messages to identify the source of the problem.

```yaml
- task: CmdLine@2
    displayName: 'Install Python libraries'
    inputs:
        script: 'pip install -r requirements.txt --target="./.python_packages/lib/site-packages"'
        workingDirectory: '$(System.DefaultWorkingDirectory)'
```

### Troubleshooting and debugging

#### App settings

You can access Function App settings in Development Subscription via [https://azfunc-my-v2-function-dev.scm.azurewebsites.net/api/settings](https://azfunc-my-v2-function-dev.scm.azurewebsites.net/api/settings)

## Useful resources

- [Azure Functions V2 Python developer guide](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Develop Azure Functions locally using Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- [Kudu](https://github.com/projectkudu/kudu/wiki)
