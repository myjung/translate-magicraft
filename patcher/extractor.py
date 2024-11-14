from dataclasses import dataclass
import toml as tomllib
import pathlib
from shutil import copyfile
import csv
import io

import UnityPy
from UnityPy.enums import ClassIDType


@dataclass
class MagicraftMetadata:
    TextConfig
    TextConfig_ActivateGirl
    TextConfig_Curse
    TextConfig_Handbook
    TextConfig_Potion
    TextConfig_Relic
    TextConfig_Research
    TextConfig_Resource
    TextConfig_Set
    TextConfig_Spell
    TextConfig_Story
    TextConfig_Unit
    TextConfig_Wand