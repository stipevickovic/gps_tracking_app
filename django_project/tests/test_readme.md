### Testing


Commands applied from django_project/ folder.


Run tests:

    pytest

Run tests after database changes (migrations):

    pytest --create-db

Run tests with coverage with --cov flag (report) example:

    pytest --cov=<app-name>.models --cov=<app-name>.models

Create html representation of last pytest coverage run:

    coverage html

Html representation is saved in `htmlcov/` folder.
Open `htmlcov/index.html` to display a list of links for files covered.
