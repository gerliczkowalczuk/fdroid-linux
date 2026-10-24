# fdroid-linux

Ultra-lightweight Android & F-Droid compatibility layer and native application runner for Linux desktop environments and handhelds (Steam Deck, laptops, workstations).

Like Valve's Proton translates Windows APIs for native Linux gaming, **fdroid-linux** seamlessly bridges Android Runtime (ART), Bionic libc, and Binder IPC directly to native Linux subsystems (Wayland, PipeWire, Vulkan/Mesa).

---

## Key Features

- **Zero-Overhead Graphics:** Direct frame-passing from Android SurfaceFlinger to Wayland compositors (Sway, GNOME, KDE Plasma, Hyprland).
- **Audio Bridge:** Native low-latency audio redirection into PipeWire / PulseAudio.
- **F-Droid Integration:** Search, fetch, and verify open-source APKs directly from official F-Droid repositories.
- **Proton-Like Simplicity:** Run any APK with a single command or double-click from your desktop environment.
- **Lightweight Architecture:** Minimal resource footprint written in Rust with direct kernel namespace isolation.

---

## Installation & Requirements

### Prerequisites
- Linux kernel 5.10+ (with `binderfs` or `binder` support)
- Wayland compositor (recommended) or X11
- Vulkan-capable GPU drivers (Mesa / RADV / ANV / Nvidia)

### Building from Source

```bash
git clone https://github.com/gerliczkowalczuk/fdroid-linux.git
cd fdroid-linux
cargo build --release
```

The resulting binary will be located at `target/release/fdroid-linux`.

---

## Usage

### 1. Check System Compatibility
```bash
fdroid-linux doctor
```

### 2. Inspect an APK Package
Inspect native architectures, manifest headers, and bytecode:
```bash
fdroid-linux inspect path/to/app.apk
```

### 3. Run an Android Application
```bash
fdroid-linux run path/to/app.apk
```

### 4. Fetch and Install Directly from F-Droid
```bash
fdroid-linux install org.fdroid.fdroid
```

---

## Architecture

```
+-------------------------------------------------------+
|                 Android APK (F-Droid)                 |
+-------------------------------------------------------+
                           |
+-------------------------------------------------------+
|             fdroid-linux Compatibility Layer          |
|  - DEX / ART Runtime Engine                           |
|  - Bionic <-> Glibc / Musl System Call Mapper         |
|  - Binder IPC <-> Unix Domain Sockets                 |
+-------------------------------------------------------+
        |                     |                    |
        v                     v                    v
+---------------+     +---------------+    +----------------+
|  Wayland / GL |     |   PipeWire    |    | Linux Kernel   |
| (Native Mesa) |     | (Direct Audio)|    | (Namespaces)   |
+---------------+     +---------------+    +----------------+
```

---

## License

GPL-3.0-or-later © Oskar Gerlicz-Kowalczuk
