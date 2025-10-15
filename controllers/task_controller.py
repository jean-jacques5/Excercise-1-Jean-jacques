# controllers/task_controller.py
# -----------------------------
# Couche "métier" : on gère la liste des tâches,
# la lecture/écriture JSON et les actions add/delete/display.
# -----------------------------

import json
from pathlib import Path
from typing import List, Optional
from model.task import Task, STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_FILE = DATA_DIR / "tasks.json"

class TaskController:
    def __init__(self, storage_path: Path = DATA_FILE):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    # ---------- Persistance ----------
    def _load(self) -> List[Task]:
        if not self.storage_path.exists():
            return []
        try:
            with self.storage_path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
        except json.JSONDecodeError:
            return []
        return [Task.from_dict(item) for item in raw]

    def _save(self, tasks: List[Task]) -> None:
        data = [t.to_dict() for t in tasks]
        with self.storage_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ---------- Actions demandées ----------
    def add(self, title: str, notes: Optional[str] = None) -> Task:
        if not title or not title.strip():
            raise ValueError("Le titre ne peut pas être vide.")
        task = Task(title=title, notes=notes)
        tasks = self._load()
        tasks.append(task)
        self._save(tasks)
        return task

    def delete(self, task_id: str) -> bool:
        tasks = self._load()
        new_tasks = [t for t in tasks if t.id != task_id]
        changed = len(new_tasks) != len(tasks)
        if changed:
            self._save(new_tasks)
        return changed

    def display(self, status: Optional[str] = None) -> List[Task]:
        tasks = self._load()
        if status in (STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE):
            tasks = [t for t in tasks if t.status == status]
        # tri simple : par created_at (ordre d’arrivée)
        tasks.sort(key=lambda t: t.created_at)
        return tasks

    # ---------- Petits plus utiles (optionnels en CLI) ----------
    def set_status(self, task_id: str, status: str) -> Optional[Task]:
        tasks = self._load()
        for t in tasks:
            if t.id == task_id:
                t.set_status(status)
                self._save(tasks)
                return t
        return None

    def clear(self) -> None:
        self._save([])
