"""Index package initializer."""
import os
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name


app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
# ...
import index.api  # noqa: E402  pylint: disable=wrong-import-position

# Load inverted index, stopwords, and pagerank into memory
index.api.main.load_index()
