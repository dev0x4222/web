#!/usr/bin/env python3
"""
Dev0x4 Tool - Web Edition (Phiên bản hoàn chỉnh)

Điểm vào của ứng dụng web cho phép chạy trên Replit và các nền tảng khác
"""

from app import app

if __name__ == "__main__":
    import os
    # Sử dụng PORT từ biến môi trường hoặc mặc định là 8080 (chuẩn của Replit)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)