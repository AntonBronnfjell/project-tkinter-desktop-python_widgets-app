from __future__ import annotations

import os

from app.ui import TodoApp, default_repository_path
from app.storage import JsonTaskRepository


def main() -> None:
    data_path = default_repository_path()
    repository = JsonTaskRepository(data_path)
    app = TodoApp(repository)
    app.mainloop()


if __name__ == "__main__":
    main()


