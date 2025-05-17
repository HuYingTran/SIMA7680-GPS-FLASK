from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from function import *
from setup import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Bạn nên sử dụng một key bí mật mạnh mẽ trong thực tế

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Lớp User cho Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Giả sử bạn có một danh sách người dùng
users = {'admin': {'password': '0123'}}

@login_manager.user_loader
def load_user(user_id):
    # Chỉ trả về User nếu id hợp lệ
    return User(user_id) if user_id in users else None

# Thông tin tài khoản mẫu
USERNAME = 'admin'
PASSWORD = '0123'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Kiểm tra xem người dùng đã bị khóa chưa
    if 'locked_until' in session:
        locked_until = session['locked_until'].replace(tzinfo=None)
        print(locked_until)
        if datetime.now() < locked_until:
            print(f"Bạn đã bị khóa. Vui lòng thử lại sau {locked_until - datetime.now()}.", 'danger')
            return jsonify({'success': False, 'message': f"Bạn đã bị khóa. Vui lòng thử lại sau {locked_until - datetime.now()}."}), 401
            # return render_template('login.html')

        # Nếu hết thời gian khóa, xóa session 'locked_until'
        else:
            session.pop('locked_until', None)
    
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        # Kiểm tra đăng nhập
        if username == USERNAME and password == PASSWORD:
            user = User(username)
            login_user(user)  # Đăng nhập người dùng
            session.pop('login_attempts', None)  # Reset số lần đăng nhập sai
            return jsonify({'success': True, 'message': 'Đăng nhập thành công!', 'redirect': url_for('home')}), 200

        # Nếu đăng nhập sai, tăng số lần đăng nhập sai
        if 'login_attempts' not in session:
            session['login_attempts'] = 0

        session['login_attempts'] += 1

        # Nếu số lần đăng nhập sai vượt quá 5 lần, khóa tài khoản
        if session['login_attempts'] >= 5:
            session['locked_until'] = datetime.now() + timedelta(minutes=10)
            flash("Bạn đã nhập sai quá 5 lần, tài khoản của bạn đã bị khóa trong 10 phút.", 'danger')
            return jsonify({'success': False, 'message': "Bạn đã nhập sai quá 5 lần, tài khoản của bạn đã bị khóa trong 10 phút."}), 401

        if session['login_attempts'] >= 1:
            return jsonify({'success': False, 'message': f"Bạn đã nhập sai quá {session['login_attempts']} lần."}), 401

        flash("Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng thử lại!", 'danger')

    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    data_db = get_all_data()
    return render_template('home.html', data=data_db)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')


@app.route('/home/filter', methods=['GET'])
def home_filter():
    # Lấy tham số ngày bắt đầu và ngày kết thúc từ URL query string
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date and end_date:
        # Nếu ngày được cung cấp, chuyển đổi thành định dạng ngày
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
        # Lấy dữ liệu từ cơ sở dữ liệu (có thể lọc theo ngày)
        data = get_data_by_time(start_date, end_date)
        # Chuyển dữ liệu thành JSON và trả về
        return jsonify(data)
    else:
        # Lấy dữ liệu từ cơ sở dữ liệu
        data = get_all_data()

        # Chuyển đổi dữ liệu thành dạng JSON và trả về
        return jsonify(data)

@app.route('/home/delete_all', methods=['POST'])
def delete_all():
    # Lấy danh sách các ID từ request
    ids = request.json.get('ids', [])

    if not ids:
        return jsonify({"message": "No IDs provided"}), 400
    delete_data_id(ids)

    return jsonify({"success": True, "message": "Successfullly!"}), 200

@app.route('/api/post', methods=['GET', 'POST'])
def post():
    data_t = request.args.get("gps")
    timestamp_t = request.args.get("timestamp")
    phone_t = request.args.get("phone")
    x_y = extract_coordinates(data_t)
    write_data(data_t, str(x_y[0]), str(x_y[1]), timestamp_t, phone_t.replace(" ","+"))
    return jsonify({"success": True, "message": "Successfullly!"}), 200

if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', debug=True)
