# 📋 Clipboard History Manager

A simple yet powerful clipboard history manager built with Python and tkinter. Automatically monitors your clipboard, stores the last N entries, and provides quick access to copy them back.

## ✨ Features

### Core Features (MVP)
- **Automatic Clipboard Monitoring**: Continuously polls clipboard for changes
- **History Storage**: Stores last 50 clipboard entries by default (configurable)
- **Quick Copy Back**: Double-click or press Enter to copy items back to clipboard
- **Persistent Storage**: Saves history to JSON file, survives app restarts

### Enhanced Features
- **Smart Content Detection**: Automatically categorizes content (URL, Text, Multi-line, Number)
- **Search & Filter**: Real-time search through clipboard history
- **Context Menu**: Right-click for additional options
- **Settings Panel**: Configure max history items and poll interval
- **Pause/Resume**: Toggle clipboard monitoring on/off
- **Clean Interface**: Modern tkinter UI with proper scrollbars and status updates

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- Windows, macOS, or Linux

### Quick Start
1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install pyperclip
   ```

3. **Run the application**:
   ```bash
   python clipboard_manager.py
   ```

## 🎯 Usage

### Basic Operations
1. **Start the app** - Clipboard monitoring begins automatically
2. **Copy something** - Any text you copy will appear in the history
3. **Access history** - Double-click any item to copy it back to clipboard
4. **Search** - Use the search bar to find specific clipboard entries
5. **Manage items** - Right-click for context menu options

### Keyboard Shortcuts
- **Enter** or **Double-click**: Copy selected item to clipboard
- **Delete**: Remove selected item from history
- **Right-click**: Show context menu

### Controls
- **⏸️ Pause/▶️ Resume**: Toggle clipboard monitoring
- **🗑️ Clear All**: Remove all history entries
- **⚙️ Settings**: Configure app preferences

## ⚙️ Configuration

### Settings Panel
- **Max History Items**: Set maximum number of clipboard entries to store (default: 50)
- **Poll Interval**: Set how often to check clipboard (default: 1 second)

### File Storage
- History is automatically saved to `clipboard_history.json` in the app directory
- File is updated after each clipboard change
- Data persists between app sessions

## 🔧 Technical Details

### Architecture
- **Main Thread**: Handles GUI and user interactions
- **Monitor Thread**: Background thread for clipboard polling
- **Event-Driven**: Uses tkinter's event system for responsive UI

### Dependencies
- **pyperclip**: Cross-platform clipboard access
- **tkinter**: GUI framework (included with Python)
- **threading**: Background clipboard monitoring
- **json**: Persistent data storage

### Performance
- **Low Resource Usage**: Minimal CPU and memory footprint
- **Efficient Polling**: Configurable interval to balance responsiveness vs. performance
- **Smart Deduplication**: Avoids storing duplicate clipboard content

## 🐛 Troubleshooting

### Common Issues

**"pyperclip module not found"**
```bash
pip install pyperclip
```

**Clipboard not updating**
- Check if monitoring is paused
- Verify app has clipboard permissions
- Try restarting the application

**Performance issues**
- Increase poll interval in settings
- Reduce max history items
- Close other clipboard-intensive applications

### Platform-Specific Notes

**Windows**: Works out of the box with pyperclip
**macOS**: May require clipboard permissions in System Preferences
**Linux**: May need additional clipboard manager (xclip/xsel)

## 🚧 Future Enhancements

### Planned Features
- **Global Hotkeys**: System-wide shortcuts for quick access
- **Clipboard Categories**: Manual organization of clipboard items
- **Export/Import**: Backup and restore clipboard history
- **Rich Content Support**: Images, files, and formatted text
- **Cloud Sync**: Sync clipboard history across devices

### Contributing
Feel free to submit issues, feature requests, or pull requests!

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Open an issue on the project repository

---

**Happy Clipping! 📋✨**
