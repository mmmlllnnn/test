from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



# 创建Flask应用 / 解决跨域问题
app = Flask(__name__)
CORS(app)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义数据库模型
class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)


# 1. 获取用户列表接口
@app.route('/get_user_list', methods=['GET'])
def get_user_list():
    try:
        users = User.query.all()
        user_list = [
            {
                'uid': user.uid,
                'name': user.name,
                'gender': user.gender
            } for user in users
        ]
        return jsonify({'success': True, 'data': user_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# 2. 添加用户接口
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.json
        name = data.get('name')
        gender = data.get('gender')

        if not name or not gender:
            return jsonify({'success': False, 'message': 'Name and gender are required'}), 400

        new_user = User(name=name, gender=gender)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'User added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# 3. 编辑用户接口
@app.route('/edit_user/<int:uid>', methods=['PUT'])
def edit_user(uid):
    try:
        data = request.json
        user = User.query.get(uid)

        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        name = data.get('name')
        gender = data.get('gender')

        if name:
            user.name = name
        if gender:
            user.gender = gender

        db.session.commit()
        print(name,gender)

        return jsonify({'success': True, 'message': 'User updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
