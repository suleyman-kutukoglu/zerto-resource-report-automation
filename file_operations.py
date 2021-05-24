from pathlib import Path
from settings import get_report_folder_path


def create_folder_for_new_day():
    Path(get_report_folder_path()).mkdir(
        parents=True, exist_ok=True)
