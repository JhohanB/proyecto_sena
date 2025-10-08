from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from app.router import auth, rescue, users
=======
from app.router import auth, users, chickens, isolation
>>>>>>> c038be07d85f4541c32fd869570facaede2ad081

app = FastAPI()

# Incluir en el objeto app los routers
app.include_router(users.router, prefix="/users", tags=["usuarios"])
app.include_router(isolation.router, prefix="/isolations", tags=["aislamiento"])
app.include_router(auth.router, prefix="/access", tags=["login"])
<<<<<<< HEAD
app.include_router(rescue.router, prefix="/rescue", tags=["salvamentos"])
=======
app.include_router(chickens.router, prefix="/chickens", tags=["gallinas"])
>>>>>>> c038be07d85f4541c32fd869570facaede2ad081

# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)

@app.get("/")
def read_root():
    return {
                "message": "ok",
            }