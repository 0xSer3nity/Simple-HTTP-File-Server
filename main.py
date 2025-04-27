#!/usr/bin/env python3

import argparse
import os
import socket
import threading
import mimetypes
import urllib.parse
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import random
import string

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler with logging and security features"""
    
    def __init__(self, *args, directory=None, enable_uploads=False, **kwargs):
        self.enable_uploads = enable_uploads
        super().__init__(*args, directory=directory, **kwargs)
    
    def log_message(self, format, *args):
        """Override logging to show client IP and timestamp"""
        client_ip = self.client_address[0]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {client_ip} - {format % args}")
    
    def list_directory(self, path):
        """Generate directory listing with improved styling"""
        try:
            listing = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        
        listing.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
        
        enc = sys.getfilesystemencoding()
        title = f"Directory listing for {self.path}"
        
        # Start HTML output
        r = []
        r.append('<!DOCTYPE HTML>')
        r.append('<html lang="en">')
        r.append('<head>')
        r.append(f'<title>{title}</title>')
        r.append('<meta charset="utf-8">')
        r.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        r.append('<style>')
        r.append('body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 20px; }')
        r.append('h1 { border-bottom: 1px solid #ddd; padding-bottom: 10px; }')
        r.append('table { border-collapse: collapse; width: 100%; }')
        r.append('th, td { text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }')
        r.append('tr:hover { background-color: #f5f5f5; }')
        r.append('a { text-decoration: none; color: #0366d6; }')
        r.append('a:hover { text-decoration: underline; }')
        r.append('.dir { font-weight: bold; }')
        r.append('.size { color: #6c757d; }')
        r.append('.upload { margin-top: 20px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; }')
        r.append('</style>')
        r.append('</head>')
        r.append('<body>')
        r.append(f'<h1>{title}</h1>')
        r.append('<table>')
        r.append('<tr><th>Name</th><th>Size</th><th>Last Modified</th></tr>')
        
        # Add parent directory entry
        r.append('<tr>')
        r.append('<td><a href="../">..</a></td>')
        r.append('<td class="size">-</td>')
        r.append('<td>-</td>')
        r.append('</tr>')
        
        # Add directory entries and files
        for name in listing:
            fullname = os.path.join(path, name)
            displayname = name
            
            # Skip hidden files
            if name.startswith('.'):
                continue
            
            # Encode the name for URL
            linkname = urllib.parse.quote(name)
            
            # Get file information
            try:
                size = os.path.getsize(fullname)
                size_str = self.format_size(size)
                mtime = datetime.fromtimestamp(os.path.getmtime(fullname))
                mtime_str = mtime.strftime("%Y-%m-%d %H:%M:%S")
            except:
                size_str = "Unknown"
                mtime_str = "Unknown"
            
            is_dir = os.path.isdir(fullname)
            
            r.append('<tr>')
            if is_dir:
                r.append(f'<td><a href="{linkname}/" class="dir">{displayname}/</a></td>')
                r.append('<td class="size">-</td>')
            else:
                r.append(f'<td><a href="{linkname}">{displayname}</a></td>')
                r.append(f'<td class="size">{size_str}</td>')
            
            r.append(f'<td>{mtime_str}</td>')
            r.append('</tr>')
        
        r.append('</table>')
        
        # Add upload form if enabled
        if self.enable_uploads:
            r.append('<div class="upload">')
            r.append('<h2>Upload File</h2>')
            r.append(f'<form action="{self.path}" method="POST" enctype="multipart/form-data">')
            r.append('<input type="file" name="file">')
            r.append('<input type="submit" value="Upload">')
            r.append('</form>')
            r.append('</div>')
        
        r.append('</body>')
        r.append('</html>')
        
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        
        return encoded
    
    def format_size(self, size):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    
    def do_POST(self):
        """Handle POST requests for file uploads"""
        if not self.enable_uploads:
            self.send_error(405, "Method Not Allowed")
            return
        
        # Parse the form data
        content_type = self.headers['Content-Type']
        
        if not content_type or not content_type.startswith('multipart/form-data'):
            self.send_error(400, "Bad Request - Not a multipart/form-data request")
            return
        
        # Find the boundary
        boundary = content_type.split('=')[1].strip()
        
        # Read the request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Split by boundary
        parts = post_data.split(bytes('--' + boundary, 'utf-8'))
        
        # Process each part
        for part in parts:
            if b'filename=' in part:
                # Extract filename
                filename_start = part.find(b'filename="') + 10
                filename_end = part.find(b'"', filename_start)
                filename = part[filename_start:filename_end].decode('utf-8')
                
                # Skip if no filename
                if not filename:
                    continue
                
                # Find the content
                content_start = part.find(b'\r\n\r\n') + 4
                content = part[content_start:-2]  # Skip the last \r\n
                
                # Save the file
                file_path = os.path.join(self.directory, filename)
                try:
                    with open(file_path, 'wb') as f:
                        f.write(content)
                    self.log_message(f"File uploaded: {filename} ({self.format_size(len(content))})")
                except Exception as e:
                    self.log_message(f"Error saving file: {e}")
                    self.send_error(500, f"Error saving file: {e}")
                    return
        
        # Redirect back to the directory listing
        self.send_response(303)
        self.send_header("Location", self.path)
        self.end_headers()

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def generate_certificate(cert_file, key_file):
    """Generate a self-signed certificate for HTTPS"""
    try:
        from OpenSSL import crypto
        
        # Create key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)
        
        # Create certificate
        cert = crypto.X509()
        cert.get_subject().C = "US"
        cert.get_subject().ST = "State"
        cert.get_subject().L = "City"
        cert.get_subject().O = "Organization"
        cert.get_subject().OU = "Organizational Unit"
        cert.get_subject().CN = socket.gethostname()
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)  # 10 years
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha256')
        
        # Save certificate and key
        with open(cert_file, "wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        
        with open(key_file, "wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
        
        return True
    except Exception as e:
        print(f"Error generating certificate: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Simple HTTP File Server")
    
    parser.add_argument("-d", "--directory", default=".", help="Directory to serve (default: current directory)")
    parser.add_argument("-p", "--port", type=int, default=8000, help="Port to listen on (default: 8000)")
    parser.add_argument("-b", "--bind", default="", help="Address to bind to (default: all interfaces)")
    parser.add_argument("-u", "--uploads", action="store_true", help="Enable file uploads")
    parser.add_argument("-s", "--ssl", action="store_true", help="Enable HTTPS")
    parser.add_argument("--cert", default="server.crt", help="SSL certificate file (default: server.crt)")
    parser.add_argument("--key", default="server.key", help="SSL key file (default: server.key)")
    
    args = parser.parse_args()
    
    # Ensure directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a directory")
        return
    
    # Set up SSL if enabled
    if args.ssl:
        if not os.path.exists(args.cert) or not os.path.exists(args.key):
            print("SSL certificate or key not found. Generating self-signed certificate...")
            if not generate_certificate(args.cert, args.key):
                print("Error generating certificate. HTTPS will not be available.")
                args.ssl = False
    
    # Set up handler
    handler = lambda *args, **kwargs: CustomHTTPRequestHandler(*args, directory=args.directory, enable_uploads=args.uploads, **kwargs)
    
    # Create server
    server = HTTPServer((args.bind, args.port), handler)
    
    # Set up SSL if enabled
    if args.ssl:
        server.socket = ssl.wrap_socket(server.socket, 
                                       server_side=True,
                                       certfile=args.cert,
                                       keyfile=args.key)
        protocol = "HTTPS"
    else:
        protocol = "HTTP"
    
    # Get local IP
    local_ip = get_local_ip()
    
    server_url = f"{protocol.lower()}://{local_ip}:{args.port}"
    
    print(f"\n{'=' * 50}")
    print(f"Simple HTTP File Server Running")
    print(f"{'=' * 50}")
    print(f"Protocol: {protocol}")
    print(f"Directory: {os.path.abspath(args.directory)}")
    print(f"Local URL: {protocol.lower()}://localhost:{args.port}")
    print(f"Network URL: {server_url}")
    
    if args.uploads:
        print("File uploads: Enabled")
    else:
        print("File uploads: Disabled")
    
    print(f"{'=' * 50}")
    print("Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    import sys
    main()
