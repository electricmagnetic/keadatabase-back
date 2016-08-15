# Kea Database
An online database designed to track kea sightings and information for the Kea Conservation Trust


## Layout
* 'locations' - models and admin for primary and secondary locations
* 'birds' - models and admin for banded birds
* 'sightings' - models and admin for sightings of kea
* 'portal' - public facing portal for adding sightings and searching kea


## Setup
This guide assumes that `python3`, `pip`, `postgres` (with postgis) and virtual environments are
installed.

For instructions on setting up `postgres` with postgis:
<https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/postgis/>

1. Ensure postgres is installed with the postgis extension
2. Create a new database 'keadatabase' with username 'keadatabase' and no password
3. Setup virtual environment with python3
4. `pip install -r requirements.txt` (install relevant dependencies)
5. `./manage.py migrate` (database setup and migration)
6. `./manage.py createsuperuser` (superuser creation)


## Running
`./manage.py runserver`


## Testing
`./manage.py test`


## Deploying
1. `./manage.py test` - Test to make sure everything is compliant
2. `./manage.py check --deploy` - Check deploy settings for security
TBD


## Loading data
### Sample data
`./manage.py loaddata sample_data/locations.json`
`./manage.py loaddata sample_data/birds.json`


### DOC boundary data
1. Download WGS84 SHP of <https://koordinates.com/layer/754-doc-public-conservation-areas/>
2. Unzip and place into `locations/data/`
3. `./manage.py shell` - Invoke shell
4. `from locations import load_data; load_data.run()`


## Contributing
Please use `pylint` to check your code before submitting a pull request. A `.pylintrc` file has been
supplied.


## Licence
TBD
