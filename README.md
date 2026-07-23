# Automation Framework

Production-grade UI and API test automation framework built with
**Python 3.12**, **Playwright**, **Pytest**, and **requests**.

## Stack

| Layer            | Technology            |
|-------------------|------------------------|
| UI automation      | Playwright (sync API) |
| API automation     | requests               |
| Test runner        | Pytest                |
| Parallel execution | pytest-xdist           |
| Reporting          | pytest-html            |
| Config management  | python-dotenv           |

## Project Structure

Notes:
For pytest.ini file: 
addopts =
    --strict-markers #Prevents silently skipping misspelt markers. eg: wo this smkoe and smoke will be considered separate markers and only one runs.
    --html=reports/html/report.html #Human readable reports
    --self-contained-html # Has CSS etc within
    --junitxml=reports/junit/results.xml #For CI/CD
    -ra #report summary, all except passed tests to get a short test summary at the end
    --tb=short # Short tracebacks
    -v #verbose so that instead of only ... pytest names the tests in cli
    --strict-config #catch invalid configuration entries


; Built in markers : 
    ; skip: Skip the test 
    ; skipif: Skip under certain conditions 
    ; xfail: Test known to fail
    ; parametrize: run same test with multiple set of arguments
    ; usefixtures: apply fixtures wo listing them as function arguments


;Log levels:
    ; DEBUG : Not shown here, debug info
    ; INFO : Shown, General info.
    ; WARNING : Shown, unexpected but not error 
    ; ERROR : Shown, error
    ; CRITICAL : Shown, serious error