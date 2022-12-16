# PokeParty
An OBS browser extension to display your current pokemon party.

## Installation
Requires Python 3.10+

`pip install -r requirements.txt`

## Sprites
The sprites are SVGs that are intended to be created by [pokesprite-svg](https://github.com/linkian209/pokesprite-svg). After creating the SVGs take the `pokesprite/` directory from the build directory and place it into the `static/img/` directory, so that they can be served.

Alternatively, you can store these SVGs somewhere else and have NGINX or serve them.

## Database
The database is a SQLite table created in the root directory of the application. Migrations are managed by alembic:

`alembic upgrade head`