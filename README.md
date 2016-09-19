# Kea Database
An online database designed to track kea sightings and information for the Kea Conservation Trust


## Layout
* 'locations' - models and admin for primary and secondary locations
* 'birds' - models and admin for known birds
* 'sightings' - models and admin for sightings of kea
* 'portal' - public facing portal for adding sightings and searching kea
* 'api' - contains urls for API
* 'bands' - models and admin for band combinations


## Setup
This guide assumes that `python3`, `pip`, `postgres` (with postgis), `bower`, `sass` and python
virtual environments are installed.

For instructions on setting up `postgres` with postgis:
<https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/postgis/>

1. Ensure postgres is installed with the postgis extension
2. Create a new database 'keadatabase' with username 'keadatabase' and no password
3. Setup virtual environment with python3
4. `bower install`
5. `pip install -r requirements.txt` (install relevant dependencies)
6. `./manage.py migrate` (database setup and migration)
7. `./manage.py createsuperuser` (superuser creation)


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
* `./manage.py loaddata sample_data/locations.json`
* `./manage.py loaddata sample_data/birds.json`


### DOC boundary data
1. Download WGS84 SHP of <https://koordinates.com/layer/754-doc-public-conservation-areas/>
2. Unzip and place into `locations/data/`
3. `./manage.py shell` - Invoke shell
4. `from locations import load_data; load_data.run()`


## Contributing
Please use `pylint` to check your code before submitting a pull request.
A `.pylintrc` file has been supplied.


## Licence
Kea Database
Copyright (C) 2016 Greenstone Limited <hello@greenstone.org.nz>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
