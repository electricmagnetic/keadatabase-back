keadatabase-back
================

[![Build Status](https://travis-ci.org/greenstone/keadatabase-back.svg?branch=master)](https://travis-ci.org/greenstone/keadatabase-back)

Setup
-----
This guide assumes that `python3`, `pip`, `postgres` (with postgis) and virtual
environments are installed.

`./manage.py` commands should be run from the `src/` directory.

For instructions on setting up PostGIS:
<https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/postgis/>

1. Setup `python3` virtual environment
2. Create a new database 'keadatabase' with username 'postgres' and no password
3. `pip install -r requirements.txt`
4. `./manage.py migrate`
5. `./manage.py createsuperuser`

Running
-------
`./manage.py runserver`

Testing
-------
Ensure that the `keadatabase_test` db is able to be created before running.
`./manage.py test`

Data synchronisation
--------------------
Export tables from Access to CSV files, ensuring that they use UTF-8 encoding, the fields are included in the first row and that dates are preceded by a leading zero.

Data synchronisation is non-destructive (it will not delete objects).

Add the following files to a `data/` folder in the root directory:
* `tStudyAreas.csv`
* `Kea.csv`
* `Kea bands.csv`
* `Transmitters.csv`

The filenames are taken directly from the Access table names.

Then run: `./manage.py synchronise`

Deploying
---------
TODO (but pre-deploy steps: `./manage.py test` and `./manage.py check --deploy`)

Layout
------
* 'test_data/' - Sample CSV data used for testing purposes
* `src/birds/` - Bird models and helpers
* `src/keadatabase/` - Project settings
* `src/locations/` - StudyArea models and helpers
* `src/synchronise/` - Command and helpers that syncs Django DB with provided CSVs
* `src/theme/` - Django REST Framework customisations

Licence
-------
Kea Database  
Copyright (C) 2017 Greenstone Limited <hello@greenstone.org.nz>  

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
