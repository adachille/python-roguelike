"""Class to hold configuration."""
import os
from pathlib import Path

import yaml


class Config:
    """Load and validate the configuration file."""

    def __init__(self, config_file_name: str = "config.yml"):
        """Initialize."""

        self.root_dir = Path(os.getcwd())
        with open(self.root_dir / config_file_name) as filein:
            self.config = yaml.safe_load(filein)
        self.player = self.config["player"]
        self.procgen = self.config["procgen"]
        self.view = self.config["view"]

        self.relative_paths = self.config["paths"]
        self.paths = self.make_absolute_paths()

    def make_absolute_paths(self):
        """Get paths as absolute paths."""
        return {key: self.root_dir / path for key, path in self.relative_paths.items()}
