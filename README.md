keadatabase-back
================

[![Build Status](https://travis-ci.org/greenstone/keadatabase-back.svg?branch=master)](https://travis-ci.org/greenstone/keadatabase-back)

The GeoDjango-based back-end for the Kea Database <https://keadatabase.nz> citizen science project.
Sponsored by [Catalyst](https://catalyst.net.nz).

Setup
-----
This guide assumes that `python3`, `pip`, `postgres` (with postgis) and virtual
environments are installed.

`./manage.py` commands should be run from the `src/` directory.

For instructions on setting up PostGIS:
<https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/postgis/>

1. Setup `python3` virtual environment
2. Create a new database 'keadatabase' with username 'postgres' and no password
3. `pip install -r requirements.txt`
4. `cd src`
5. `./manage.py migrate`
6. `./manage.py createsuperuser`

NB: To create database, login as postgres user then run `createdb keadatabase` in bash shell and `grant all privileges on database keadatabase to postgres;` in the psql shell. You may need to adjust your pg_hba.conf settings for no password access.

Running
-------
`./manage.py runserver`

Testing
-------
Ensure that the `keadatabase_test` db is able to be created before running.

`./manage.py test`

Data synchronisation: Bird, BandCombo, StudyArea
------------------------------------------------
These steps assume you have `mdbtools` installed.

1. Create a directory 'data/' and add the `kea_be.mdb` file (back-end to the Access kea database).
2. From the current directory run: `./export_kea_be.sh`. This will export three CSV files into the `data/` directory.
3. Run `./manage.py synchronise`

Data synchronisation is non-destructive (it will not delete objects).

Importing database dump
-----------------------
To import a database dump from Heroku run the following command as the `postgres` user:
`pg_restore --clean --no-owner --role=postgres -d keadatabase <file>.sql`


Data synchronisation: Region, Place
-----------------------------------

1. Obtain datasets for Region (merged copy of NZ regions dataset), and Place (SI-only NZ Placenames)
2. Import datasets into a local version of the kea database using `./manage.py loadregions` and `./manage.py loadplaces`
3. Dump data using `./manage.py dumpdata locations.place`and `./manage.py dumpdata locations.region`
4. Upload data to the keadatabase S3 bucket
5. `heroku run bash` then wget the data and run `./manage.py loadddata <filename>json`


Deploying
---------
This code is deployed using a continuous integration workflow. Code pushed to master will be deployed to Heroku after Travis CI tests are passed. The process takes a few minutes.

Please note, aside from `collectstatic` Django commands such as `migrate` are not run automatically.

Layout
------
* `test_data/` - Sample CSV data used for testing purposes
* `src/bands/` - Band models and helpers
* `src/birds/` - Bird models and helpers
* `src/keadatabase/` - Project settings
* `src/locations/` - StudyArea models and helpers
* `src/report/` - The only non-read-only API endpoint, used for POSTing sightings
* `src/sightings/` - All sightings related information, including links to Bird objects
* `src/synchronise/` - Command and helpers that syncs Django DB with provided CSVs
* `src/theme/` - Django REST Framework customisations

Licence
-------
Kea Database  
Copyright (C) 2018 Greenstone Limited  
<hello@greenstone.org.nz>  

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
