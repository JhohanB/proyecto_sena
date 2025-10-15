from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional
import logging

from app.schemas.chickens import ChickenCreate, ChickenUpdate

logger = logging.getLogger(__name__)

def create_chicken(db: Session, chicken: ChickenCreate) -> Optional[bool]:
    try:
        sentencia = text("""
            INSERT INTO ingreso_gallinas (
                id_galpon, fecha,
                id_tipo_gallina, cantidad_gallinas
            ) VALUES (
                :id_galpon, :fecha,
                :id_tipo_gallina, :cantidad_gallinas
            )
        """)
        db.execute(sentencia, chicken.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear el registro de gallinas: {e}")
        raise Exception("Error de base de datos al crear el registro")


def get_chicken_by_id(db: Session, id_ingreso: int):
    try:
        query = text("""SELECT id_ingreso, id_galpon, fecha, id_tipo_gallina, raza, cantidad_gallinas
                     FROM ingreso_gallinas
                     JOIN tipo_gallinas ON ingreso_gallinas.id_tipo_gallina = tipo_gallinas.id_tipo_gallinas
                     WHERE id_ingreso = :ingreso
                """)
        result = db.execute(query, {"ingreso": id_ingreso}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener el registro por id: {e}")
        raise Exception("Error de base de datos al obtener el registro")


def get_chicken_by_galpon(db: Session, id_galpon: int):
    try:
        query = text("""SELECT id_ingreso, id_galpon, fecha, id_tipo_gallina, raza, cantidad_gallinas
                     FROM ingreso_gallinas
                     JOIN tipo_gallinas ON ingreso_gallinas.id_tipo_gallina = tipo_gallinas.id_tipo_gallinas
                     WHERE id_galpon = :galpon
                """)
        result = db.execute(query, {"galpon": id_galpon}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener el registro por galpon: {e}")
        raise Exception("Error de base de datos al obtener el registro")


def get_all_chickens(db: Session):
    try:
        query = text("""SELECT id_ingreso, id_galpon, fecha, id_tipo_gallina, raza, cantidad_gallinas
                     FROM ingreso_gallinas
                     JOIN tipo_gallinas ON ingreso_gallinas.id_tipo_gallina = tipo_gallinas.id_tipo_gallinas
                """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener los registros: {e}")
        raise Exception("Error de base de datos al obtener los registros")


def update_chickens_by_id(db: Session, id_ingreso: int, chicken: ChickenUpdate) -> Optional[bool]:
    try:
        # Solo los campos enviados por el cliente
        chicken_data = chicken.model_dump(exclude_unset=True)
        if not chicken_data:
            return False  # nada que actualizar


        # Construir dinámicamente la sentencia UPDATE
        set_clauses = ", ".join([f"{key} = :{key}" for key in chicken_data.keys()])
        sentencia = text(f"""
            UPDATE ingreso_gallinas 
            SET {set_clauses}
            WHERE id_ingreso = :id_ingreso
        """)

        # Agregar el id_usuario
        chicken_data["id_ingreso"] = id_ingreso

        result = db.execute(sentencia, chicken_data)
        db.commit()

        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar el registro {id_ingreso}: {e}")
        raise Exception("Error de base de datos al actualizar el registro")


def get_chicken_by_id(db: Session, id_ingreso: int):
    try:
        query = text("""SELECT id_ingreso, id_galpon, fecha, id_tipo_gallina, raza, cantidad_gallinas
                     FROM ingreso_gallinas
                     JOIN tipo_gallinas ON ingreso_gallinas.id_tipo_gallina = tipo_gallinas.id_tipo_gallinas
                     WHERE id_ingreso = :id
                """)
        result = db.execute(query, {"id": id_ingreso}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener el registro por id: {e}")
        raise Exception("Error de base de datos al obtener el registro")