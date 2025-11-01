# MapMaker

## Overview
MapMaker is a tile-based map authoring tool built with Python and Pygame. It couples a simple world model with an interactive editor so you can prototype tactical battlefields or adventure maps without writing code. The default entry point prepares an 80×60 world, wires up the editing interface, and launches the event loop, allowing you to start painting immediately once the assets are in place.

## Features
- **Layered world representation.** Worlds are backed by dedicated layers for ground, impassable terrain, objects, and units, letting you keep structural data separate while editing.
- **Event-driven Pygame interface.** The UI bootstraps a resizable hardware-accelerated window, dispatches keyboard and mouse events to active components, and maintains consistent rendering state via a shared theme.
- **Editing game mode.** The `EditGameMode` wires together the world view, resource display, minimap, and palette components. It supports configurable brushes, drag-to-paint gestures, and keyboard shortcuts for quality-of-life features like auto-tiling toggles.
- **Theme-driven assets.** Tilesets, fonts, and colors are resolved through the `Theme` class, which expects sprite sheets and typography under an `assets/` directory so that art can be swapped without touching logic.

## Project structure
```text
core/          Core game state, domain logic, and constants.
ui/            Pygame-based interface, components, and editing modes.
Tools/         Utility modules shared across the project (e.g., vector math).
main.py        Launch script that builds a world and starts the editor.
test/          Legacy tests (pytest) slated for porting to the current package layout.
```

## Requirements
- Python 3.10 or newer (tested with CPython 3.11)
- [Pygame](https://www.pygame.org/) for rendering and input handling
- [NumPy](https://numpy.org/) for deterministic random generation in the theme system
- [pytest](https://docs.pytest.org/) for running the existing automated tests (optional)

Install dependencies with pip:
```bash
pip install pygame numpy pytest
```

## Assets
The UI and theme expect sprite sheets, fonts, and icons under an `assets/` directory. At minimum you should provide:
- `assets/toen/icon.png` for the application window icon.
- The tilesets and font files referenced in `ui/Theme/Theme.py` (e.g., `assets/toen/ground.png`, `assets/font/prstart/prstartk.ttf`).

## Getting started
1. Clone the repository and create a virtual environment (recommended).
2. Install dependencies as shown above.
3. Ensure the expected assets exist in the `assets/` directory.
4. Launch the editor:
   ```bash
   python main.py
   ```

Once running, use the palette to choose brush layers/values, paint on the world view with the mouse, and toggle auto-tiling with <kbd>F1</kbd>/<kbd>F2</kbd> when the world component is focused.

## Testing
Invoke pytest from the repository root:
```bash
pytest
```
Pytest currently discovers the legacy suite in `test/`; feel free to migrate or extend it to cover newer modules.

## Contributing
Contributions are welcome! Please open an issue or pull request describing the feature or fix you have in mind. When adding new UI or logic components, keep the separation between core state management and presentation so editors remain flexible.
