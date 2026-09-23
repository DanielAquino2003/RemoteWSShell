import fcntl
import os
import pty
import struct
import termios


class PTYManager:
    def __init__(self):
        self.pid = None
        self.master_fd = None

    def start(self):
        pid, master_fd = pty.fork()

        if pid == 0:
            os.environ["TERM"] = "xterm-256color"
            os.execlp("bash", "bash", "-i")

        self.pid = pid
        self.master_fd = master_fd

    def resize(self, rows: int, cols: int):
        winsize = struct.pack("HHHH", rows, cols, 0, 0)
        fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, winsize)

    def write(self, data: bytes):
        os.write(self.master_fd, data)

    def read(self, size=4096):
        return os.read(self.master_fd, size)
