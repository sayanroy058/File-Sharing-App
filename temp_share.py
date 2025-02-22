import os
import time
import threading
import qrcode
from datetime import datetime, timedelta
from uuid import uuid4

class TempFileShare:
    def __init__(self, base_url, upload_folder, expiry_minutes=10):
        self.base_url = base_url
        self.upload_folder = upload_folder
        self.expiry_minutes = expiry_minutes
        self.temp_files = {}
        self._start_cleanup_thread()
    
    def _start_cleanup_thread(self):
        def cleanup_loop():
            while True:
                self._cleanup_expired_files()
                time.sleep(60)  # Check every minute
        
        thread = threading.Thread(target=cleanup_loop, daemon=True)
        thread.start()
    
    def _cleanup_expired_files(self):
        current_time = datetime.now()
        expired_files = []
        
        for share_id, info in self.temp_files.items():
            # Skip files that never expire (expiry_time is None)
            if info['expiry_time'] is not None and current_time >= info['expiry_time']:
                # Remove the file and QR code
                try:
                    os.remove(info['file_path'])
                    os.remove(info['qr_path'])
                    expired_files.append(share_id)
                except OSError:
                    pass
        
        # Remove expired entries from temp_files
        for share_id in expired_files:
            self.temp_files.pop(share_id)
    
    def generate_share(self, original_filename, unique_filename, expiry_time=None):
        # Generate unique share ID
        share_id = str(uuid4())
        
        # Use provided expiry time or default
        if expiry_time is None:
            expiry_time = datetime.now() + timedelta(minutes=self.expiry_minutes)
        
        # Generate share URL
        share_url = f"{self.base_url}/share/{share_id}"
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(share_url)
        qr.make(fit=True)
        
        # Save QR code
        qr_filename = f"{share_id}.png"
        qr_path = os.path.join(self.upload_folder, qr_filename)
        qr.make_image(fill_color="black", back_color="white").save(qr_path)
        
        # Store file information
        self.temp_files[share_id] = {
            'original_filename': original_filename,
            'file_path': os.path.join(self.upload_folder, unique_filename),
            'qr_path': qr_path,
            'expiry_time': expiry_time,
            'share_url': share_url
        }
        
        return {
            'share_id': share_id,
            'share_url': share_url,
            'qr_path': qr_path,
            'expiry_time': expiry_time
        }
    
    def get_file_info(self, share_id):
        return self.temp_files.get(share_id)