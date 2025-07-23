# LSNZ Website 2.0

This is a reimplementation of the [LSNZ website](lasersportsnz.com) using Python and Flask, instead of Wordpress, to support adding more complex dynamic features and domain-specific data models.

## How to run
This project uses [uv](https://docs.astral.sh/uv/) for dependency management. It's recommended you install this first, so that you can install all the project dependencies into a virtual environment with ```uv sync```. Then:
1. Create a development database with the current schema using ```flask db upgrade head```
2. Populate the DB with some example records using ```flask cli prepopulate``` (this drops any other records)
3. Use ```flask run``` to start the dev server on localhost:5000

## How to update database schema
This project uses [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/) for object-relational mapping, app/models.py contains the data models. [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is used for database migrations, so if changes to the models are made then ūse ```flask db migrate -m "<MIGRATION_MESSAGE>"``` to create a corresponding migration script. Then use ```flask db upgrade``` to migrate the database to the new schema. 

## Planned features
* OAuth options via Facebook/Google
* Switch from Google forms to custom UI that integrates with database
* Role-based features for user accounts e.g. ability to create/edit blog posts, manage permissions, manage tournament registrations etc.
* Improved payment integrations
* Options for season pass management
* Player pages with profile pictures, tournament finishes etc.
* More advanced tournament registration interface including ability to create/join teams via dropdown
* Interactive maps showing Zone sites
* Event calendars, subscribtion options for event updates/reminders
* Consolidation of historical tournament stats into database, support for variety of queries and Excel/Sheets export
* Analysis tools for player grading
* Embedded Twitch streams
* Admin features for management of LSNZ Committee
* APIs for integration with tournament admin applications, including automated post-tournament results saving/posting
* Open-source contribution guide and consolidation with other apps under a LSNZ GitHub organisation
* Additional technical resources
* Timing minigames