import os
import sqlite3
from contextlib import contextmanager
from datetime import date, time
from pathlib import Path

from objetos.Cliente import Cliente
from objetos.Profesional import Profesional
from objetos.Servicio import Servicio
from objetos.Turno import Turno


RUTA_BASE_DATOS = Path(
    os.getenv(
        "SPA_DB",
        Path(__file__).resolve().parents[1] / "spa.db",
    )
)


@contextmanager
def _conexion():
    conexion = sqlite3.connect(RUTA_BASE_DATOS, timeout=10)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    try:
        with conexion:
            yield conexion
    finally:
        conexion.close()


def inicializar_base_datos():
    with _conexion() as conexion:
        conexion.executescript(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT NOT NULL,
                telefono TEXT NOT NULL,
                email TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS profesionales (
                id_profesional INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT NOT NULL,
                telefono TEXT NOT NULL,
                email TEXT NOT NULL,
                especialidad TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS servicios (
                id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                duracion INTEGER NOT NULL CHECK (duracion > 0),
                precio NUMERIC NOT NULL CHECK (precio >= 0)
            );

            CREATE TABLE IF NOT EXISTS turnos (
                id_turno INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                id_profesional INTEGER NOT NULL,
                id_servicio INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'Activo'
                    CHECK (estado IN ('Activo', 'Cancelado')),
                FOREIGN KEY (id_cliente)
                    REFERENCES clientes (id_cliente),
                FOREIGN KEY (id_profesional)
                    REFERENCES profesionales (id_profesional),
                FOREIGN KEY (id_servicio)
                    REFERENCES servicios (id_servicio)
            );

            CREATE UNIQUE INDEX IF NOT EXISTS
                ux_turnos_profesional_horario_activo
            ON turnos (id_profesional, fecha, hora)
            WHERE estado = 'Activo';
            """
        )


def registrar_cliente(nombre, apellido, dni, telefono, email):
    with _conexion() as conexion:
        cursor = conexion.execute(
            """
            INSERT INTO clientes (nombre, apellido, dni, telefono, email)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nombre, apellido, dni, telefono, email),
        )
        return cursor.lastrowid


def registrar_profesional(
    nombre, apellido, dni, telefono, email, especialidad
):
    with _conexion() as conexion:
        cursor = conexion.execute(
            """
            INSERT INTO profesionales
                (nombre, apellido, dni, telefono, email, especialidad)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (nombre, apellido, dni, telefono, email, especialidad),
        )
        return cursor.lastrowid


def registrar_servicio(nombre, descripcion, duracion, precio):
    with _conexion() as conexion:
        cursor = conexion.execute(
            """
            INSERT INTO servicios (nombre, descripcion, duracion, precio)
            VALUES (?, ?, ?, ?)
            """,
            (nombre, descripcion, duracion, precio),
        )
        return cursor.lastrowid


def obtener_clientes():
    with _conexion() as conexion:
        filas = conexion.execute(
            """
            SELECT id_cliente, nombre, apellido, dni, telefono, email
            FROM clientes
            ORDER BY id_cliente
            """
        ).fetchall()
    return [Cliente(*fila) for fila in filas]


def obtener_profesionales():
    with _conexion() as conexion:
        filas = conexion.execute(
            """
            SELECT
                id_profesional, nombre, apellido, dni, telefono, email,
                especialidad
            FROM profesionales
            ORDER BY id_profesional
            """
        ).fetchall()
    return [Profesional(*fila) for fila in filas]


def obtener_servicios():
    with _conexion() as conexion:
        filas = conexion.execute(
            """
            SELECT id_servicio, nombre, descripcion, duracion, precio
            FROM servicios
            ORDER BY id_servicio
            """
        ).fetchall()
    return [Servicio(*fila) for fila in filas]


def registrar_turno(id_cliente, id_profesional, id_servicio, fecha, hora):
    try:
        with _conexion() as conexion:
            cursor = conexion.execute(
                """
                INSERT INTO turnos
                    (id_cliente, id_profesional, id_servicio, fecha, hora)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    id_cliente,
                    id_profesional,
                    id_servicio,
                    fecha.isoformat(),
                    hora.strftime("%H:%M"),
                ),
            )
            return cursor.lastrowid
    except sqlite3.IntegrityError as error:
        if "ux_turnos_profesional_horario_activo" in str(error):
            raise ValueError(
                "El profesional no está disponible en ese horario."
            ) from error
        raise


def horario_ocupado(id_profesional, fecha, hora):
    with _conexion() as conexion:
        fila = conexion.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM turnos
                WHERE id_profesional = ?
                  AND fecha = ?
                  AND hora = ?
                  AND estado = 'Activo'
            )
            """,
            (id_profesional, fecha.isoformat(), hora.strftime("%H:%M")),
        ).fetchone()
    return bool(fila[0])


def obtener_turnos():
    with _conexion() as conexion:
        filas = conexion.execute(
            """
            SELECT
                t.id_turno,
                c.id_cliente, c.nombre, c.apellido, c.dni, c.telefono, c.email,
                p.id_profesional, p.nombre, p.apellido, p.dni, p.telefono,
                p.email, p.especialidad,
                s.id_servicio, s.nombre, s.descripcion, s.duracion, s.precio,
                t.fecha, t.hora, t.estado
            FROM turnos AS t
            JOIN clientes AS c ON c.id_cliente = t.id_cliente
            JOIN profesionales AS p
                ON p.id_profesional = t.id_profesional
            JOIN servicios AS s ON s.id_servicio = t.id_servicio
            ORDER BY t.fecha, t.hora, t.id_turno
            """
        ).fetchall()

    turnos = []
    for fila in filas:
        cliente = Cliente(*fila[1:7])
        profesional = Profesional(*fila[7:14])
        servicio = Servicio(*fila[14:19])
        turnos.append(
            Turno(
                fila[0],
                cliente,
                profesional,
                servicio,
                date.fromisoformat(fila[19]),
                time.fromisoformat(fila[20]),
                fila[21],
            )
        )
    return turnos


def cancelar_turno(id_turno):
    with _conexion() as conexion:
        cursor = conexion.execute(
            """
            UPDATE turnos
            SET estado = 'Cancelado'
            WHERE id_turno = ? AND estado = 'Activo'
            """,
            (id_turno,),
        )
        return cursor.rowcount > 0


inicializar_base_datos()
