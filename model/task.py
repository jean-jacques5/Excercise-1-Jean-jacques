# model/task.py
# -----------------------------
# Modèle très simple d'une "tâche".
# -----------------------------

import uuid
from datetime import datetime

STATUS_TODO = "todo"
STATUS_IN_PROGRESS = "in_progress"
STATUS_DONE = "done"

def now_iso():
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

class Task:
    """
    Représente une tâche de ToDoList.
    - title: texte
    - status: 'todo' | 'in_progress' | 'done'
    - notes: texte optionnel
    - id: identifiant unique (UUID)
    - created_at / updated_at: horodatages ISO lisibles
    """
    def __init__(self, title, notes=None, status=STATUS_TODO, task_id=None,
                 created_at=None, updated_at=None):
        self.id = task_id or str(uuid.uuid4())
        self.title = (title or "").strip()
        self.notes = (notes or "").strip() or None
        self.status = status
        self.created_at = created_at or now_iso()
        self.updated_at = updated_at or now_iso()

    # Petites méthodes utiles
    def rename(self, new_title):
        self.title = (new_title or "").strip()
        self.touch()

    def set_notes(self, text):
        self.notes = (text or "").strip() or None
        self.touch()

    def set_status(self, status):
        if status in (STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE):
            self.status = status
            self.touch()

    def touch(self):
        self.updated_at = now_iso()

    # Sérialisation <-> JSON
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "notes": self.notes,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(d: dict):
        return Task(
            title=d.get("title", ""),
            notes=d.get("notes"),
            status=d.get("status", STATUS_TODO),
            task_id=d.get("id"),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
        )
