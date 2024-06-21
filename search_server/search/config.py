"""search_server development configuration."""
import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# File Upload to var/uploads/
SEARCH_SERVER_ROOT = pathlib.Path(__file__).resolve().parent.parent

# # Add search_server and index_server to sys.path
# search_server_path = os.path.abspath('/path/to/search_server')
# index_server_path = os.path.abspath('/path/to/index_server')

# sys.path.insert(0, search_server_path)
# sys.path.insert(0, index_server_path)

# UPLOAD_FOLDER = INSTA485_ROOT/'var'/'uploads'
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = 'var/search.sqlite3'

# From spec for p5
SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]
