# -*- coding: utf-8 -*-

from enum import Enum

db_file = "database.vdb"


class States(Enum):
    S_START = "0"
    S_ENTER_NAME = "1"
    S_ENTER_GEO = "2"
