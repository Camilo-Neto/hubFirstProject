from flask import Blueprint, request, jsonify
from models.userModels import User as UserModel

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/api/users', methods=['POST'])
async def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    idade = data.get("idade")
    role = data.get("role", "user")
    password = data.get("senha")
    
    if not name or not email or not idade:
        return jsonify({"message": "Name, email and idade are required"}), 400

    user = await UserModel.create_user(name, email, idade, password, role)
    return jsonify({"id": user.id, "name": user.name, "email": user.email, "idade": user.idade, "senha": user.password, "role": user.role}), 201


@user_routes.route('/api/users', methods=['GET'])
async def get_users():
    users = await UserModel.get_all_users()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email, "idade": user.idade, "role": user.role,"senha": user.password} for user in users])


@user_routes.route('/api/users/<int:user_id>', methods=['GET'])
async def get_user(user_id):
    user = await UserModel.get_user_by_id(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email, "idade": user.idade, "role": user.role, "senha": user.password})
    return jsonify({"message": "User not found"}), 404


@user_routes.route('/api/users/<int:user_id>', methods=['PUT'])
async def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    idade = data.get("idade")
    role = data.get("role", "user")
    password = data.get("senha")

    if not name or not email:
        return jsonify({"message": "Name and email are required"}), 400

    updated_user = await UserModel.update_user(user_id, name, email, idade, password, role)
    if updated_user:
        return jsonify({"id": updated_user.id, "name": updated_user.name, "email": updated_user.email, "idade": updated_user.idade, "role": updated_user.role, "senha": updated_user.password})
    return jsonify({"message": "User not found"}), 404

# Deletar um usuário
@user_routes.route('/api/users/<int:user_id>', methods=['DELETE'])
async def delete_user(user_id):
    deleted_user = await UserModel.delete_user(user_id)
    if deleted_user:
        return jsonify({"id": deleted_user.id, "name": deleted_user.name, "email": deleted_user.email, "role": deleted_user.role, "idade": deleted_user.idade, "senha": deleted_user.password})
    return jsonify({"message": "User not found"}), 404
