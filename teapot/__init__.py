from .cogs import *
from .managers import *
from .tools import *
from .config import *
from .events import *
from .messages import *
from .setup import *


def version():
    return "v0.0.1.5"


def config_version():
    return "0.1"


def time():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")


def year():
    import datetime
    return str(datetime.datetime.now().year)


def copyright():
    if year() == "2020":
        return "© 2020 RedCoke Development"
    else:
        return f"© 2020-{year()} RedCoke Development"


def platform():
    import platform
    return platform.system() + " " + platform.release()


def hostname():
    import socket
    return socket.gethostname()


def ip():
    import socket
    return socket.gethostbyname(hostname())


def path():
    import sys
    return sys.path
