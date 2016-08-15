# Kea Database
An online database designed to track kea sightings and information for the Kea Conservation Trust


## Setup
This guide assumes that `python3`, `pip`, and virtual environments are installed.
1. Setup virtual environment with python3
2. `pip install -r requirements.txt` (install relevant dependencies)
3. `./manage.py migrate` (database setup and migration)
4. `./manage.py createsuperuser` (superuser creation)


## Running
`./manage.py runserver`


## Testing
`./manage.py test`


## Deploying
TBD


## Contributing
Please use `pylint` to check your code before submitting a pull request. A `.pylintrc` file has been
supplied.


## Licence
TBD
