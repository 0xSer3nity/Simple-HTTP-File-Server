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

## 📝 Examples

### Start a basic server in the current directory:
```bash
python main.py
```

### Serve a specific directory:
```bash
python main.py -d /path/to/files
```

### Use a different port:
```bash
python main.py -p 9000
```

### Enable file uploads:
```bash
python main.py -u
```

### Enable HTTPS:
```bash
python main.py -s
```

### Full example with all options:
```bash
python main.py -d /path/to/files -p 8080 -u -s
```

## 🔄 How It Works

The server uses Python's built-in HTTP server capabilities to create a web server that:

1. Serves files from your specified directory
2. Provides a clean, mobile-friendly interface to browse directories
3. Displays file sizes in human-readable format
4. Shows last modification times for files
5. Optionally allows file uploads through a simple web form
6. Provides secure connections with HTTPS if enabled

When you start the server, it will display the URLs you can use to access it, both from the local machine and from other devices on your network.

## 🔒 Security Notes

- This server is intended for temporary file sharing on trusted networks
- The file upload feature should be used with caution, as it allows anyone with access to upload files
- When using HTTPS, a self-signed certificate is generated, which may cause browser warnings
- There is no authentication, so anyone with network access can view and download files
- Do not use this server for sensitive information without proper security measures

## 💡 Tips

- Use the `-u` flag to enable file uploads when you need to collect files from others
- HTTPS is recommended if you're sharing on public Wi-Fi
- The server shows your local network IP, so others on the same network can access it
- You can redirect the output to a file to keep a log of all accesses
- To make the server accessible from the internet, you would need to configure port forwarding on your router (not recommended without proper security)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.