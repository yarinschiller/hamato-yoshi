"""
Demonstrates a Rich "application" using the Layout and Live classes.
"""
import logging
from datetime import datetime
from time import sleep
from typing import Tuple, List, Dict

import psutil as psutil
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.logging import RichHandler
from rich.panel import Panel
from rich.style import Style
from rich.table import Table

CYBER_LEVELS_TITLES = ["NORMAL", "WARNING", "HIGH"]
CYBER_LEVEL_STYLES = [Style(color="green", blink=True, bold=True),
                      Style(color="yellow", blink=False, bold=True),
                      Style(color="red", blink=True, bold=True), ]

console = Console()





# class HamatoYoshiLogger(logging.Logger):
#     def

class PanelLogsHandler(RichHandler, Panel):
    def __init__(self, panel_name, *args, color=None):
        RichHandler.__init__(self, *args)
        self.panel_name = panel_name
        self.color = color
        self.logs = []

    def emit(self, record):
        self.logs.insert(0, self.format(record))

    def __rich__(self) -> Panel:
        return Panel(renderable="\n".join(self.logs),
                     highlight=True,
                     title=self.panel_name,
                     border_style=Style(color=self.color))


general_logger = logging.getLogger("rich")
general_logger.setLevel(logging.INFO)
general_logs_panel = PanelLogsHandler("Logs")
general_logger.addHandler(general_logs_panel)


def get_logger_and_panel(subject_name: str) -> Tuple[logging.Logger, Panel]:
    subject_logger = logging.getLogger(subject_name)
    subject_logger.setLevel(logging.DEBUG)
    subject_panel = PanelLogsHandler(subject_name, color=SUBJECT_COLORS[subject_name])
    # subject_logger.addHandler(general_logs_panel)
    subject_logger.addHandler(subject_panel)
    return subject_logger, subject_panel


SubjectName = str
SUBJECT_NAME_MEMORY: SubjectName = 'Memory'
SUBJECT_NAME_PROCESSES: SubjectName = 'Processes / Threads'
SUBJECT_NAME_PERMISSIONS: SubjectName = 'Permissions'
SUBJECT_NAME_CHANGES: SubjectName = 'Global Changes'
SUBJECT_NAME_FILES: SubjectName = 'Files / Sockets / Pipes'
SUBJECT_NAME_NETWORK: SubjectName = 'Network'
SUBJECT_NAME_LOGS: SubjectName = 'Logs'
SUBJECT_NAMES: List[SubjectName] = [
    SUBJECT_NAME_MEMORY,
    SUBJECT_NAME_PROCESSES,
    SUBJECT_NAME_PERMISSIONS,
    SUBJECT_NAME_CHANGES,
    SUBJECT_NAME_FILES,
    SUBJECT_NAME_NETWORK,
]
SUBJECT_COLORS: Dict[SubjectName, str] = {
    SUBJECT_NAME_MEMORY: 'cyan',
    SUBJECT_NAME_PROCESSES: 'blue',
    SUBJECT_NAME_PERMISSIONS: 'green',
    SUBJECT_NAME_CHANGES: 'yellow',
    SUBJECT_NAME_FILES: 'magenta',
    SUBJECT_NAME_NETWORK: 'red',
}

SUBJECT_LOGGERS_AND_PANELS = {subject_name: get_logger_and_panel(subject_name) for subject_name in SUBJECT_NAMES}


def subject_logger(subject_name: SubjectName) -> logging.Logger:
    return SUBJECT_LOGGERS_AND_PANELS[subject_name][0]


memory_logger = subject_logger(SUBJECT_NAME_MEMORY)
processes_logger = subject_logger(SUBJECT_NAME_PROCESSES)
permissions_logger = subject_logger(SUBJECT_NAME_PERMISSIONS)
changes_logger = subject_logger(SUBJECT_NAME_CHANGES)
files_logger = subject_logger(SUBJECT_NAME_FILES)
network_logger = subject_logger(SUBJECT_NAME_NETWORK)


def subject_panel(subject_name: str) -> Panel:
    return SUBJECT_LOGGERS_AND_PANELS[subject_name][1]


def make_dashboard() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer")
    )
    layout["main"].split_row(
        *[Layout(name=subject_name) for subject_name in SUBJECT_NAMES]
    )
    layout["footer"].split_row(
        Layout(name="logs"),
        Layout(name="stats")
    )
    return layout


class Header:
    """Display header with clock."""

    def __init__(self, cyber_level):
        self.cyber_level = cyber_level

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify='center', ratio=1)
        grid.add_column(justify='right', ratio=1)
        grid.add_row(
            f"[dim] [white]Hamato Yoshi v1.0.0[/]",
            f"[dim] [white]Cyber Level:[/] {CYBER_LEVELS_TITLES[self.cyber_level]}",
            f"[dim] [white]{datetime.now().ctime().replace(':', '[white blink]:[/]')}[/]",
        )
        return Panel(grid, style=CYBER_LEVEL_STYLES[self.cyber_level])


def rule_panel(rule_num) -> Panel:
    return Panel(renderable="", highlight=True, title=f"Rule #{rule_num}", border_style="blue")


def log_hamato_yoshi(subject_name: SubjectName, title: str, msg: str):
    color = SUBJECT_COLORS[subject_name]
    now = datetime.now()
    time = f"{now.hour}:{now.minute}:{now.second:02}"
    general_logger.info(f'[dim] [{color}]{time}[/dim] - [bold]{title}[/bold] - [{color} dim]{msg}[/]')
    subject_logger(subject_name).info(f'[dim] [{color}]{time}[/dim] - [bold]{title}[/]')


def stats_panel() -> Panel:
    # !/usr/bin/env python
    # gives a single float value
    cpu = psutil.cpu_percent()
    # gives an object with many fields
    ram = psutil.virtual_memory()
    # you can convert that object to a dictionary
    ram = dict(psutil.virtual_memory()._asdict())
    ram_total = psutil.virtual_memory().total
    # you can have the percentage of used RAM
    ram_used = psutil.virtual_memory().percent
    # you can calculate percentage of available memory
    ram_available = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    return Panel(f"CPU Usage: %{cpu:02}\n"
                 f"RAM Usage: %{ram_used:02}\n"
                 f"RAM Total: {ram_total}\n"
                 f"RAM Avail: {ram_available}",
                 title="Stats")


def refresh_dashboard(layout, cyber_level=0):
    layout["header"].update(Header(cyber_level=cyber_level))
    for subject_name in SUBJECT_NAMES:
        panel = subject_panel(subject_name)
        panel.color = SUBJECT_COLORS[subject_name]
        layout[subject_name].update(panel)
    layout["logs"].update(general_logs_panel)
    layout["stats"].update(stats_panel())


if __name__ == "__main__":
    layout = make_dashboard()
    with Live(layout, refresh_per_second=10, screen=True):
        i = 0
        while True:
            sleep(0.1)
            refresh_dashboard(layout)
            if (i % 5 == 0):
                log_hamato_yoshi(subject_name=SUBJECT_NAME_MEMORY,
                                 title='Meminfo.Memtotal',
                                 msg='total memory exceeded 1000Mb')
            if (i % 7 == 0):
                log_hamato_yoshi(subject_name=SUBJECT_NAME_NETWORK,
                                 title='Network.Packets',
                                 msg='sent too many packets')
            if (i % 8 == 0):
                log_hamato_yoshi(subject_name=SUBJECT_NAME_FILES,
                                 title="Files.lot",
                                 msg="Too many files open")
            i += 1
