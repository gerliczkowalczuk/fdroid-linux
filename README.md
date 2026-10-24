# fdroid-linux

Ultra-lightweight Android & F-Droid application runner and compatibility layer for Linux desktop environments and handhelds (Steam Deck, laptops, workstations).

`fdroid-linux` provides two native interfaces:
1. **`fdroid` / `f-droid` (GUI)**: Directly launches the official, full-featured F-Droid Android client in native Wayland/X11 multi-window mode.
2. **`fdroid-cli` (CLI)**: A command-line tool for inspecting APKs, checking system readiness, and managing packages.

---

## Architecture

`fdroid-linux` uses the ultra-optimized **`andron`** translation engine:
- Direct pass-through from `SurfaceFlinger` to Wayland via Mesa DMA-BUF.
- Zero-copy low-latency audio via PipeWire.
- Minimal CPU and RAM footprint without heavy virtual machines.

---

## Installation & Packages

### AUR Packages
- **`fdroid` / `f-droid`**: The default GUI launcher.
- **`fdroid-cli`**: The command-line management interface.
- **`andron`**: The ultra-lightweight Android compatibility & translation runtime.

```bash
yay -S fdroid
# or for CLI only
yay -S fdroid-cli
```

---

## License

GPL-3.0-or-later © Oskar Gerlicz-Kowalczuk
