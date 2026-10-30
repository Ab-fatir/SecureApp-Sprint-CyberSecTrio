import os
import ctypes
import struct

class MetadataParserWrapper:
    MAGIC = b"CVLT"
    HEADER_STRUCT = "<4sHHI"
    HEADER_SIZE = struct.calcsize(HEADER_STRUCT)
    MAX_SAFE_PAYLOAD = 4096

    def __init__(self, mode="secure"):
        self.mode = mode
        self.lib = None
        self._load_native_library()

    def _load_native_library(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        so_path = os.path.join(base_dir, "libparser_secure.so")
        dll_path = os.path.join(base_dir, "libparser_secure.dll")

        if os.path.exists(so_path):
            try:
                self.lib = ctypes.CDLL(so_path)
            except Exception:
                self.lib = None
        elif os.path.exists(dll_path):
            try:
                self.lib = ctypes.CDLL(dll_path)
            except Exception:
                self.lib = None

    def parse_header(self, raw_bytes):
        if self.mode == "vulnerable":
            if len(raw_bytes) < self.HEADER_SIZE:
                return {"success": False, "error": "Buffer too small", "error_code": -1}
            payload = raw_bytes[self.HEADER_SIZE:]
            parts = payload.split(b"\x00")
            author = parts[0].decode("latin-1", errors="ignore")
            title = parts[1].decode("latin-1", errors="ignore") if len(parts) > 1 else "Default Title"
            return {
                "success": True,
                "author": author,
                "title": title,
                "error_code": 0
            }

        if len(raw_bytes) < self.HEADER_SIZE:
            return {"success": False, "error": "Buffer too small", "error_code": -1}

        if len(raw_bytes) > self.MAX_SAFE_PAYLOAD:
            return {"success": False, "error": "Payload exceeds 4096 limit", "error_code": -4}

        magic, version, flags, declared_len = struct.unpack(self.HEADER_STRUCT, raw_bytes[:self.HEADER_SIZE])

        if magic != self.MAGIC:
            return {"success": False, "error": "Invalid magic header", "error_code": -2}

        actual_payload_len = len(raw_bytes) - self.HEADER_SIZE
        if declared_len > actual_payload_len:
            return {"success": False, "error": "Declared length mismatch", "error_code": -3}

        payload = raw_bytes[self.HEADER_SIZE:self.HEADER_SIZE + actual_payload_len]
        parts = payload.split(b"\x00")
        author = parts[0][:63].decode("utf-8", errors="replace")
        title = parts[1][:127].decode("utf-8", errors="replace") if len(parts) > 1 else "Untitled Document"

        return {
            "success": True,
            "author": author,
            "title": title,
            "version": version,
            "flags": flags,
            "error_code": 0
        }
