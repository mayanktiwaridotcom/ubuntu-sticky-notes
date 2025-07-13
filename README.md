# Ubuntu Sticky Notes

A simple, lightweight sticky notes application for the Ubuntu desktop, designed to be always on top of other windows.

![screenshot](https://i.imgur.com/R4iJ4Zt.png) <!-- Placeholder image -->

## Features

*   **Always on Top**: Notes stay visible over any other application.
*   **Multiple Notes**: Create up to six notes simultaneously.
*   **Rich Text Formatting**: Basic text styling with **Bold**, *Italic*, and Underline.
*   **Persistence**: Notes are automatically saved and restored when you restart the application.
*   **System Tray Integration**: Easily accessible from a system tray icon for creating new notes or quitting the app.

## Prerequisites

Before you begin, ensure you have the following dependencies installed on your Ubuntu or Debian-based system:

```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
```

## Installation

To install the application on your system, you can build and install the `.deb` package.

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone <repository-url>
cd ubuntu-sticky-notes
```

*(Replace `<repository-url>` with the actual URL once you upload it to GitHub.)*

### 2. Build the `.deb` Package

Run the following commands to create the Debian package file:

```bash
# Create the packaging directory structure
mkdir -p ../ubuntu-sticky-notes-pkg/DEBIAN
mkdir -p ../ubuntu-sticky-notes-pkg/usr/bin
mkdir -p ../ubuntu-sticky-notes-pkg/usr/share/applications
mkdir -p ../ubuntu-sticky-notes-pkg/usr/share/icons/hicolor/scalable/apps

# Copy the application script
cp main.py ../ubuntu-sticky-notes-pkg/usr/bin/sticky-notes

# Create the control file for package metadata
cat <<EOF > ../ubuntu-sticky-notes-pkg/DEBIAN/control
Package: sticky-notes
Version: 1.0
Architecture: all
Maintainer: Your Name <you@example.com>
Description: A simple sticky notes application for Ubuntu.
 Depends: python3-gi, gir1.2-gtk-3.0, gir1.2-ayatanaappindicator3-0.1
EOF

# Create the .desktop file for the application menu
cat <<EOF > ../ubuntu-sticky-notes-pkg/usr/share/applications/sticky-notes.desktop
[Desktop Entry]
Name=Sticky Notes
Exec=/usr/bin/sticky-notes
Icon=sticky-notes
Type=Application
Categories=Utility;
EOF

# Add an application icon
cat <<EOF > ../ubuntu-sticky-notes-pkg/usr/share/icons/hicolor/scalable/apps/sticky-notes.svg
<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><path fill="#ffeb3b" d="M10 10h44v44H10z"/><path fill="#fbc02d" d="M54 10v44L10 54V10h44m0-4H10c-2.21 0-4 1.79-4 4v44c0 2.21 1.79 4 4 4h44c2.21 0 4-1.79 4-4V10c0-2.21-1.79-4-4-4z"/></svg>
EOF

# Build the final .deb package
dpkg-deb --build ../ubuntu-sticky-notes-pkg
```

This will create a `ubuntu-sticky-notes-pkg.deb` file in the parent directory.

### 3. Install the Package

You can now install the application using `dpkg`:

```bash
sudo dpkg -i ../ubuntu-sticky-notes-pkg.deb
```

If you encounter any dependency issues, run the following command to fix them:

```bash
sudo apt-get install -f
```

## How to Use

After installation, you can find **"Sticky Notes"** in your system's application launcher.

Alternatively, the application will place an icon in your system tray. Right-click this icon to:
*   **New Note**: Create a new sticky note.
*   **Quit**: Close all notes and exit the application.

## For Developers

If you want to run the application directly from the source code without installing it:

1.  **Clone the repository.**
2.  **Install the prerequisites** (listed above).
3.  **Run the main script:**
    ```bash
    cd ubuntu-sticky-notes
    chmod +x main.py
    ./main.py
    ```
