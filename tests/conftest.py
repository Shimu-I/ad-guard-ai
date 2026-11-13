import os

# Use a throwaway in-memory database for every test run. This must be set before
# the app modules are imported, because the engine is created at import time.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["APP_ENV"] = "test"
