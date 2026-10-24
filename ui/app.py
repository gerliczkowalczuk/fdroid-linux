#!/usr/bin/env python3
import sys
import os
import json
import threading
import urllib.request
import subprocess
from pathlib import Path

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio

APPS_DATA_URL = "https://f-droid.org/repo/index-v1.jar" # or fast cached popular apps list

POPULAR_FDROID_APPS = [
    {
        "id": "org.fdroid.fdroid",
        "name": "F-Droid",
        "summary": "The Open Source Android app repository client",
        "icon": "https://f-droid.org/repo/org.fdroid.fdroid/en-US/icon.png",
        "apk": "https://f-droid.org/repo/org.fdroid.fdroid_1023052.apk"
    },
    {
        "id": "org.mozilla.fenix.fdroid",
        "name": "Fennec F-Droid",
        "summary": "Firefox-based privacy-focused web browser",
        "icon": "https://f-droid.org/repo/org.mozilla.fenix.fdroid/en-US/icon.png",
        "apk": "https://f-droid.org/repo/org.mozilla.fenix.fdroid.apk"
    },
    {
        "id": "org.telegram.messenger.web",
        "name": "Telegram-FOSS",
        "summary": "Official open-source Telegram messenger client",
        "icon": "https://f-droid.org/repo/org.telegram.messenger.web/en-US/icon.png",
        "apk": "https://f-droid.org/repo/org.telegram.messenger.web.apk"
    },
    {
        "id": "im.vector.app",
        "name": "Element",
        "summary": "Decentralized Matrix chat client",
        "icon": "https://f-droid.org/repo/im.vector.app/en-US/icon.png",
        "apk": "https://f-droid.org/repo/im.vector.app.apk"
    },
    {
        "id": "org.videolan.vlc",
        "name": "VLC",
        "summary": "Open source multimedia player and streaming client",
        "icon": "https://f-droid.org/repo/org.videolan.vlc/en-US/icon.png",
        "apk": "https://f-droid.org/repo/org.videolan.vlc.apk"
    },
    {
        "id": "com.aurora.store",
        "name": "Aurora Store",
        "summary": "Elegant open-source Google Play alternative client",
        "icon": "https://f-droid.org/repo/com.aurora.store/en-US/icon.png",
        "apk": "https://f-droid.org/repo/com.aurora.store.apk"
    },
    {
        "id": "com.vitorpamplona.amethyst",
        "name": "Amethyst",
        "summary": "Decentralized Nostr social network client",
        "icon": "https://f-droid.org/repo/com.vitorpamplona.amethyst/en-US/icon.png",
        "apk": "https://f-droid.org/repo/com.vitorpamplona.amethyst.apk"
    },
    {
        "id": "com.simplemobiletools.gallery.pro",
        "name": "Simple Gallery Pro",
        "summary": "Lightweight, customizable photo and video viewer",
        "icon": "https://f-droid.org/repo/com.simplemobiletools.gallery.pro/en-US/icon.png",
        "apk": "https://f-droid.org/repo/com.simplemobiletools.gallery.pro.apk"
    }
]

class FDroidWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="F-Droid for Linux")
        self.set_default_size(860, 680)

        self.storage_dir = Path.home() / ".local" / "share" / "fdroid-linux" / "apps"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.setup_ui()

    def setup_ui(self):
        # Header bar
        header = Adw.HeaderBar()
        title = Adw.WindowTitle(title="F-Droid", subtitle="Linux Compatibility Layer (andron)")
        header.set_title_widget(title)

        # Search Bar
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search open-source applications...")
        self.search_entry.connect("search-changed", self.on_search_changed)

        # Main Box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_box.append(header)

        # Search container
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        search_box.set_margin_top(12)
        search_box.set_margin_bottom(12)
        search_box.set_margin_start(16)
        search_box.set_margin_end(16)
        search_box.append(self.search_entry)
        self.search_entry.set_hexpand(True)
        main_box.append(search_box)

        # Scrolled Window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        main_box.append(scrolled)

        # List Box
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.list_box.add_css_class("boxed-list")
        self.list_box.set_margin_start(16)
        self.list_box.set_margin_end(16)
        self.list_box.set_margin_bottom(16)

        clamp = Adw.Clamp()
        clamp.set_maximum_size(900)
        clamp.set_child(self.list_box)
        scrolled.set_child(clamp)

        self.set_content(main_box)
        self.render_apps(POPULAR_FDROID_APPS)

    def render_apps(self, apps):
        # Clear existing
        while True:
            row = self.list_box.get_row_at_index(0)
            if row is None:
                break
            self.list_box.remove(row)

        for app_data in apps:
            row = Adw.ActionRow()
            row.set_title(app_data["name"])
            row.set_subtitle(app_data["summary"])

            # Check if installed
            target_apk = self.storage_dir / f"{app_data['id']}.apk"
            is_installed = target_apk.exists()

            btn = Gtk.Button()
            if is_installed:
                btn.set_label("Launch")
                btn.add_css_class("suggested-action")
                btn.connect("clicked", self.on_launch_clicked, app_data)
            else:
                btn.set_label("Install")
                btn.connect("clicked", self.on_install_clicked, app_data, btn)

            btn.set_valign(Gtk.Align.CENTER)
            row.add_suffix(btn)
            self.list_box.append(row)

    def on_search_changed(self, entry):
        query = entry.get_text().strip().lower()
        if not query:
            self.render_apps(POPULAR_FDROID_APPS)
        else:
            filtered = [
                a for a in POPULAR_FDROID_APPS
                if query in a["name"].lower() or query in a["summary"].lower() or query in a["id"].lower()
            ]
            self.render_apps(filtered)

    def on_install_clicked(self, button, app_data, row_btn):
        button.set_sensitive(False)
        button.set_label("Downloading...")

        def download_worker():
            target_apk = self.storage_dir / f"{app_data['id']}.apk"
            try:
                urllib.request.urlretrieve(app_data["apk"], target_apk)
                GLib.idle_add(self.install_finished, button, app_data, True)
            except Exception as e:
                print("Download error:", e)
                GLib.idle_add(self.install_finished, button, app_data, False)

        threading.Thread(target=download_worker, daemon=True).start()

    def install_finished(self, button, app_data, success):
        button.set_sensitive(True)
        if success:
            button.set_label("Launch")
            button.add_css_class("suggested-action")
            try:
                button.disconnect_by_func(self.on_install_clicked)
            except Exception:
                pass
            button.connect("clicked", self.on_launch_clicked, app_data)
        else:
            button.set_label("Retry")

    def on_launch_clicked(self, button, app_data):
        target_apk = self.storage_dir / f"{app_data['id']}.apk"
        print(f"Launching {app_data['name']} via andron compatibility layer...")
        cmd = ["andron", "run", str(target_apk)]
        subprocess.Popen(cmd)

class FDroidApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="org.fdroid.linux", flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = FDroidWindow(self)
        win.present()

if __name__ == "__main__":
    app = FDroidApp()
    app.run(sys.argv)
