# 🌐 Simple HTTP File Server

A lightweight HTTP server for sharing files on your local network with a clean web interface.

## ✨ Features

- 📂 Serve files from any directory
- 🔄 Clean and responsive directory listing
- 📤 Optional file upload capability
- 🔒 Support for HTTPS with self-signed certificates
- 📱 Works with any device on your network
- 📊 Real-time access logging
- 🔧 Customizable port and binding address

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xSer3nity/simple-http-server.git
cd simple-http-server
```

2. Optional: Install PyOpenSSL for HTTPS support:
```bash
pip install pyopenssl
```

3. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py [options]
```

## ⚙️ Options

- `-d, --directory`: Directory to serve (default: current directory)
- `-p, --port`: Port to listen on (default: 8000)
- `-b, --bind`: Address to bind to (default: all interfaces)
- `-u, --uploads`: Enable file uploads
- `-s, --ssl`: Enable HTTPS
- `--cert`: SSL certificate file (default: server.crt)
- `--key`: SSL key file (default: server.key)

