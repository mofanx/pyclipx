#  Copyright 2021 Spencer Phillip Young
#  Copyright 2026 mofanx
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
import platform
import os
import sys

# Auto-detect and set environment variables for sudo on Wayland
if platform.system() == 'Linux' and hasattr(os, 'geteuid') and os.geteuid() == 0:
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        try:
            import pwd
            real_uid = str(pwd.getpwnam(sudo_user).pw_uid)
            os.environ.setdefault("WAYLAND_DISPLAY", "wayland-0")
            os.environ.setdefault("XDG_RUNTIME_DIR", f"/run/user/{real_uid}")
        except (KeyError, ImportError):
            pass

from .util import detect_clipboard
from .base import ClipboardSetupException
from functools import wraps
try:
    DEFAULT_CLIPBOARD = detect_clipboard()
except ClipboardSetupException as e:
    DEFAULT_CLIPBOARD = None
    _CLIPBOARD_EXCEPTION_TB = sys.exc_info()[2]

def wrapif(f):
    if DEFAULT_CLIPBOARD is not None:
        wrapped = getattr(DEFAULT_CLIPBOARD, f.__name__)
        wrapper = wraps(wrapped)
        return wrapper(f)
    return f

@wrapif
def copy(*args, **kwargs):
    if DEFAULT_CLIPBOARD is None:
        raise ClipboardSetupException("Could not setup clipboard").with_traceback(_CLIPBOARD_EXCEPTION_TB)
    return DEFAULT_CLIPBOARD.copy(*args, **kwargs)


@wrapif
def paste(*args, **kwargs):
    if DEFAULT_CLIPBOARD is None:
        raise ClipboardSetupException("Could not setup clipboard").with_traceback(_CLIPBOARD_EXCEPTION_TB)
    return DEFAULT_CLIPBOARD.paste(*args, **kwargs)


@wrapif
def clear(*args, **kwargs):
    if DEFAULT_CLIPBOARD is None:
        raise ClipboardSetupException("Could not setup clipboard").with_traceback(_CLIPBOARD_EXCEPTION_TB)
    return DEFAULT_CLIPBOARD.clear(*args, **kwargs)
