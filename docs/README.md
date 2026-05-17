# PyClipX

Cross-platform clipboard utilities supporting both binary and text data.

This is a fork of the original [PyClip](https://github.com/spyoungtech/pyclip) project, maintained under Apache License 2.0. All functionality remains compatible with the original API.

## Why PyClipX?

This fork was created to fix clipboard compatibility issues when running with **sudo** on **Ubuntu 26.04 LTS** and other modern Linux distributions that use **pure Wayland** as the display server. While the original PyClip project works fine in non-root environments, it encounters issues when run with elevated privileges. This version focuses on:

- **Sudo compatibility** - fixes clipboard operations when running with sudo privileges on Wayland
- **Enhanced Wayland support** through the `wayland_clip.py` module, which provides clipboard functionality via `wl-copy`/`wl-paste` commands
- **Modern Linux compatibility** for systems that have moved away from X11 to Wayland

The `wayland_clip.py` module specifically handles clipboard operations on Wayland by leveraging the `wl-clipboard` package, which is the standard Wayland clipboard utility.

![PyPI Version](https://img.shields.io/pypi/v/pyclipx?color=blue)
![Python Versions](https://img.shields.io/pypi/pyversions/pyclipx)


Some key features include:

- A cross-platform API (supports MacOS, Windows, Linux)
- Can handle arbitrary binary data
- On Windows, some additional [clipboard formats](https://docs.microsoft.com/en-us/windows/win32/dataxchg/standard-clipboard-formats) 
are supported

## Installation

Requires python 3.7+

```bash
pip install pyclipx
```

## Usage

pyclip can be used in Python code
```python
import pyclip

pyclip.copy("hello clipboard") # copy data to the clipboard
cb_data = pyclip.paste() # retrieve clipboard contents 
print(cb_data)  # b'hello clipboard'
cb_text = pyclip.paste(text=True)  # paste as text
print(cb_text)  # 'hello clipboard'

pyclip.clear() # clears the clipboard contents
assert not pyclip.paste()
```

### Using with sudo on Wayland

When running with sudo on Wayland (e.g., Ubuntu 26.04 LTS), you need to set environment variables before importing pyclip:

```python
import platform
import os

if platform.system() == 'Linux' and hasattr(os, 'geteuid') and os.geteuid() == 0:
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        try:
            import pwd
            real_uid = str(pwd.getpwnam(sudo_user).pw_uid)
            os.environ.setdefault("WAYLAND_DISPLAY", "wayland-0")
            os.environ.setdefault("XDG_RUNTIME_DIR", f"/run/user/{real_uid}")
        except KeyError:
            pass

import pyclip

pyclip.copy("hello clipboard")
```

Or a CLI

```bash
# paste clipboard contents to stdout
python -m pyclip paste

# load contents to the clipboard from stdin
python -m pyclip copy < myfile.text
# same as above, but pipe from another command
some-program | python -m pyclip copy
```

Installing via pip also provides the console script `pyclip`:

```bash
pyclip copy < my_file.txt
```

This library implements functionality for several platforms and clipboard utilities. 

- [x] MacOS
- [x] Windows
- [x] Linux on x11 (with `xclip`)
- [x] Linux on wayland (with `wl-clipboard`)

If there is a platform or utility not currently listed, please request it by creating an issue.

## Platform specific notes/issues

### Windows

- On Windows, the `pywin32` package is installed as a requirement.
- On Windows, additional clipboard formats are supported, including copying from a file 
(like if you right-click copy from File Explorer)

### MacOS

MacOS has support for multiple backends. By default, the `pasteboard` package is used.

`pbcopy`/`pbpaste` can also be used as a backend, but does not support arbitrary binary data, which may lead to 
data being lost on copy/paste. This backend may be removed in a future release.

### Linux

Linux on X11 requires `xclip` to work. Install with your package manager, e.g. `sudo apt install xclip`
Linux on Wayland requires `wl-clipboard` to work. Install with your package manager, e.g. `sudo apt install wl-clipboard`

# Acknowledgements

Big thanks to [Howard Mao](https://github.com/zhemao) for donating the PyClip project name on PyPI to 
the original project.
