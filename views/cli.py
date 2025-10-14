# views/cli.py
# -----------------------------
# Interface CLI très simple avec argparse.
# Elle utilise le contrôleur pour réaliser les actions
# et s'occupe d'afficher proprement.
# -----------------------------

import argparse
from controllers.task_controller import TaskController
from model.task import STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE

def _icon(status: str) -> str:
    return {
        STATUS_TODO: "📝",
        STATUS_IN_PROGRESS: "⏳",
        STATUS_DONE: "✅",
    }.get(status, "•")

def build_parser():
    p = argparse.ArgumentParser(
        prog="todolist",
        description="ToDoList CLI (MVC débutant)"
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    # display
    sp = sub.add_parser("display", help="Afficher les tâches")
    sp.add_argument("--status", choices=[STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE],
                    help="Filtrer par statut")

    # add
    sp = sub.add_parser("add", help="Ajouter une tâche")
    sp.add_argument("title", help="Titre de la tâche")
    sp.add_argument("--notes", help="Notes (optionnel)")

    # delete
    sp = sub.add_parser("delete", help="Supprimer une tâche")
    sp.add_argument("id", help="ID de la tâche")

    # (petits plus)
    sp = sub.add_parser("start", help="Passer une tâche en cours")
    sp.add_argument("id")

    sp = sub.add_parser("done", help="Terminer une tâche")
    sp.add_argument("id")

    sub.add_parser("clear", help="Vider toutes les tâches")

    return p

def run():
    args = build_parser().parse_args()
    c = TaskController()

    if args.cmd == "display":
        tasks = c.display(status=args.status)
        if not tasks:
            print("Aucune tâche.")
            return
        for t in tasks:
            notes = f"\n    Notes: {t.notes}" if t.notes else ""
            print(f"{_icon(t.status)} {t.title}\n    id={t.id}  status={t.status}  updated={t.updated_at}{notes}")

    elif args.cmd == "add":
        try:
            t = c.add(title=args.title, notes=args.notes)
            print(f"✅ Ajoutée : {t.title}\n    id={t.id}")
        except ValueError as e:
            print(f"⚠️  {e}")

    elif args.cmd == "delete":
        ok = c.delete(args.id)
        print("🗑️  Supprimée." if ok else "⚠️  Tâche introuvable.")

    elif args.cmd == "start":
        t = c.set_status(args.id, STATUS_IN_PROGRESS)
        print(f"⏳ En cours : {t.title}" if t else "⚠️  Tâche introuvable.")

    elif args.cmd == "done":
        t = c.set_status(args.id, STATUS_DONE)
        print(f"✅ Terminée : {t.title}" if t else "⚠️  Tâche introuvable.")

    elif args.cmd == "clear":
        c.clear()
        print("🧹  Liste vidée.")
