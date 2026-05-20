# droidFetch (dfetch) 📱

A highly customizable, fast, and lightweight system information tool specifically designed for Android environments, `droidFetch` provides a beautiful, `neofetch`-style terminal overview of your device's software and hardware.

## ✨ Features

* **Deep ROM/Distro Detection:** Automatically recognizes major Android distributions, manufacturer skins, and custom ROMs via system properties (`getprop`).
* **Beautiful ASCII Logos:** Built-in custom ASCII art and color palettes for over 15 different Android interfaces.(!!SOME IS HANDMADE SO MAYBE LOW QUALITY!!)
* **Tablet / Horizontal Mode:** Switch to a horizontal layout optimized for tablets, wide screens, or desktop modes.
* **Highly Customizable:** Easily override colors, force specific distro logos, or use your own custom ASCII art via a configuration file.
* **Lightweight:** Written in pure Python 3 with no heavy external dependencies.

## 🚀 Supported Distributions

`droidFetch` currently recognizes and provides custom ASCII logos for:
* Xiaomi HyperOS / MIUI
* EMUI / HarmonyOS / MagicOS
* ColorOS / OxygenOS / OriginOS / FuntouchOS
* Samsung One UI
* Meizu Flyme OS
* Nothing OS
* Pixel UI / Pixel Experience
* LineageOS / Evolution X / crDroid / Paranoid Android / GrapheneOS

## 🛠️ Installation

Since `droidFetch` relies on Android system commands (like `getprop`), it is intended to be run directly on an Android device (e.g., via [Termux](https://termux.dev/)).

1. Clone the repository:
   git clone https://github.com/yourusername/droidFetch.git
   cd droidFetch

2. Make the script executable:
   chmod +x dfetch-unstable-0.2.py

3. Run it:
   python3 dfetch-unstable-0.2.py

*(Optional)* You can rename the script to `dfetch` and move it to your bin folder (e.g., `PREFIX/bin/` in Termux) for global access.

## 📖 Usage

Run the script without arguments for the standard vertical layout:
python3 dfetch-unstable-0.2.py

### Command-Line Options

| Option | Description |
| :--- | :--- |
| `-h`, `--help` | Show the help message and exit. |
| `-v`, `--version` | Display version information and exit. |
| `-T`, `--tablet` | Enable horizontal layout mode (ideal for tablets/wide terminals). |
| `-D`, `--custom-distro <ID>` | **Debug Mode:** Force display a specific distro logo (e.g., `MIUI`, `HYPEROS`, `LINEAGE`). |
| `-C`, `--custom-color <COLOR>` | **Debug Mode:** Force override the theme color. Supports ANSI escape codes or special palettes (`GOOGLE_RAINBOW`, `PRIDE`, `TRANS_PRIDE`). |
| `--gen-config` | Generate a default configuration file in `~/.config/dfetch/dfetch.conf` and exit. |
| `--gen-config-samedir` | Generate a default configuration file in a `dfetch` folder within the current directory (useful for portable testing). |

## ⚙️ Configuration

You can customize `droidFetch` permanently by generating a config file:

python3 dfetch-unstable-0.2.py --gen-config

This creates `~/.config/dfetch/dfetch.conf`. Open it in any text editor to modify defaults:

# dfetch configuration file
distro=default        # Override detected ROM (e.g., set to CRDROID)
color=default         # Override color (e.g., set to \033[1;31m)
custom_ascii=default  # Path to a text file containing custom ASCII art
tablet_mode=default   # Set to 'true' to always use horizontal mode
