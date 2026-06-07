from flask import Flask, request, render_template_string, send_from_directory
import os
import html

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FORM = '''
<!doctype html>
<title>文件上传靶场</title>
<h1>上传任意文件（无限制）</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=上传>
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return (
                f'上传成功！文件已保存到：{filepath}<br><br>'
                f'<a href="/uploads/{filename}">访问文件</a><br>'
                f'<a href="/raw/{filename}">查看源码（验证 PHP 内容）</a>'
            )
    return render_template_string(UPLOAD_FORM)


@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/raw/<path:filename>')
def show_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        escaped = html.escape(content)
        return f'<pre style="background:#f0f0f0;padding:16px;border:2px solid red;font-size:16px;">{escaped}</pre>'
    else:
        return (
            f'<p>File not found: {filepath}</p>'
            f'<p>当前上传目录中的文件：{os.listdir(app.config["UPLOAD_FOLDER"])}</p>'
        ), 404


if __name__ == '__main__':
    print(f'上传目录: {UPLOAD_FOLDER}')
    print(f'访问地址: http://127.0.0.1:5000')
    app.run(host='127.0.0.1', port=5000, debug=True)
