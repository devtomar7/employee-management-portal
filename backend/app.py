# =========================
# IMPORTS
# =========================
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required
)

# =========================
# APP CONFIG
# =========================
app = Flask(__name__)
CORS(app)  # ✅ ENABLE CORS

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT CONFIG
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# =========================
# DUMMY USER (LOGIN)
# =========================
USER = {
    "username": "admin",
    "password": "1234"
}

# =========================
# MODEL
# =========================
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "salary": self.salary
        }

# =========================
# HOME
# =========================
@app.route('/')
def home():
    return jsonify({"message": "Employee Management Backend Running 🚀"})

# =========================
# LOGIN ROUTE
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if username == USER["username"] and password == USER["password"]:
        token = create_access_token(identity=username)
        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401

# =========================
# GET ALL (PROTECTED)
# =========================
@app.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees]), 200

# =========================
# ADD EMPLOYEE (PROTECTED)
# =========================
@app.route('/employees', methods=['POST'])
@jwt_required()
def add_employee():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get('name')
        email = data.get('email')
        department = data.get('department')
        salary = data.get('salary')

        if not all([name, email, department, salary]):
            return jsonify({"error": "All fields are required"}), 400

        existing = Employee.query.filter_by(email=email).first()
        if existing:
            return jsonify({"error": "Email already exists"}), 409

        new_emp = Employee(
            name=name,
            email=email,
            department=department,
            salary=salary
        )

        db.session.add(new_emp)
        db.session.commit()

        return jsonify({
            "message": "Employee added successfully",
            "employee": new_emp.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================
# DELETE (PROTECTED)
# =========================
@app.route('/employees/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    emp = Employee.query.get(id)

    if not emp:
        return jsonify({"error": "Employee not found"}), 404

    db.session.delete(emp)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"}), 200

# =========================
# UPDATE (PROTECTED)
# =========================
@app.route('/employees/<int:id>', methods=['PUT'])
@jwt_required()
def update_employee(id):
    try:
        emp = Employee.query.get(id)

        if not emp:
            return jsonify({"error": "Employee not found"}), 404

        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        if 'name' in data:
            emp.name = data['name']

        if 'email' in data:
            existing = Employee.query.filter_by(email=data['email']).first()
            if existing and existing.id != id:
                return jsonify({"error": "Email already exists"}), 409
            emp.email = data['email']

        if 'department' in data:
            emp.department = data['department']

        if 'salary' in data:
            emp.salary = data['salary']

        db.session.commit()

        return jsonify({
            "message": "Employee updated successfully",
            "employee": emp.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================
# RUN
# =========================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)