"""Insta485 model (database) API."""
import sqlite3
import flask
import search


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template. Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Open a new database connection.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in flask.g:
        db_filename = search.app.config['DATABASE_FILENAME']
        flask.g.sqlite_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection. This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db


@search.app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()


def get_document_details(docid):
    """Get document details from the database."""
    db = get_db()
    cursor = db.execute(
        "SELECT title, summary, url FROM documents WHERE docid = ?",
        (docid,)
    )
    row = cursor.fetchone()
    return row if row else None


# def get_document_details(docid):
#     db = get_db()
#     cur = db.execute('SELECT * FROM documents WHERE docid = ?', (docid,))
#     result = cur.fetchone()
#     if result:
#         return {
#             'docid': result['docid'],
#             'title': result['title'],
#             'summary': result.get('summary', 'No summary available'),
#             'url': result['url']
#         }
#     return None
