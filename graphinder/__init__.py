# pylint: skip-file

from rich.console import Console

__version__ = '1.0.0-beta.0'

console = Console()

title = r"""
  ____                 _     _           _           
 / ___|_ __ __ _ _ __ | |__ (_)_ __   __| | ___ _ __ 
| |  _| '__/ _` | '_ \| '_ \| | '_ \ / _` |/ _ \ '__|
| |_| | | | (_| | |_) | | | | | | | | (_| |  __/ |   
 \____|_|  \__,_| .__/|_| |_|_|_| |_|\__,_|\___|_|   
                |_|                                  

        """
# pylint: disable=anomalous-backslash-in-string
console.print(title, style='bold')

console.print(
    f'  (c) 2021 Escape Technologies - Version: {__version__} \n\n\n')

from graphinder.main import main  # noqa
