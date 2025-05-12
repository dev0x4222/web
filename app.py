#!/usr/bin/env python3
"""
Dev0x4 Tool - Web Edition (Phiên bản hoàn chỉnh)

Phiên bản nâng cấp với giao diện web hiện đại, không yêu cầu cơ sở dữ liệu.
Hỗ trợ tải xuống bản GUI cho người dùng.
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file, abort, flash, session
from attached_assets.github_manager import GitHubManager
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

# Khởi tạo GitHub Manager
github_manager = GitHubManager()

def get_user_info():
    """Lấy thông tin người dùng từ header"""
    try:
        return {
            'id': request.headers.get('X-Replit-User-Id'),
            'name': request.headers.get('X-Replit-User-Name'),
            'roles': request.headers.get('X-Replit-User-Roles')
        }
    except:
        return None

@app.context_processor
def inject_user():
    """Inject user info vào tất cả template"""
    return dict(user=get_user_info())

# Thư mục lưu trữ tệp đã tải lên
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Giới hạn kích thước tệp (16MB)

# Các định dạng tệp cho phép
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
ALLOWED_ZIP_EXTENSIONS = {'zip', 'zst', 'zstd'}

# Lưu log vào bộ nhớ thay vì cơ sở dữ liệu
logs = []

# Các thông tin về phiên bản
APP_VERSION = "1.0.0"
GUI_VERSION = "1.0.0"
GUI_FILE_SIZE = 0.73  # MB - Cập nhật kích thước thực của file zip nếu có thể

# Kiểm tra phần mở rộng tệp
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Trang chủ
@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.datetime.now().strftime("%H:%M:%S"))

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
    return render_template('download.html', file_size=GUI_FILE_SIZE)

# Tải xuống bản GUI
@app.route('/download/gui')
def download_gui():
    try:
        # Đường dẫn đến file zip trong dự án
        zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dev0x4-modernUI.zip")
        if os.path.exists(zip_path):
            return send_file(zip_path, as_attachment=True)
        else:
            # Đường dẫn thay thế (lên một cấp thư mục)
            alt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dev0x4-modernUI.zip")
            if os.path.exists(alt_path):
                return send_file(alt_path, as_attachment=True)
            else:
                # Chuyển hướng đến đường dẫn Replit
                flash('Đang chuyển hướng đến Replit để tải xuống file...', 'info')
                return redirect("https://replit.com/@clonegithub1712/Dev0x4-Tool#dev0x4-modernUI.zip")
    except Exception as e:
        flash(f'Không thể tải xuống: {str(e)}', 'error')
        return redirect(url_for('download'))

# Xử lý ảnh - Tách ảnh
@app.route('/image/split')
def image_split():
    return render_template('image_split.html', current_time=datetime.datetime.now().strftime("%H:%M:%S"))

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

    try:
        # Tạo thư mục output nếu chưa tồn tại
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Lưu file tạm thời
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Xử lý ảnh theo phương thức được chọn
        from PIL import Image
        img = Image.open(filepath)

        split_method = request.form.get('split_method', 'size')
        if split_method == 'size':
            # Tách theo kích thước
            width = int(request.form.get('width', 100))
            height = int(request.form.get('height', 100))
            maintain_ratio = 'maintain_ratio' in request.form

            if maintain_ratio:
                ratio = img.size[0] / img.size[1]
                height = int(width / ratio)

            # Tách ảnh thành các phần nhỏ
            num_cols = img.size[0] // width
            num_rows = img.size[1] // height

            for i in range(num_rows):
                for j in range(num_cols):
                    box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
                    output_filename = f'split_{i}_{j}.png'
                    output_path = os.path.join(output_dir, output_filename)
                    img.crop(box).save(output_path)

        elif split_method == 'grid':
            # Tách theo lưới
            rows = int(request.form.get('rows', 2))
            cols = int(request.form.get('columns', 2))

            width = img.size[0] // cols
            height = img.size[1] // rows

            for i in range(rows):
                for j in range(cols):
                    box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
                    output_filename = f'grid_{i}_{j}.png'
                    output_path = os.path.join(output_dir, output_filename)
                    img.crop(box).save(output_path)

        elif split_method == 'color':
            # Tách theo màu sắc
            from PIL import ImageOps
            threshold = int(request.form.get('color_threshold', 50))
            ignore_bg = 'ignore_background' in request.form

            # Chuyển ảnh sang grayscale và áp dụng ngưỡng
            gray_img = ImageOps.grayscale(img)
            binary_img = gray_img.point(lambda x: 0 if x < threshold else 255, '1')

            if ignore_bg:
                # Lưu phần foreground
                output_path = os.path.join(output_dir, 'foreground.png')
                binary_img.save(output_path)
            else:
                # Lưu cả foreground và background
                output_path_fg = os.path.join(output_dir, 'foreground.png')
                output_path_bg = os.path.join(output_dir, 'background.png')
                binary_img.save(output_path_fg)
                ImageOps.invert(binary_img).save(output_path_bg)

        # Lấy danh sách các file đã xử lý
        processed_files = os.listdir(output_dir)
        processed_files = [f for f in processed_files if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        # Xóa file tạm
        os.remove(filepath)

        # Lưu danh sách file vào session
        session['processed_files'] = processed_files

        flash('Xử lý ảnh thành công!', 'success')
        return redirect(url_for('image_split_results'))

    except Exception as e:
        flash(f'Lỗi khi xử lý ảnh: {str(e)}', 'error')
        return redirect(url_for('image_split'))

# Xử lý ảnh - Chuyển ảnh thành văn bản
@app.route('/image/text')
def image_to_text():
    return render_template('feature.html', 
                          feature_name="Chuyển ảnh thành văn bản",
                          feature_description="Chuyển đổi ảnh thành ASCII Art hoặc văn bản.",
                          current_time=datetime.datetime.now().strftime("%H:%M:%S"))

# Xử lý ảnh - Xóa ảnh đã tạo
@app.route('/image/delete')
def delete_images():
    return render_template('feature.html', 
                          feature_name="Xóa ảnh đã tạo",
                          feature_description="Dọn dẹp các ảnh đã tạo để tiết kiệm không gian lưu trữ.",
                          current_time=datetime.datetime.now().strftime("%H:%M:%S"))

# Tệp ZSTD - Nén tệp
@app.route('/zstd/compress')
def compress_zstd():
    return render_template('feature.html', 
                          feature_name="Nén tệp ZSTD",
                          feature_description="Nén tệp hoặc thư mục sử dụng thuật toán ZSTD hiệu quả.",
                          current_time=datetime.datetime.now().strftime("%H:%M:%S"))

# Tệp ZSTD - Giải nén tệp
@app.route('/zstd/decompress')
def decompress_zstd():
    return render_template('feature.html', 
                          feature_name="Giải nén tệp ZSTD",
                          feature_description="Giải nén các tệp đã được nén bằng ZSTD.",
                          current_time=datetime.datetime.now().strftime("%H:%M:%S"))

# Tệp ZSTD - Tạo từ điển
@app.route('/zstd/dictionary')
def create_dict():
    return render_template('feature.html', 
                          feature_name="Tạo từ điển ZSTD",
                          feature_description="Tạo từ điển tùy chỉnh để cải thiện hiệu suất nén cho các tệp tương tự.",
                          current_time=datetime.datetime.now().strftime("%H:%M:%S"))

# Công cụ Mod - Mod Effect
@app.route('/mod/effect')
def mod_effect():
    return render_template('feature.html', 
                          feature_name="Mod Effect",
                          feature_description="Chỉnh sửa hiệu ứng của tướng và trang phục trong game Arena of Valor.",
                          current_time=datetime.datetime.now().strftime("%H:%M:%S"))

# Công cụ Mod - Xem thông tin Mod
@app.route('/mod/info')
def mod_info():
    return render_template('feature.html', 
                          feature_name="Xem thông tin Mod",
                          feature_description="Tra cứu thông tin về các ID tướng, trang phục và hiệu ứng.",
                          current_time=datetime.datetime.now().strftime("%H:%M:%S"))

# Công cụ Mod - Hướng dẫn sử dụng Mod
@app.route('/mod/guide')
def mod_guide():
    return render_template('feature.html', 
                          feature_name="Hướng dẫn sử dụng Mod",
                          feature_description="Xem hướng dẫn chi tiết về cách cài đặt và sử dụng mod trong game.",
                          current_time=datetime.datetime.now().strftime("%H:%M:%S"))

# Tiện ích - Chatbot trợ giúp
@app.route('/utilities/chatbot')
def chatbot():
    return render_template('feature.html', 
                          feature_name="Chatbot Trợ giúp",
                          feature_description="Tương tác với chatbot để nhận hỗ trợ về cách sử dụng công cụ.",
                          current_time=datetime.datetime.now().strftime("%H:%M:%S"))

# Tiện ích - Chat với ChatGPT
@app.route('/utilities/chatgpt')
def chat_gpt():
    return render_template('feature.html', 
                          feature_name="Chat với ChatGPT",
                          feature_description="Sử dụng AI tiên tiến để nhận hỗ trợ hoặc thông tin (yêu cầu API key).",
                          current_time=datetime.datetime.now().strftime("%H:%M:%S"))

# Tiện ích - Xem ZIP
@app.route('/utilities/zip')
def view_zip():
    return render_template('feature.html', 
                          feature_name="Xem ZIP",
                          feature_description="Xem nội dung tệp ZIP mà không cần giải nén.",
                          current_time=datetime.datetime.now().strftime("%H:%M:%S"))

# Tiện ích - Tối ưu Windows
@app.route('/utilities/winoptimizer')
def win_optimizer():
    return render_template('downloadw.html')

@app.route('/download/winoptimizer')
def download_winoptimizer():
    return send_file(
        'WinOptimizerPro.exe', 
        as_attachment=True,
        download_name='WinOptimizerPro.exe'
    )

# API lấy trạng thái
@app.route('/api/status')
def api_status():
    return jsonify({
        "status": "success",
        "version": APP_VERSION,
        "gui_version": GUI_VERSION,
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
    logs.append({
        'timestamp': timestamp,
        'message': message,
        'level': level
    })

    # Giới hạn số lượng log để tránh chiếm quá nhiều bộ nhớ
    if len(logs) > 1000:
        logs.pop(0)

    return jsonify({"status": "success", "message": "Log saved"})

# Xử lý lỗi 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Trang không tìm thấy"), 404

# Xử lý lỗi 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_code=500, error_message="Lỗi máy chủ nội bộ"), 500

if __name__ == '__main__':
    # Sử dụng port từ biến môi trường hoặc mặc định là 8080 (Replit sử dụng port này)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

@app.route('/image/split/results')
def image_split_results():
    processed_files = session.get('processed_files', [])
    return render_template('image_split_results.html', files=processed_files)

@app.route('/image/split/download/<filename>')
def download_processed_image(filename):
    try:
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'output')
        return send_file(os.path.join(output_dir, filename), as_attachment=True)
    except:
        flash('Không tìm thấy file.', 'error')
        return redirect(url_for('image_split_results'))