#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, AyatanaAppIndicator3, GObject, Pango
import os
import json

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "stickynotes")
NOTES_FILE = os.path.join(CONFIG_DIR, "notes.json")

class StickyNotesApp:
    def __init__(self):
        self.notes = []
        self.indicator = AyatanaAppIndicator3.Indicator.new(
            "StickyNotes",
            "emblem-default",
            AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self._build_menu())
        
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
            
        self.load_notes()


    def _build_menu(self):
        menu = Gtk.Menu()
        item_new_note = Gtk.MenuItem(label="New Note")
        item_quit = Gtk.MenuItem(label="Quit")

        item_new_note.connect("activate", self._on_new_note)
        item_quit.connect("activate", self._on_quit)

        menu.append(item_new_note)
        menu.append(Gtk.SeparatorMenuItem())
        menu.append(item_quit)
        menu.show_all()
        return menu

    def _on_new_note(self, _):
        if len(self.notes) < 6:
            print("Creating a new note...")
            note_window = NoteWindow()
            note_window.connect("destroy", self._on_note_closed)
            self.notes.append(note_window)
            note_window.show_all()
        else:
            print("Maximum number of notes reached.")

    def _on_note_closed(self, window):
        print("A note was closed.")
        self.notes.remove(window)
        self.save_notes()

    def _on_quit(self, _):
        self.save_notes()
        for note in self.notes:
            note.destroy()
        Gtk.main_quit()

    def save_notes(self):
        notes_data = []
        for note in self.notes:
            width, height = note.get_size()
            x, y = note.get_position()
            buffer = note.textview.get_buffer()
            content = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
            notes_data.append({
                "content": content,
                "width": width,
                "height": height,
                "x": x,
                "y": y
            })
        
        with open(NOTES_FILE, "w") as f:
            json.dump(notes_data, f)

    def load_notes(self):
        if not os.path.exists(NOTES_FILE):
            return

        with open(NOTES_FILE, "r") as f:
            notes_data = json.load(f)

        for note_data in notes_data:
            note_window = NoteWindow()
            note_window.connect("destroy", self._on_note_closed)
            self.notes.append(note_window)
            
            buffer = note_window.textview.get_buffer()
            buffer.set_text(note_data["content"])
            note_window.resize(note_data["width"], note_data["height"])
            note_window.move(note_data["x"], note_data["y"])
            
            note_window.show_all()

class NoteWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Sticky Note")
        self.set_default_size(300, 250)
        self.set_keep_above(True)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)

        self.buffer = self.textview.get_buffer()
        self.tag_bold = self.buffer.create_tag("bold", weight=700)
        self.tag_italic = self.buffer.create_tag("italic", style=Pango.Style.ITALIC)
        self.tag_underline = self.buffer.create_tag("underline", underline=Pango.Underline.SINGLE)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        toolbar = Gtk.Toolbar()
        vbox.pack_start(toolbar, False, True, 0)

        btn_bold = Gtk.ToolButton(stock_id=Gtk.STOCK_BOLD)
        toolbar.insert(btn_bold, -1)

        btn_italic = Gtk.ToolButton(stock_id=Gtk.STOCK_ITALIC)
        toolbar.insert(btn_italic, -1)

        btn_underline = Gtk.ToolButton(stock_id=Gtk.STOCK_UNDERLINE)
        toolbar.insert(btn_underline, -1)

        scrolled_window = Gtk.ScrolledWindow()
        vbox.pack_start(scrolled_window, True, True, 0)
        scrolled_window.add(self.textview)

        btn_bold.connect("clicked", self.on_format_button_clicked, self.tag_bold)
        btn_italic.connect("clicked", self.on_format_button_clicked, self.tag_italic)
        btn_underline.connect("clicked", self.on_format_button_clicked, self.tag_underline)

    def on_format_button_clicked(self, button, tag):
        bounds = self.buffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.buffer.apply_tag(tag, start, end)

if __name__ == "__main__":
    app = StickyNotesApp()
    GObject.threads_init()
    Gtk.main()
