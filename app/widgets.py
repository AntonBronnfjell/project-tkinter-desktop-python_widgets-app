from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from .models import Task


class ScrollableFrame(ttk.Frame):
    """A vertical scrollable area that can contain arbitrary child widgets."""

    def __init__(self, master: tk.Widget, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)

        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)

        self.inner.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        def _on_canvas_configure(event):
            self.canvas.itemconfig(window, width=event.width)

        self.canvas.bind("<Configure>", _on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class TaskItem(ttk.Frame):
    """Visual representation of a Task with controls for editing and deleting."""

    def __init__(
        self,
        master: tk.Widget,
        task: Task,
        on_toggle_complete: Callable[[str, bool], None],
        on_title_change: Callable[[str, str], None],
        on_delete: Callable[[str], None],
    ) -> None:
        super().__init__(master)

        self.task = task
        self.on_toggle_complete = on_toggle_complete
        self.on_title_change = on_title_change
        self.on_delete = on_delete

        self.is_completed_var = tk.BooleanVar(value=self.task.is_completed)
        self.title_var = tk.StringVar(value=self.task.title)

        self.check = ttk.Checkbutton(self, variable=self.is_completed_var, command=self._handle_toggle)
        self.entry = ttk.Entry(self, textvariable=self.title_var)
        self.delete_btn = ttk.Button(self, text="Eliminar", command=lambda: self.on_delete(self.task.id))

        self.check.grid(row=0, column=0, padx=(4, 8), pady=6)
        self.entry.grid(row=0, column=1, sticky="ew", pady=6)
        self.delete_btn.grid(row=0, column=2, padx=(8, 4), pady=6)

        self.columnconfigure(1, weight=1)

        self.entry.bind("<Return>", self._handle_title_commit)
        self.entry.bind("<FocusOut>", self._handle_title_commit)

        self._apply_completed_style()

    def _handle_toggle(self) -> None:
        new_state = bool(self.is_completed_var.get())
        self.on_toggle_complete(self.task.id, new_state)
        self._apply_completed_style()

    def _handle_title_commit(self, event=None) -> None:
        new_title = self.title_var.get().strip()
        if new_title != self.task.title:
            self.on_title_change(self.task.id, new_title)

    def _apply_completed_style(self) -> None:
        if self.is_completed_var.get():
            self.entry.configure(state="readonly")
        else:
            self.entry.configure(state="normal")


