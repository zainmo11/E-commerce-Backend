import os

import dj_database_url

from .base import *  # noqa: F403

# For now
BEBUG = True

ALLOWED_HOSTS = ["https://distributed-project-backend.onrender.com"]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # noqa: F405
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ["DATABASE_URL"], conn_max_age=600
    )
}
