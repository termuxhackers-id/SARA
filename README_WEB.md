# SARA Web Interface

A modern Flask web application for SARA (Simple Android Ransomware Attack) with a beautiful, dark-themed UI.

## Features

- 🌐 **Web-based Interface**: Modern, responsive web UI with Bootstrap 5
- 🎨 **Dark Theme**: Professional dark theme with glassmorphism effects
- 🔧 **Trojan Builder**: Create custom trojan APKs with Metasploit payload
- 🔒 **File Locker**: Generate file encryption ransomware
- 📱 **Screen Locker**: Build screen lock ransomware with custom messages
- 🎯 **Listener**: Start Metasploit listeners directly from the web interface
- 📁 **File Upload**: Custom icon upload for APK files
- ⚡ **Real-time Progress**: Live progress tracking for APK generation
- 📱 **Mobile Responsive**: Works on desktop, tablet, and mobile devices

## Installation

1. **Clone the repository** (if not already done):
```bash
git clone https://github.com/termuxhackers-id/SARA
cd SARA
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Ensure SARA dependencies are installed**:
```bash
sudo bash install.sh
```

## Usage

### Starting the Web Interface

```bash
python3 app.py
```

The web interface will be available at: `http://localhost:5000`

### Web Interface Features

#### 1. Trojan Builder
- Configure host IP and port
- Upload custom app icons
- Generate reverse TCP trojan APKs
- Compatible with Metasploit listeners

#### 2. File Locker
- Create file encryption ransomware
- Custom app names and messages
- Generates both encrypter and decrypter APKs
- Strong encryption algorithms

#### 3. Screen Locker
- Build screen lock ransomware
- Custom lock screen messages
- Configurable unlock passphrases
- Persistent screen overlay

#### 4. Listener
- Start Metasploit listeners
- Configure LHOST and LPORT
- Real-time listener status
- Automatic payload configuration

### API Endpoints

The web interface provides RESTful API endpoints:

- `GET /` - Main dashboard
- `GET /trojan` - Trojan builder page
- `POST /build_trojan` - Build trojan APK
- `GET /file_locker` - File locker builder page
- `POST /build_file_locker` - Build file locker APK
- `GET /screen_locker` - Screen locker builder page
- `POST /build_screen_locker` - Build screen locker APK
- `GET /listener` - Listener control page
- `POST /start_listener` - Start Metasploit listener
- `POST /upload_icon` - Upload custom icon
- `GET /download/<filename>` - Download generated APK

## Configuration

### Environment Variables

- `FLASK_ENV`: Set to `development` for debug mode
- `FLASK_PORT`: Custom port (default: 5000)
- `FLASK_HOST`: Custom host (default: 0.0.0.0)

### Security Notes

- Change the `secret_key` in `app.py` for production use
- Use HTTPS in production environments
- Implement proper authentication for production deployment
- Configure firewall rules appropriately

## File Structure

```
SARA/
├── app.py                 # Main Flask application
├── sara.py               # Original SARA core functions
├── requirements.txt      # Python dependencies
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Main dashboard
│   ├── trojan.html     # Trojan builder
│   ├── file_locker.html # File locker builder
│   ├── screen_locker.html # Screen locker builder
│   ├── listener.html   # Listener control
│   ├── 404.html       # Error page
│   └── 500.html       # Error page
├── static/             # Static assets
│   ├── css/
│   │   └── style.css  # Custom styles
│   └── js/
│       └── app.js     # JavaScript functionality
├── uploads/           # Uploaded icons
└── data/             # SARA data files
```

## Development

### Adding New Features

1. Create new routes in `app.py`
2. Add corresponding HTML templates
3. Update navigation in `base.html`
4. Add any new dependencies to `requirements.txt`

### Customizing the UI

- Modify `static/css/style.css` for styling changes
- Update `static/js/app.js` for JavaScript functionality
- Edit templates in `templates/` directory

## Security Disclaimer

⚠️ **IMPORTANT**: This tool is for educational purposes only. The author is not responsible for any misuse or damage caused by this software. Only use on devices you own or have explicit permission to test.

## Legal Notice

- Use only for authorized penetration testing
- Respect local laws and regulations
- Obtain proper permission before testing
- Use responsibly and ethically

## Dependencies

### Python Packages
- Flask 2.3.3
- Werkzeug 2.3.7
- Pillow 10.0.1
- Requests 2.31.0

### System Requirements
- Python 3.7+
- Java (for APK signing)
- APKTool
- Metasploit Framework (for listeners)

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **APK Generation Fails**: Check Java and APKTool installation
3. **Listener Issues**: Verify Metasploit Framework installation
4. **File Upload Issues**: Check file permissions and size limits

### Debug Mode

Enable debug mode for development:
```bash
export FLASK_ENV=development
python3 app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project follows the same license as the original SARA project.

## Credits

- Original SARA by [Termux Hackers ID](https://github.com/termuxhackers-id)
- Web interface built with Flask and Bootstrap
- Icons from Bootstrap Icons