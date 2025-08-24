from __future__ import annotations

import os
import platform
import tkinter as tk
from tkinter import ttk
from typing import List

from .models import Task
from .storage import JsonTaskRepository
from .widgets import ScrollableFrame, TaskItem


class TodoApp(tk.Tk):
    """Main application window for the To-Do list."""

    def __init__(self, repository: JsonTaskRepository) -> None:
        super().__init__()

        self.repository = repository
        self.tasks: List[Task] = self.repository.load_tasks()
        self.filter_var = tk.StringVar(value="all")

        self.title("Lista de Tareas - Tkinter")
        self._configure_style()
        self._build_layout()
        self._bind_shortcuts()
        self._refresh_tasks()

    def _configure_style(self) -> None:
        self.geometry("720x520")
        self.minsize(520, 420)
        style = ttk.Style()
        if platform.system() == "Darwin":
            style.theme_use("clam")
        style.configure("TButton", padding=6)
        style.configure("TEntry", padding=4)
        style.configure("Counter.TLabel", font=("Helvetica", 10, "bold"))

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Nueva tarea", command=self._focus_new_task)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.destroy)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Eliminar completadas", command=self._delete_completed_tasks)
        menu_bar.add_cascade(label="Edición", menu=edit_menu)
        self.config(menu=menu_bar)

        input_frame = ttk.Frame(self)
        input_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))
        input_frame.columnconfigure(0, weight=1)

        self.new_title_var = tk.StringVar()
        self.new_title_entry = ttk.Entry(input_frame, textvariable=self.new_title_var)
        self.new_title_entry.grid(row=0, column=0, sticky="ew")
        add_btn = ttk.Button(input_frame, text="Añadir", command=self._add_task)
        add_btn.grid(row=0, column=1, padx=(8, 0))

        filters_frame = ttk.Frame(self)
        filters_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))
        filters_frame.columnconfigure(0, weight=1)

        left_filters = ttk.Frame(filters_frame)
        left_filters.grid(row=0, column=0, sticky="w")

        ttk.Radiobutton(left_filters, text="Todas", value="all", variable=self.filter_var, command=self._refresh_tasks).grid(
            row=0, column=0, padx=(0, 8)
        )
        ttk.Radiobutton(left_filters, text="Activas", value="active", variable=self.filter_var, command=self._refresh_tasks).grid(
            row=0, column=1, padx=(0, 8)
        )
        ttk.Radiobutton(left_filters, text="Completadas", value="completed", variable=self.filter_var, command=self._refresh_tasks).grid(
            row=0, column=2
        )

        self.counter_label = ttk.Label(filters_frame, style="Counter.TLabel")
        self.counter_label.grid(row=0, column=1, sticky="e")

        list_frame = ttk.Frame(self)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        self.scrollable = ScrollableFrame(list_frame)
        self.scrollable.grid(row=0, column=0, sticky="nsew")

        self.new_title_entry.focus_set()

    def _bind_shortcuts(self) -> None:
        self.bind("<Return>", lambda e: self._add_task())
        self.bind("<Control-n>", lambda e: self._focus_new_task())
        self.bind("<Command-n>", lambda e: self._focus_new_task())
        self.bind("<Escape>", lambda e: self._clear_new_title())

    def _focus_new_task(self) -> None:
        self.new_title_entry.focus_set()

    def _clear_new_title(self) -> None:
        self.new_title_var.set("")

    def _add_task(self) -> None:
        title = self.new_title_var.get().strip()
        if not title:
            return
        new_task = Task(title=title)
        self.tasks.append(new_task)
        self.repository.save_tasks(self.tasks)
        self.new_title_var.set("")
        self._refresh_tasks()

    def _delete_completed_tasks(self) -> None:
        self.tasks = [task for task in self.tasks if not task.is_completed]
        self.repository.save_tasks(self.tasks)
        self._refresh_tasks()

    def _update_counts(self) -> None:
        total = len(self.tasks)
        active = len([t for t in self.tasks if not t.is_completed])
        completed = total - active
        self.counter_label.configure(text=f"Total: {total}  Activas: {active}  Completadas: {completed}")

    def _filtered_tasks(self) -> List[Task]:
        mode = self.filter_var.get()
        if mode == "active":
            return [t for t in self.tasks if not t.is_completed]
        if mode == "completed":
            return [t for t in self.tasks if t.is_completed]
        return list(self.tasks)

    def _refresh_tasks(self) -> None:
        for child in list(self.scrollable.inner.winfo_children()):
            child.destroy()

        for index, task in enumerate(self._filtered_tasks()):
            item = TaskItem(
                self.scrollable.inner,
                task=task,
                on_toggle_complete=self._on_toggle_complete,
                on_title_change=self._on_title_change,
                on_delete=self._on_delete_task,
            )
            item.grid(row=index, column=0, sticky="ew")

        self._update_counts()

    def _on_toggle_complete(self, task_id: str, new_state: bool) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.is_completed = new_state
                break
        self.repository.save_tasks(self.tasks)
        self._refresh_tasks()

    def _on_title_change(self, task_id: str, new_title: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.title = new_title
                break
        self.repository.save_tasks(self.tasks)
        self._update_counts()

    def _on_delete_task(self, task_id: str) -> None:
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.repository.save_tasks(self.tasks)
        self._refresh_tasks()


def default_repository_path() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    return os.path.abspath(os.path.join(data_dir, "tasks.json"))


