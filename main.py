"""
main.py
=======
Entry point for the Legal Contract Analyzer.
Builds the tkinter GUI and wires it to the ContractAnalyzer engine.

Run:
    python main.py
"""

from __future__ import annotations

import textwrap
import threading
import tkinter as tk
from tkinter import filedialog, font, messagebox, scrolledtext, ttk
from typing import List, Optional

from analyzer import ContractAnalyzer, RiskFinding
from risk_patterns import SEVERITY_COLORS


# ═══════════════════════════════════════════════════════════════════════════════
# Theme constants
# ═══════════════════════════════════════════════════════════════════════════════

THEME = {
    "bg_dark":      "#0d1117",
    "bg_panel":     "#161b22",
    "bg_card":      "#1c2128",
    "bg_input":     "#21262d",
    "border":       "#30363d",
    "text_primary": "#e6edf3",
    "text_muted":   "#7d8590",
    "accent":       "#1f6feb",
    "accent_hover": "#388bfd",
    "success":      "#3fb950",
    "btn_text":     "#ffffff",
}

SEV_BG = {
    "CRITICAL": "#3d1a1a",
    "HIGH":     "#3d2b1a",
    "MEDIUM":   "#3d370a",
    "LOW":      "#0d2540",
}

WRAP_WIDTH = 90   # characters for text wrapping in detail panel


# ═══════════════════════════════════════════════════════════════════════════════
# Main Application
# ═══════════════════════════════════════════════════════════════════════════════

class LegalAnalyzerApp:
    """Root application window."""

    APP_TITLE   = "⚖  Legal Contract Risk Analyzer"
    APP_VERSION = "v1.0.0  |  Prototype"
    MIN_W, MIN_H = 1100, 720

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(self.APP_TITLE)
        self.root.minsize(self.MIN_W, self.MIN_H)
        self.root.configure(bg=THEME["bg_dark"])

        self._analyzer = ContractAnalyzer()
        self._findings: List[RiskFinding] = []
        self._file_path: Optional[str] = None
        self._selected_finding: Optional[RiskFinding] = None

        self._build_fonts()
        self._build_layout()
        self._apply_treeview_style()

    # ── Fonts ────────────────────────────────────────────────────────────────

    def _build_fonts(self) -> None:
        self.f_title   = font.Font(family="Segoe UI",    size=15, weight="bold")
        self.f_heading = font.Font(family="Segoe UI",    size=11, weight="bold")
        self.f_body    = font.Font(family="Segoe UI",    size=10)
        self.f_mono    = font.Font(family="Courier New", size=9)
        self.f_badge   = font.Font(family="Segoe UI",    size=9, weight="bold")
        self.f_small   = font.Font(family="Segoe UI",    size=8)

    # ── Layout ───────────────────────────────────────────────────────────────

    def _build_layout(self) -> None:
        # ── Top bar ──────────────────────────────────────────────────────────
        self._build_topbar()

        # ── Main pane (left list | right detail) ─────────────────────────────
        paned = tk.PanedWindow(
            self.root, orient=tk.HORIZONTAL,
            bg=THEME["bg_dark"], sashwidth=5,
            sashrelief=tk.FLAT,
        )
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        left = self._build_left_panel(paned)
        right = self._build_right_panel(paned)

        paned.add(left,  minsize=420)
        paned.add(right, minsize=360)

        # ── Status bar ───────────────────────────────────────────────────────
        self._build_statusbar()

    def _build_topbar(self) -> None:
        bar = tk.Frame(self.root, bg=THEME["bg_panel"],
                       highlightthickness=1,
                       highlightbackground=THEME["border"])
        bar.pack(fill=tk.X, padx=10, pady=(10, 6))

        # Logo / title
        tk.Label(
            bar, text="⚖", font=("Segoe UI", 20),
            bg=THEME["bg_panel"], fg=THEME["accent"],
        ).pack(side=tk.LEFT, padx=(14, 4), pady=8)

        title_frame = tk.Frame(bar, bg=THEME["bg_panel"])
        title_frame.pack(side=tk.LEFT, pady=6)
        tk.Label(
            title_frame, text="Legal Contract Risk Analyzer",
            font=self.f_title, bg=THEME["bg_panel"], fg=THEME["text_primary"],
        ).pack(anchor=tk.W)
        tk.Label(
            title_frame, text=self.APP_VERSION,
            font=self.f_small, bg=THEME["bg_panel"], fg=THEME["text_muted"],
        ).pack(anchor=tk.W)

        # Severity legend
        legend = tk.Frame(bar, bg=THEME["bg_panel"])
        legend.pack(side=tk.RIGHT, padx=14)
        for sev, colour in SEVERITY_COLORS.items():
            dot = tk.Label(legend, text="●", fg=colour,
                           bg=THEME["bg_panel"], font=self.f_badge)
            dot.pack(side=tk.LEFT, padx=(0, 1))
            lbl = tk.Label(legend, text=sev, fg=THEME["text_muted"],
                           bg=THEME["bg_panel"], font=self.f_small)
            lbl.pack(side=tk.LEFT, padx=(0, 10))

        # Buttons
        btn_frame = tk.Frame(bar, bg=THEME["bg_panel"])
        btn_frame.pack(side=tk.RIGHT, padx=(0, 4))

        self._btn_open = self._make_button(
            btn_frame, "📂  Open Contract", self._open_file,
            THEME["accent"], THEME["accent_hover"],
        )
        self._btn_open.pack(side=tk.LEFT, padx=4, pady=8)

        self._btn_analyze = self._make_button(
            btn_frame, "🔍  Analyze", self._run_analysis,
            "#238636", "#2ea043",
            state=tk.DISABLED,
        )
        self._btn_analyze.pack(side=tk.LEFT, padx=4, pady=8)

        self._btn_clear = self._make_button(
            btn_frame, "🗑  Clear", self._clear_all,
            "#6e7681", "#8b949e",
        )
        self._btn_clear.pack(side=tk.LEFT, padx=4, pady=8)

    def _build_left_panel(self, parent) -> tk.Frame:
        frame = tk.Frame(parent, bg=THEME["bg_dark"])

        # Summary badges row
        self._summary_frame = tk.Frame(frame, bg=THEME["bg_dark"])
        self._summary_frame.pack(fill=tk.X, pady=(4, 6))
        self._summary_labels: dict = {}
        for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            card = tk.Frame(
                self._summary_frame, bg=SEV_BG[sev],
                highlightthickness=1,
                highlightbackground=SEVERITY_COLORS[sev],
            )
            card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)
            tk.Label(card, text=sev, font=self.f_badge,
                     bg=SEV_BG[sev], fg=SEVERITY_COLORS[sev]).pack(pady=(6, 0))
            num_lbl = tk.Label(card, text="—", font=("Segoe UI", 18, "bold"),
                               bg=SEV_BG[sev], fg=SEVERITY_COLORS[sev])
            num_lbl.pack(pady=(0, 6))
            self._summary_labels[sev] = num_lbl

        # Filter row
        filter_frame = tk.Frame(frame, bg=THEME["bg_dark"])
        filter_frame.pack(fill=tk.X, pady=(0, 4))
        tk.Label(filter_frame, text="Filter:", font=self.f_body,
                 bg=THEME["bg_dark"], fg=THEME["text_muted"]).pack(side=tk.LEFT, padx=(2, 4))

        self._filter_var = tk.StringVar(value="ALL")
        for sev in ("ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"):
            rb = tk.Radiobutton(
                filter_frame, text=sev, variable=self._filter_var, value=sev,
                command=self._apply_filter,
                bg=THEME["bg_dark"], fg=SEVERITY_COLORS.get(sev, THEME["text_primary"]),
                selectcolor=THEME["bg_card"], activebackground=THEME["bg_dark"],
                font=self.f_badge, relief=tk.FLAT,
            )
            rb.pack(side=tk.LEFT, padx=3)

        # Treeview (findings list)
        tree_frame = tk.Frame(
            frame, bg=THEME["bg_panel"],
            highlightthickness=1, highlightbackground=THEME["border"],
        )
        tree_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("severity", "category", "preview")
        self._tree = ttk.Treeview(
            tree_frame, columns=cols, show="headings",
            selectmode="browse",
        )
        self._tree.heading("severity",  text="Severity",  anchor=tk.W)
        self._tree.heading("category",  text="Category",  anchor=tk.W)
        self._tree.heading("preview",   text="Clause preview", anchor=tk.W)
        self._tree.column("severity",  width=90,  stretch=False)
        self._tree.column("category",  width=170, stretch=False)
        self._tree.column("preview",   width=300, stretch=True)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL,
                            command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        # Colour tags per severity
        for sev, colour in SEVERITY_COLORS.items():
            self._tree.tag_configure(sev, foreground=colour,
                                     background=SEV_BG[sev])

        return frame

    def _build_right_panel(self, parent) -> tk.Frame:
        frame = tk.Frame(parent, bg=THEME["bg_panel"],
                         highlightthickness=1,
                         highlightbackground=THEME["border"])

        tk.Label(
            frame, text="Risk Detail", font=self.f_heading,
            bg=THEME["bg_panel"], fg=THEME["text_primary"],
        ).pack(anchor=tk.W, padx=14, pady=(10, 2))

        self._detail_text = scrolledtext.ScrolledText(
            frame, wrap=tk.WORD, state=tk.DISABLED,
            bg=THEME["bg_card"], fg=THEME["text_primary"],
            font=self.f_body, relief=tk.FLAT,
            insertbackground=THEME["text_primary"],
            selectbackground=THEME["accent"],
            padx=10, pady=10,
        )
        self._detail_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # Configure text tags for rich formatting
        self._detail_text.tag_configure("heading",  font=self.f_heading,
                                         foreground=THEME["text_primary"])
        self._detail_text.tag_configure("label",    font=self.f_badge,
                                         foreground=THEME["text_muted"])
        self._detail_text.tag_configure("value",    font=self.f_body,
                                         foreground=THEME["text_primary"])
        self._detail_text.tag_configure("mono",     font=self.f_mono,
                                         foreground="#79c0ff")
        self._detail_text.tag_configure("rec",      font=self.f_body,
                                         foreground=THEME["success"])
        for sev, colour in SEVERITY_COLORS.items():
            self._detail_text.tag_configure(f"sev_{sev}", font=self.f_badge,
                                             foreground=colour)

        self._show_placeholder()
        return frame

    def _build_statusbar(self) -> None:
        bar = tk.Frame(self.root, bg=THEME["bg_panel"], height=26,
                       highlightthickness=1,
                       highlightbackground=THEME["border"])
        bar.pack(fill=tk.X, padx=10, pady=(0, 10))
        bar.pack_propagate(False)

        self._status_var = tk.StringVar(value="Ready. Open a contract to begin.")
        tk.Label(
            bar, textvariable=self._status_var,
            font=self.f_small, bg=THEME["bg_panel"], fg=THEME["text_muted"],
            anchor=tk.W,
        ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            bar, text="Powered by spaCy NLP  |  Rule-based risk engine",
            font=self.f_small, bg=THEME["bg_panel"], fg=THEME["text_muted"],
        ).pack(side=tk.RIGHT, padx=10)

    # ── Button factory ───────────────────────────────────────────────────────

    def _make_button(self, parent, text, command, bg, hover_bg,
                     state=tk.NORMAL) -> tk.Button:
        btn = tk.Button(
            parent, text=text, command=command,
            bg=bg, fg=THEME["btn_text"],
            font=self.f_badge, relief=tk.FLAT,
            padx=12, pady=5, cursor="hand2", state=state,
            activebackground=hover_bg, activeforeground=THEME["btn_text"],
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    # ── TreeView styling ─────────────────────────────────────────────────────

    def _apply_treeview_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=THEME["bg_panel"],
                        foreground=THEME["text_primary"],
                        fieldbackground=THEME["bg_panel"],
                        rowheight=28,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                        background=THEME["bg_card"],
                        foreground=THEME["text_muted"],
                        font=("Segoe UI", 9, "bold"),
                        relief=tk.FLAT)
        style.map("Treeview",
                  background=[("selected", THEME["accent"])],
                  foreground=[("selected", "#ffffff")])
        style.configure("Vertical.TScrollbar",
                        background=THEME["bg_card"],
                        troughcolor=THEME["bg_panel"],
                        arrowcolor=THEME["text_muted"])

    # ── Actions ──────────────────────────────────────────────────────────────

    def _open_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Select Contract File",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files",  "*.*"),
            ],
        )
        if not path:
            return
        self._file_path = path
        short = path.split("/")[-1] or path.split("\\")[-1]
        self._status_var.set(f"Loaded: {short}  —  Click 'Analyze' to scan for risks.")
        self._btn_analyze.config(state=tk.NORMAL)
        self._clear_results()

    def _run_analysis(self) -> None:
        if not self._file_path:
            return

        self._status_var.set("⏳  Analyzing… please wait.")
        self._btn_analyze.config(state=tk.DISABLED)
        self._btn_open.config(state=tk.DISABLED)

        def _worker():
            try:
                with open(self._file_path, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
                findings = self._analyzer.analyze(text)
                self.root.after(0, self._display_results, findings)
            except Exception as exc:  # noqa: BLE001
                self.root.after(
                    0,
                    lambda: messagebox.showerror("Analysis Error", str(exc)),
                )
                self.root.after(0, self._restore_buttons)

        threading.Thread(target=_worker, daemon=True).start()

    def _display_results(self, findings: List[RiskFinding]) -> None:
        self._findings = findings
        self._populate_tree(findings)
        self._update_summary(findings)

        total = len(findings)
        critical = sum(1 for f in findings if f.severity == "CRITICAL")
        msg = (
            f"✅  Analysis complete — {total} risk(s) found"
            + (f"  ·  ⚠ {critical} CRITICAL" if critical else "")
        )
        self._status_var.set(msg)
        self._restore_buttons()

    def _populate_tree(self, findings: List[RiskFinding]) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)

        for finding in findings:
            preview = finding.sentence[:80].replace("\n", " ")
            if len(finding.sentence) > 80:
                preview += "…"
            self._tree.insert(
                "", tk.END,
                values=(finding.severity, finding.category, preview),
                tags=(finding.severity,),
                iid=str(id(finding)),
            )

        # Store mapping iid → finding
        self._iid_map = {str(id(f)): f for f in findings}

    def _apply_filter(self) -> None:
        sev = self._filter_var.get()
        filtered = (
            self._findings if sev == "ALL"
            else [f for f in self._findings if f.severity == sev]
        )
        self._populate_tree(filtered)
        self._show_placeholder()

    def _update_summary(self, findings: List[RiskFinding]) -> None:
        counts = {s: 0 for s in ("CRITICAL", "HIGH", "MEDIUM", "LOW")}
        for f in findings:
            counts[f.severity] += 1
        for sev, lbl in self._summary_labels.items():
            lbl.config(text=str(counts[sev]))

    def _on_select(self, _event=None) -> None:
        selected = self._tree.selection()
        if not selected:
            return
        iid = selected[0]
        finding = self._iid_map.get(iid)
        if finding:
            self._show_detail(finding)

    # ── Detail panel ─────────────────────────────────────────────────────────

    def _show_detail(self, finding: RiskFinding) -> None:
        dt = self._detail_text
        dt.config(state=tk.NORMAL)
        dt.delete("1.0", tk.END)

        sev_tag = f"sev_{finding.severity}"

        dt.insert(tk.END, f"  {finding.severity}  ", (sev_tag,))
        dt.insert(tk.END, f"  {finding.category}\n\n", ("heading",))

        dt.insert(tk.END, "MATCHED PATTERN\n", ("label",))
        dt.insert(tk.END, f'  "{finding.pattern_matched}"\n\n', ("mono",))

        dt.insert(tk.END, "CLAUSE  (sentence #{:d})\n".format(finding.sentence_index),
                  ("label",))
        wrapped = textwrap.fill(finding.sentence, width=WRAP_WIDTH)
        dt.insert(tk.END, f"  {wrapped}\n\n", ("value",))

        dt.insert(tk.END, "WHY THIS IS RISKY\n", ("label",))
        wrapped_exp = textwrap.fill(finding.explanation, width=WRAP_WIDTH)
        dt.insert(tk.END, f"  {wrapped_exp}\n\n", ("value",))

        dt.insert(tk.END, "RECOMMENDATION\n", ("label",))
        wrapped_rec = textwrap.fill(finding.recommendation, width=WRAP_WIDTH)
        dt.insert(tk.END, f"  {wrapped_rec}\n", ("rec",))

        dt.config(state=tk.DISABLED)

    def _show_placeholder(self) -> None:
        dt = self._detail_text
        dt.config(state=tk.NORMAL)
        dt.delete("1.0", tk.END)
        dt.insert(tk.END,
                  "\n\n  Select a finding from the list\n"
                  "  to view its detailed analysis\n"
                  "  and recommendations here.",
                  ("label",))
        dt.config(state=tk.DISABLED)

    # ── Utilities ────────────────────────────────────────────────────────────

    def _clear_results(self) -> None:
        self._findings = []
        self._iid_map = {}
        for item in self._tree.get_children():
            self._tree.delete(item)
        for lbl in self._summary_labels.values():
            lbl.config(text="—")
        self._show_placeholder()

    def _clear_all(self) -> None:
        self._file_path = None
        self._clear_results()
        self._btn_analyze.config(state=tk.DISABLED)
        self._status_var.set("Ready. Open a contract to begin.")

    def _restore_buttons(self) -> None:
        self._btn_analyze.config(state=tk.NORMAL)
        self._btn_open.config(state=tk.NORMAL)

    # ── Run ──────────────────────────────────────────────────────────────────

    def run(self) -> None:
        self.root.mainloop()


# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = LegalAnalyzerApp()
    app.run()
