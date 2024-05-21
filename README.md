# venue-accesses-app

## Getting started for dev

Create , activate a virtualenv. Install the dependencies wrote into requirements.txt and run the application choosing the python intepreter into the virtualvenv.  

## Getting started for usage
### CMD:
- make build
- make run
### view at http://localhost:8085/login

## Generate and open coverage report:
### Install coverage
pip install coverage

### Run tests with coverage
coverage run -m pytest

### Generate terminal report
coverage report

### Generate HTML report
coverage html

### Optional: Open HTML report in the browser (Linux/Mac)
open htmlcov/index.html
### Optional: Open HTML report in the browser (Windows)
start htmlcov/index.html


