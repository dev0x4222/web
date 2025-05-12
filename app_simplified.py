#!/usr/bin/env python3
"""
Dev0x4 Tool - Web Edition (Simplified Version)

Phiên bản nâng cấp với giao diện web hiện đại, không yêu cầu cơ sở dữ liệu.
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file, abort, flash, session
import os
import datetime
import time
import mimetypes
import shutil
import json
from werkzeug.utils import secure_filename

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
app.secret_key = "dev0x4-aov-tool-secret-key"

# Thư mục lưu trữ tệp đã tải lên
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config[
    'MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Giới hạn kích thước tệp (16MB)

# Các định dạng tệp cho phép
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
ALLOWED_ZIP_EXTENSIONS = {'zip', 'zst', 'zstd'}

# Lưu log vào bộ nhớ thay vì cơ sở dữ liệu
logs = []


# Kiểm tra phần mở rộng tệp
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in allowed_extensions


# Trang chủ
@app.route('/')
def index():
    return render_template(
        'index.html',
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


# Trang hướng dẫn
@app.route('/guide')
def guide():
    return render_template('guide.html')


# Trang thông tin
@app.route('/about')
def about():
    current_date = datetime.datetime.now().strftime("%d/%m/%Y")
    return render_template('about.html', current_date=current_date)


# Trang tải về
@app.route('/download')
def download():
    file_size = 0.73  # Kích thước có thể được cập nhật nếu có file thực
    return render_template('download.html', file_size=file_size)


# Tải xuống tệp
@app.route('/download/file')
def download_file():
    try:
        # Đường dẫn đến file zip - cần cập nhật theo đường dẫn thực của bạn
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "dev0x4-modernUI.zip")
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('Không tìm thấy tệp tải về.', 'error')
            return redirect(url_for('download'))
    except:
        flash('Không tìm thấy tệp tải về.', 'error')
        return redirect(url_for('download'))


# Xử lý ảnh - Tách ảnh
@app.route('/image/split')
def image_split():
    return render_template(
        'image_split.html',
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


@app.route('/image/split/process', methods=['POST'])
def image_split_process():
    if 'image' not in request.files:
        flash('Không tìm thấy tệp ảnh', 'error')
        return redirect(url_for('image_split'))

    file = request.files['image']
    if file.filename == '':
        flash('Chưa chọn tệp', 'error')
        return redirect(url_for('image_split'))

    if not allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        flash('Định dạng tệp không được hỗ trợ', 'error')
        return redirect(url_for('image_split'))

    # Thông báo tính năng đang được phát triển
    flash('Tính năng tách ảnh đang được phát triển', 'info')
    return redirect(url_for('image_split'))


# Xử lý ảnh - Chuyển ảnh thành văn bản
@app.route('/image/text')
def image_to_text():
    return render_template(
        'feature.html',
        feature_name="Chuyển ảnh thành văn bản",
        feature_description="Chuyển đổi ảnh thành ASCII Art hoặc văn bản.",
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


# Xử lý ảnh - Xóa ảnh đã tạo
@app.route('/image/delete')
def delete_images():
    return render_template(
        'feature.html',
        feature_name="Xóa ảnh đã tạo",
        feature_description=
        "Dọn dẹp các ảnh đã tạo để tiết kiệm không gian lưu trữ.",
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


# Tệp ZSTD - Nén tệp
@app.route('/zstd/compress')
def compress_zstd():
    return render_template(
        'feature.html',
        feature_name="Nén tệp ZSTD",
        feature_description=
        "Nén tệp hoặc thư mục sử dụng thuật toán ZSTD hiệu quả.",
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


# Tệp ZSTD - Giải nén tệp
@app.route('/zstd/decompress')
def decompress_zstd():
    return render_template(
        'feature.html',
        feature_name="Giải nén tệp ZSTD",
        feature_description="Giải nén các tệp đã được nén bằng ZSTD.",
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


# Tệp ZSTD - Tạo từ điển
@app.route('/zstd/dictionary')
def create_dict():
    return render_template(
        'feature.html',
        feature_name="Tạo từ điển ZSTD",
        feature_description=
        "Tạo từ điển tùy chỉnh để cải thiện hiệu suất nén cho các tệp tương tự.",
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


# Công cụ Mod - Mod Effect
@app.route('/mod/effect')
def mod_effect():
    return render_template(
        'feature.html',
        feature_name="Mod Effect",
        feature_description=
        "Chỉnh sửa hiệu ứng của tướng và trang phục trong game Arena of Valor.",
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


# Công cụ Mod - Xem thông tin Mod
@app.route('/mod/info')
def mod_info():
    return render_template(
        'feature.html',
        feature_name="Xem thông tin Mod",
        feature_description=
        "Tra cứu thông tin về các ID tướng, trang phục và hiệu ứng.",
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


# Công cụ Mod - Hướng dẫn sử dụng Mod
@app.route('/mod/guide')
def mod_guide():
    return render_template(
        'feature.html',
        feature_name="Hướng dẫn sử dụng Mod",
        feature_description=
        "Xem hướng dẫn chi tiết về cách cài đặt và sử dụng mod trong game.",
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


# Tiện ích - Chatbot trợ giúp
@app.route('/utilities/chatbot')
def chatbot():
    return render_template(
        'feature.html',
        feature_name="Chatbot Trợ giúp",
        feature_description=
        "Tương tác với chatbot để nhận hỗ trợ về cách sử dụng công cụ.",
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


# Tiện ích - Chat với ChatGPT
@app.route('/utilities/chatgpt')
def chat_gpt():
    return render_template(
        'feature.html',
        feature_name="Chat với ChatGPT",
        feature_description=
        "Sử dụng AI tiên tiến để nhận hỗ trợ hoặc thông tin (yêu cầu API key).",
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


# Tiện ích - Xem ZIP
@app.route('/utilities/zip')
def view_zip():
    return render_template(
        'feature.html',
        feature_name="Xem ZIP",
        feature_description="Xem nội dung của tệp ZIP mà không cần giải nén.",
        current_time=datetime.datetime.now().strftime("%H:%M:%S"))


# API lấy trạng thái
@app.route('/api/status')
def api_status():
    return jsonify({
        "status": "success",
        "version": "1.0.0",
        "server_time": datetime.datetime.now().isoformat()
    })


# API log
@app.route('/api/log', methods=['POST'])
def api_log():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"status": "error", "message": "Missing message"}), 400

    message = data['message']
    level = data.get('level', 'info')

    # Lưu log vào bộ nhớ
    timestamp = datetime.datetime.now().isoformat()
    logs.append({'timestamp': timestamp, 'message': message, 'level': level})

    # Giới hạn số lượng log để tránh chiếm quá nhiều bộ nhớ
    if len(logs) > 1000:
        logs.pop(0)

    return jsonify({"status": "success", "message": "Log saved"})


# Xử lý lỗi 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',
                           error_code=404,
                           error_message="Trang không tìm thấy"), 404


# Xử lý lỗi 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html',
                           error_code=500,
                           error_message="Lỗi máy chủ nội bộ"), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
