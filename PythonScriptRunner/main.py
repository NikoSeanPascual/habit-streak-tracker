import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import threading
import time
import os
import queue
import sys


class PythonSandboxV1:
    def __init__(self, root):
        self.root = root
        self.root.title("Niko's CRT Terminal | Dark Green Style")
        self.root.geometry("950x700")
        self.BG_DARK = "#050505"
        self.BG_MID = "#0a0a0a"
        self.ACCENT = "#00FF41"
        self.TEXT_DIM = "#008F11"
        self.ERROR = "#FF0000"
        self.FONT = ("Fixedsys", 12)
        self.FONT_SMALL = ("Fixedsys", 10)

        self.root.configure(bg=self.BG_DARK)

        self.process = None
        self.output_queue = queue.Queue()
        self.timeout_seconds = 30

        self.setup_ui()
        self.setup_shortcuts()
        self.poll_output()

    def setup_ui(self):
        header = tk.Frame(self.root, bg=self.BG_DARK, padx=10, pady=5)
        header.pack(fill=tk.X)

        tk.Label(header, text="> SOURCE:", fg=self.ACCENT, bg=self.BG_DARK, font=self.FONT_SMALL).pack(side=tk.LEFT)

        # Fixed: borderwidth and relief types
        self.path_entry = tk.Entry(header, bg=self.BG_MID, fg=self.ACCENT, insertbackground=self.ACCENT,
                                   font=self.FONT_SMALL, borderwidth=1, relief=tk.SOLID)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # Fixed: relief type
        tk.Button(header, text="[ BROWSE ]", command=self.browse_file, bg=self.BG_DARK, fg=self.ACCENT,
                  activebackground=self.ACCENT, activeforeground=self.BG_DARK,
                  font=self.FONT_SMALL, borderwidth=1, relief=tk.SOLID).pack(side=tk.LEFT)

        settings_row = tk.Frame(self.root, bg=self.BG_DARK, padx=10)
        settings_row.pack(fill=tk.X)

        tk.Label(settings_row, text="> ARGS:", fg=self.ACCENT, bg=self.BG_DARK, font=self.FONT_SMALL).pack(side=tk.LEFT)

        # Fixed: relief type
        self.args_entry = tk.Entry(settings_row, bg=self.BG_MID, fg=self.ACCENT, insertbackground=self.ACCENT,
                                   font=self.FONT_SMALL, borderwidth=1, relief=tk.SOLID)
        self.args_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Label(settings_row, text="LIMIT(s):", fg=self.ACCENT, bg=self.BG_DARK, font=self.FONT_SMALL).pack(
            side=tk.LEFT)

        # Fixed: relief type
        self.timeout_entry = tk.Entry(settings_row, bg=self.BG_MID, fg=self.ACCENT, insertbackground=self.ACCENT,
                                      width=5, borderwidth=1, relief=tk.SOLID, font=self.FONT_SMALL)
        self.timeout_entry.insert(0, "30")
        self.timeout_entry.pack(side=tk.LEFT, padx=5)

        ctrl_frame = tk.Frame(self.root, bg=self.BG_DARK, padx=10, pady=10)
        ctrl_frame.pack(fill=tk.X)

        # Fixed: relief in the btn_style dictionary
        btn_style = {"bg": self.BG_DARK, "fg": self.ACCENT, "activebackground": self.ACCENT,
                     "activeforeground": self.BG_DARK, "font": self.FONT, "relief": tk.SOLID, "borderwidth": 1}

        self.run_btn = tk.Button(ctrl_frame, text="[ EXECUTE ]", command=self.start_execution, **btn_style)
        self.run_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(ctrl_frame, text="[ ABORT ]", command=self.stop_execution, state=tk.DISABLED,
                                  **btn_style)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(ctrl_frame, text="[ PURGE ]", command=self.clear_console, **btn_style).pack(side=tk.LEFT, padx=5)

        # Fixed: relief type
        self.terminal = scrolledtext.ScrolledText(self.root, bg=self.BG_MID, fg=self.ACCENT, font=self.FONT,
                                                  insertbackground=self.ACCENT, borderwidth=1, relief=tk.SOLID,
                                                  padx=15, pady=15, undo=True)
        self.terminal.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.terminal.tag_config("stderr", foreground=self.ERROR)
        self.terminal.tag_config("system", foreground=self.ACCENT, font=("Fixedsys", 12, "bold"))

        self.terminal.bind("<Return>", self.handle_input)

        footer = tk.Frame(self.root, bg=self.BG_DARK)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_lbl = tk.Label(footer, text="SYSTEM_READY", bg=self.BG_DARK, fg=self.ACCENT, font=self.FONT_SMALL)
        self.status_lbl.pack(side=tk.LEFT, padx=10)

        self.timer_lbl = tk.Label(footer, text="0.00s", bg=self.BG_DARK, fg=self.TEXT_DIM, font=self.FONT_SMALL)
        self.timer_lbl.pack(side=tk.RIGHT, padx=10)

    # ... [Rest of your methods remain the same] ...
    def setup_shortcuts(self):
        self.root.bind('<Control-r>', lambda e: self.start_execution())
        self.root.bind('<Control-l>', lambda e: self.clear_console())

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if filename:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, filename)

    def handle_input(self, event):
        if self.process and self.process.poll() is None:
            input_text = self.terminal.get("insert linestart", "insert lineend")
            try:
                self.process.stdin.write(input_text + "\n")
                self.process.stdin.flush()
            except Exception as e:
                self.output_queue.put(("text", f"\n[!] STDIN_ERROR: {str(e)}\n", "stderr"))
        return None

    def start_execution(self):
        if self.process: return

        script_path = self.path_entry.get()
        if not os.path.exists(script_path):
            self.terminal.insert(tk.END, f"\n[!] ERROR: FILE_NOT_FOUND\n", "stderr")
            return

        try:
            self.timeout_seconds = int(self.timeout_entry.get())
        except ValueError:
            self.timeout_seconds = 30

        self.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_lbl.config(text="STATUS: EXECUTING...")

        args = self.args_entry.get().split()
        cmd = [sys.executable, "-u", script_path] + args

        self.terminal.insert(tk.END, f"\n>>> KERNEL_START: {time.strftime('%H:%M:%S')}\n", "system")
        threading.Thread(target=self.run_engine, args=(cmd,), daemon=True).start()

    def run_engine(self, cmd):
        start_time = time.time()
        try:
            self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                text=True, bufsize=1, universal_newlines=True,
                cwd=os.path.dirname(cmd[2]) if os.path.dirname(cmd[2]) else None
            )

            def read_pipe(pipe, tag):
                try:
                    for line in iter(pipe.readline, ''):
                        self.output_queue.put(("text", line, tag))
                finally:
                    pipe.close()

            threading.Thread(target=read_pipe, args=(self.process.stdout, None), daemon=True).start()
            threading.Thread(target=read_pipe, args=(self.process.stderr, "stderr"), daemon=True).start()

            while self.process.poll() is None:
                if (time.time() - start_time) > self.timeout_seconds:
                    self.stop_execution()
                    self.output_queue.put(
                        ("text", f"\n[!!!] KERNEL_HALT: TIMEOUT ({self.timeout_seconds}s)\n", "stderr"))
                    break
                time.sleep(0.1)

            exit_code = self.process.wait()
            self.output_queue.put(("finish", exit_code, time.time() - start_time))

        except Exception as e:
            self.output_queue.put(("text", f"\n[!] CRITICAL_FAILURE: {str(e)}\n", "stderr"))
            self.output_queue.put(("finish", 1, 0))

    def poll_output(self):
        try:
            while True:
                msg = self.output_queue.get_nowait()
                if msg[0] == "text":
                    self.terminal.insert(tk.END, msg[1], msg[2])
                    self.terminal.see(tk.END)
                elif msg[0] == "finish":
                    self.process = None
                    self.run_btn.config(state=tk.NORMAL)
                    self.stop_btn.config(state=tk.DISABLED)
                    self.status_lbl.config(text="SYSTEM_READY")
                    self.timer_lbl.config(text=f"{msg[2]:.2f}s")
        except queue.Empty:
            pass
        self.root.after(50, self.poll_output)

    def stop_execution(self):
        if self.process:
            self.process.kill()
            self.terminal.insert(tk.END, "\n[!] PROCESS_TERMINATED_BY_USER\n", "stderr")

    def clear_console(self):
        self.terminal.delete('1.0', tk.END)
        self.terminal.insert(tk.END, "> LOG_PURGED...\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = PythonSandboxV1(root)
    root.mainloop()