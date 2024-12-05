from quart import Blueprint, request, jsonify
from models import userModels

user_routes = Blueprint('user', __name__, url_prefix='/users')

@user_routes.route('/', methods=['GET'])
async def get_users():
    users = await userModels.User.all()
    users_dict = [
        {"id": user.id, "name": user.name, "email": user.email, "idade": user.idade, "role": user.role, "senha": user.password} for user in users
    ]
    return jsonify(users_dict)

@user_routes.route('/<int:user_id>', methods=['GET'])
async def get_user(user_id):
    user = await userModels.User.get_or_none(id=user_id)
    if user:
        user_dict = {"id": user.id, "name": user.name, "email": user.email, "idade": user.idade, "role": user.role, "senha": user.password}
        return jsonify(user_dict)
    return jsonify({"error": "Usuário não encontrado"}), 404

@user_routes.route('/', methods=['POST'])
async def create_user():
    try:
        data = await request.get_json()
        role = data.get("role", "user")
        user = await userModels.User.create( 
            
            name=data["name"],
            email=data["email"],
            password=data["password"],  
            role = role,
            idade = data["idade"]
        )

        return jsonify({"id": user.id, "name": user.name, "email": user.email, "idade": user.idade, "role": user.role, "senha": user.password}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_routes.route('/<int:user_id>', methods=['PUT'])
async def update_user(user_id):
    try:
        data = await request.get_json()
        user = await userModels.User.get_or_none(id=user_id)
        if user:
            await user.update_from_dict(data)
            await user.save()
            updated_user = {"id": user.id, "name": user.name, "email": user.email, "idade": user.idade, "role": user.role, "senha": user.password}
            return jsonify(updated_user)
        return jsonify({"error": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_routes.route('/<int:user_id>', methods=['DELETE'])
async def delete_user(user_id):
    user = await userModels.User.get_or_none(id=user_id)
    if user:
        await user.delete()
        return jsonify({"message": "Usuário deletado com sucesso."})
    return jsonify({"error": "Usuário não encontrado"}), 404
