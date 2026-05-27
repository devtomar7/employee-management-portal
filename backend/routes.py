from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

employee_bp = Blueprint("employee", __name__)

# HOME
@routes.route("/")
def home():
    return "Backend is running"


# CREATE (POST)
@routes.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get('name')
    email = data.get('email')
    role = data.get('role')
    salary = data.get('salary')

    if not all([name, email, role, salary]):
        return jsonify({"error": "Missing fields"}), 400

    new_emp = Employee(
        name=name,
        email=email,
        role=role,
        salary=salary
    )

    db.session.add(new_emp)
    db.session.commit()

    return jsonify({
        "message": "Employee added successfully",
        "employee": new_emp.to_dict()
    })


# READ (GET)
@routes.route("/employees", methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    return jsonify([e.to_dict() for e in employees])


# UPDATE (PUT)
@routes.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):
    emp = Employee.query.get(id)

    if not emp:
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json()

    emp.name = data.get("name")
    emp.email = data.get("email")
    emp.role = data.get("role")
    emp.salary = data.get("salary")

    db.session.commit()

    return jsonify({"message": "Updated successfully"})


# DELETE
@routes.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    emp = Employee.query.get(id)

    if not emp:
        return jsonify({"error": "Employee not found"}), 404

    db.session.delete(emp)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"})