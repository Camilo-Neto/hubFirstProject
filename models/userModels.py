from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=128)
    idade = fields.IntField(null=True)
    role = fields.CharField(max_length=20, default="user")

    def is_admin(self):
        return self.role == "admin"
    
    class Meta:
        table = "users"

    @staticmethod
    async def get_all_users():
        return await User.all()

    @staticmethod
    async def get_user_by_id(user_id):
        return await User.get_or_none(id=user_id)

    @staticmethod
    async def create_user(name, email, idade, role, password):
        return await User.create(name=name, email=email, idade=idade, role=role, password=password)

    @staticmethod
    async def update_user(user_id, name, email, idade, role, password):
        user = await User.get_or_none(id=user_id)
        if user:
            user.name = name
            user.email = email
            user.idade = idade
            user.role = role
            user.password = password
            await user.save()
            return user
        return None

    @staticmethod
    async def delete_user(user_id):
        user = await User.get_or_none(id=user_id)
        if user:
            await user.delete()
            return user
        return None
