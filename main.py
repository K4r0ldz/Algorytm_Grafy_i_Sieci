#UI
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Wykres matplot jaki widget Tkintera
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

from src import logic, visualization


class App:
    # Rozmiar okna
    WIDTH = 1100
    HEIGHT = 750

    # Konstrukto
    def __init__(self):
        # Inicjalizacja głównego okna
        self.root = tk.Tk()
        self.root.title("Lokalizacja straży pożarnej")
        self._center_window()

        # Główny kontener, w którym będą zmieniane widoki
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Inicjalizacja zmiennych
        self.custom_graphs = []
        self.results = []
        self.result_idx = 0
        
        self._show_menu()
        self.root.mainloop()

    def _center_window(self):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = max(0, (sw - self.WIDTH) // 2)
        y = max(0, (sh - self.HEIGHT) // 2)
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

    def _clear(self):
        for child in self.container.winfo_children():
            child.destroy()

    def _show_menu(self):
        self._clear()
        tk.Label(self.container, text="Lokalizacja straży pożarnej",
                 font=("TkDefaultFont", 20, "bold")).pack(pady=60)
        tk.Label(self.container, text="Wybierz tryb:",
                 font=("TkDefaultFont", 13)).pack(pady=10)
        tk.Button(self.container, text="Uruchom z przykładowymi danymi",
                  command=self._run_sample, width=40, height=2).pack(pady=10)
        tk.Button(self.container, text="Wprowadź własne dane",
                  command=self._show_custom, width=40, height=2).pack(pady=10)

    def _show_custom(self):
        self._clear()
        self.custom_graphs = []

        tk.Label(self.container, text="Wprowadź własne dane",
                 font=("TkDefaultFont", 16, "bold")).pack(pady=10)

        is_directed_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.container, text="Graf skierowany",
                       variable=is_directed_var).pack(anchor="w", padx=20)

        tk.Label(self.container,
                 text="Krawędzie (jedna na linię, format: source,target,weight):"
                 ).pack(anchor="w", padx=20)
        text_input = scrolledtext.ScrolledText(self.container, width=70, height=15)
        text_input.pack(padx=20, pady=5)

        status_var = tk.StringVar(value="Dodano grafów: 0")
        tk.Label(self.container, textvariable=status_var,
                 font=("TkDefaultFont", 11, "italic")).pack()

        def add_graph():
            try:
                graph = logic.parse_edges(text_input.get("1.0", "end"), is_directed_var.get())
            except ValueError as exc:
                messagebox.showerror("Błąd wejścia", str(exc))
                return
            self.custom_graphs.append((graph, is_directed_var.get()))
            status_var.set(f"Dodano grafów: {len(self.custom_graphs)}")
            text_input.delete("1.0", "end")

        def run_algorithm():
            if not self.custom_graphs:
                messagebox.showinfo("Brak danych", "Najpierw dodaj co najmniej jeden graf.")
                return
            results = []
            for i, (graph, directed) in enumerate(self.custom_graphs, start=1):
                result = logic.compute_center(graph)
                results.append((graph, directed, f"Graf własny {i}", result))
            self._show_results(results)

        btn_frame = tk.Frame(self.container)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Dodaj graf do listy",
                  command=add_graph, width=22).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Uruchom algorytm",
                  command=run_algorithm, width=22).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Wstecz do menu",
                  command=self._show_menu, width=22).pack(side="left", padx=5)

    def _run_sample(self):
        data, is_directed = logic.dataReader()
        results = []
        for gid in data:
            result = logic.compute_center(data[gid])
            results.append((data[gid], is_directed[gid], f"Graf {gid}", result))
        self._show_results(results)

    def _show_results(self, results):
        self.results = results
        self.result_idx = 0
        self._clear()

        self.title_var = tk.StringVar()
        tk.Label(self.container, textvariable=self.title_var,
                 font=("TkDefaultFont", 16, "bold")).pack(pady=5)

        self.info_var = tk.StringVar()
        tk.Label(self.container, textvariable=self.info_var,
                 font=("TkDefaultFont", 12)).pack(pady=2)

        self.canvas_frame = tk.Frame(self.container)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

        btn_frame = tk.Frame(self.container)
        btn_frame.pack(pady=10)
        self.prev_btn = tk.Button(btn_frame, text="← Poprzedni",
                                  command=self._prev, width=18)
        self.prev_btn.pack(side="left", padx=5)
        self.next_btn = tk.Button(btn_frame, text="Następny graf →",
                                  command=self._next, width=18)
        self.next_btn.pack(side="left", padx=5)
        tk.Button(btn_frame, text="Wstecz do menu",
                  command=self._show_menu, width=18).pack(side="left", padx=5)

        self._render_current()

    def _render_current(self):
        for child in self.canvas_frame.winfo_children():
            child.destroy()

        graph, directed, graph_id, result = self.results[self.result_idx]
        counter = f"({self.result_idx + 1}/{len(self.results)})"
        self.title_var.set(f"{graph_id} {counter}")

        if result is None:
            self.info_var.set("Graf jest niespójny — brak centrum.")
            fig = visualization.build_figure(graph, directed=directed, title=graph_id)
        else:
            start, extreme, min_dist, prev = result
            self.info_var.set(f"Start: {start}    Najdalej: {extreme}    Odległość: {min_dist}")
            fig = visualization.build_figure(graph, start_vertex=start, directed=directed,
                                             title=graph_id, previous_vertex=prev)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.prev_btn.config(state="normal" if self.result_idx > 0 else "disabled")
        self.next_btn.config(
            state="normal" if self.result_idx + 1 < len(self.results) else "disabled")

    def _next(self):
        if self.result_idx + 1 < len(self.results):
            self.result_idx += 1
            self._render_current()

    def _prev(self):
        if self.result_idx > 0:
            self.result_idx -= 1
            self._render_current()


if __name__ == "__main__":
    App()
