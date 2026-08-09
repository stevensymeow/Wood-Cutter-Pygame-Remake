from __future__ import annotations
import tkinter as tk
from tkinter import ttk

import os
from pathlib import Path

from src.utils.loader import get_persistent_path, ASSETS_DIR
from src.levels import Level, LevelInfo

BASE_PATH = get_persistent_path("")

def tk_level_select(level_datas: list[LevelInfo], index: int, parent_object: tk.Tk | tk.Toplevel | None = None, icon_path: str | Path = "") -> int:
    # Deal with parent
    for name, root in globals().items():
        if isinstance(root, tk.Tk):
            try:
                root.destroy()
                print(f"[*] You bad! I have to destroy the root '{name}' for you!")
            except Exception:
                pass
    
    if parent_object:
        parent = parent_object
    else:
        parent = tk.Tk()
        parent.withdraw()
    
    # Icon
    do_set_icon = False
    
    if icon_path:
        icon_path = Path(icon_path)
        if not icon_path.is_absolute():
            icon_path = BASE_PATH / icon_path
        if os.path.exists(icon_path):
            parent.iconbitmap(icon_path)
            do_set_icon = True
     
    # Dialog
    dialog = tk.Toplevel(parent)
    
    if (not parent_object) and do_set_icon:
        dialog.iconbitmap(icon_path)
    
    dialog.title("Level select window")
    dialog.resizable(False, False)
    d_width = 300
    d_heigth = 200
    dialog.geometry(f"{d_width}x{d_heigth}")
    dialog.grab_set()
    
    pad = {"padx": 10, "pady": 4}
    
    level_cnt = len(level_datas)
    level_names = [level_data["level_name"] for level_data in level_datas]
    level_labels = [level_data["level_label"] for level_data in level_datas]
    level_index = index if 0 <= index <= level_cnt-1 else 0
    level_name_var = tk.StringVar(value=level_names[level_index])
    level_label_var = tk.StringVar(value=level_labels[level_index])
    level_index_var = tk.IntVar(value=level_index)
    
    # Must first deal with root window before creating variable
    ret_val = tk.IntVar(value=level_index)
    
    def _build_side_frame(parent: tk.Toplevel, row: int, label: str, name_var: tk.StringVar, label_var: tk.IntVar, index_var: tk.IntVar):
        frame = ttk.Labelframe(parent, text=label)
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", **pad)
        
        def _on_name_change(e = None):
            level_index = level_names.index(name_var.get())
            label_var.set(level_labels[level_index])
            index_var.set(level_index)
        
        def _on_label_change(e = None):
            level_index = level_labels.index(label_var.get())
            name_var.set(level_names[level_index])
            index_var.set(level_index)
        
        def _on_index_change(e = None):
            level_index = index_var.get()
            name_var.set(level_names[level_index])
            label_var.set(level_labels[level_index])
        
        ttk.Label(frame, text="Level:").grid(
            row=0, column=0, sticky="w", padx=4, pady=2
        )
        name_combo = ttk.Combobox(
            frame,
            textvariable=name_var,
            values=level_names,
            state="readonly",
            width=22,
        )
        name_combo.grid(row=0, column=1, columnspan=4, sticky="ew", padx=4, pady=2)
        
        ttk.Label(frame, text="Label:").grid(
            row=1, column=0, sticky="w", padx=4, pady=2
        )
        label_combo = ttk.Combobox(
            frame,
            textvariable=label_var,
            values=level_labels,
            state="readonly",
            width=10,
        )
        label_combo.grid(row=1, column=1, sticky="w", padx=4, pady=2)
        
        ttk.Label(frame, text="Index:").grid(
            row=1, column=2, sticky="w", padx=4, pady=2
        )
        index_spin = ttk.Spinbox(frame, from_=0, to=level_cnt-1, textvariable=index_var, width=4, command=_on_index_change)
        index_spin.grid(row=1, column=3, sticky="w", padx=4, pady=2)
        
        name_combo.bind("<<ComboboxSelected>>", _on_name_change)
        label_combo.bind("<<ComboboxSelected>>", _on_label_change)
    
    _build_side_frame(dialog, 0, "Levels", level_name_var, level_label_var, level_index_var)
    
    # Buttons
    btn_frame = ttk.Frame(dialog)
    btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
    ttk.Button(
        btn_frame,
        text="Select",
        command=lambda: [ret_val.set(level_index_var.get()), dialog.destroy()],
        width=10,
    ).grid(row=0, column=0, padx=8)
    ttk.Button(btn_frame, text="Cancel", command=dialog.destroy, width=10).grid(
        row=0, column=1, padx=8
    )
    
    # Wait and return
    dialog.bind(
        "<Return>", lambda e: [ret_val.set(level_index_var.get()), dialog.destroy()]
    )
    dialog.bind("<Escape>", lambda e: dialog.destroy())
    
    dialog.update_idletasks()
    dw, dh = dialog.winfo_width(), dialog.winfo_height()
    sw, sh = dialog.winfo_screenwidth(), dialog.winfo_screenheight()
    dialog.geometry(f"+{(sw - dw) // 2}+{(sh - dh) // 2}")
    dialog.wait_window()
    
    # Deal with parent
    if not parent_object:
        parent.destroy()
    
    return ret_val.get()

if __name__ == "__main__":
    import sys
    
    levels: list[LevelInfo] = [
        {"level_label": "Lv1", "level_name": "FirFirFirst"},
        {"level_label": "Lv67", "level_name": "SixSeven"},
        {"level_label": "Lv87", "level_name": "Bachi"}
    ]
    level_cnt = len(levels)
    
    level_index = 0
    argc = len(sys.argv)
    valid = False
    
    if argc == 2:
        try:
            level_index = int(sys.argv[1])
            if 0 <= level_index <= level_cnt-1:
                valid = True
            else:
                print(f"<index> must be between 0 and {level_cnt-1}, not {level_index}", file=sys.stderr)
        except ValueError as val_err:
            print(f"<index> must be int, not '{sys.argv[1]}'", file=sys.stderr)
    
    if not valid:
        print(f"Usage: {sys.argv[0]} <index(0~{level_cnt-1})>", file=sys.stderr)
        sys.exit(1)
    
    icon_path = ASSETS_DIR / "images/window_icon/mochicat.ico"
    print(icon_path.is_absolute())
    index_selected = tk_level_select(levels, level_index, icon_path=icon_path)
    print(f"Index selected: {index_selected}")
    