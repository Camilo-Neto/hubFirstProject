from quart import Quart, jsonify, request
from tortoise import Tortoise
from routes.user_routes import user_routes

app = Quart(__name__)

DB_URL = 'sqlite://db.sqlite3'
MODELS = ['models.userModels']

app.config['ASYNC_MODE'] = True


@app.before_serving
async def init():
    try:
     
        await Tortoise.init(
            db_url=DB_URL,
            modules={"models": MODELS},  
        )
        
        await Tortoise.generate_schemas()
        print("Banco de dados conectado e schemas gerados.")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise

@app.after_serving
async def finish():
   
    await Tortoise.close_connections()
    print("Conexões com o banco de dados fechadas.")


app.register_blueprint(user_routes)

@app.route('/')
async def home():
    return 'Bem-vindo'

if __name__ == "__main__":
    app.run(debug=True)



TORTOISE_ORM = {
    "connections": {
        "default": DB_URL,  
    },
    "apps": {
        "models": {
            "models": MODELS + ["aerich.models"],
            "default_connection": "default",
        },
    },
}
