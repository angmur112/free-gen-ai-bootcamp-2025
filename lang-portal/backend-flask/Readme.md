## Setting up the database

```sh
invoke init-db
```

This will do the following:
- create the words.db (Sqlite3 database)
- run the migrations found in `seeds/`
- run the seed data found in `seed/`

Please note that migrations and seed data is manually coded to be imported in the `lib/db.py`. So you need to modify this code if you want to import other seed data.

## Clearing the database

Simply delete the `words.db` to clear entire database.

## Running the backend api

```sh
python app.py 
```

This should start the flask app on port `5000`

1. **Database Setup**
   - The command `invoke init-db` is used to initialize the database
   - It performs three main tasks:
     - Creates a SQLite3 database file named `words.db`
     - Runs database migrations from the `seeds/` directory
     - Loads seed (initial) data from the `seed/` directory
   - There's a note that migrations and seed data need to be manually configured in `lib/db.py`

2. **Database Reset**
   - To clear the database, you simply need to delete the `words.db` file

3. **Starting the Backend API**
   - The command `python app.py` starts the Flask application
   - The API will run on port 5000
