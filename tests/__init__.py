from os import environ

import pytest

from .helpers import create_graphs
from .helpers import bigtable_emulator


TEST_DATASETS_PATH = "tests/datasets/*.yml"

environ["PRELOAD_DATASETS"] = "/app/dataset/*.yml"
