import os
from unittest.mock import Mock, patch

def patch_env(settings):
    return patch.object(os, 'getenv', Mock(side_effect=settings.get))
