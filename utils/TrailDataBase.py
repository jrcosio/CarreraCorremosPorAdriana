from sqlalchemy import (
    create_engine, Column, Integer, String, Date, CHAR, Boolean, ForeignKey, TIMESTAMP, CheckConstraint, Index, text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
import os
import logging
from datetime import date, datetime
from dotenv import load_dotenv

load_dotenv(override=True)

log = logging.getLogger(__name__)
# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Base para los modelos ORM
Base = declarative_base()

# ORM: Tabla Inscritos
class Inscrito(Base):
    __tablename__ = "inscritos"

    id = Column(Integer, primary_key=True)
    dorsal = Column(String(4), nullable=False)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(100), nullable=False)
    sexo = Column(CHAR(1), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    telefono = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False)
    tipo_documento = Column(String(20), nullable=False)
    numero_documento = Column(String(30), nullable=False)
    direccion = Column(String(100), nullable=False)
    ccaa = Column(String(60), nullable=False)
    municipio = Column(String(50), nullable=False)
    tipo_carrera = Column(String(20), nullable=False)
    talla = Column(String(10), nullable=False)
    contacto_emergencia = Column(String(100), nullable=False)
    telefono_emergencia = Column(String(15), nullable=False)
    edicion = Column(Integer, nullable=False)
    pagado = Column(Boolean, default=False)

    clasificaciones = relationship("Clasificacion", back_populates="inscrito", cascade="all, delete")

    __table_args__ = (
        CheckConstraint(sexo.in_(['M', 'F']), name='chk_sexo_valido'),
        CheckConstraint(tipo_carrera.in_(['trail', 'andarines']), name='chk_tipo_carrera_valido'),
        CheckConstraint(talla.in_(['S', 'M', 'L', 'XL', 'XXL']), name='chk_talla_valida'),
    )


class Clasificacion(Base):
    __tablename__ = "clasificacion"

    id = Column(Integer, primary_key=True)
    id_inscrito = Column(Integer, ForeignKey("inscritos.id", ondelete="CASCADE"), nullable=False)
    edicion = Column(Integer, nullable=False)
    tiempo_p1 = Column(TIMESTAMP)
    tiempo_final = Column(TIMESTAMP)
    finalizado = Column(Boolean, default=False)

    inscrito = relationship("Inscrito", back_populates="clasificaciones")

    __table_args__ = (
        Index("idx_clasificacion_edicion", "edicion"),
    )


class TrailDataBase:
    """
    Singleton para gestionar la base de datos PostgreSQL de trails/carreras
    """
    _instance = None
    _session = None
    _engine = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TrailDataBase, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Solo inicializar una vez
        if self._session is None:
            self._connect()
    
    def _connect(self):
        """Establece la conexión con PostgreSQL"""
        try:
            # Cargar variables de entorno desde .env
            load_dotenv()

            # Obtener credenciales de Gmail desde .env
            server_bd_url = os.getenv('SERVER_BD_URL')
            server_bd_user = os.getenv('SERVER_BD_USER')
            server_bd_password = os.getenv('SERVER_BD_PASSWORD')
            server_bd_name = os.getenv('SERVER_BD_NAME')
            
            print(f"Conectando a la base de datos {server_bd_name} en {server_bd_url} con usuario {server_bd_user}")
            
            if not server_bd_url or not server_bd_user or not server_bd_password or not server_bd_name:
                log.error("Faltan variables de entorno para la conexión a la base de datos")
                raise ValueError("Faltan variables de entorno para la conexión a la base de datos")
            # Construir URL de conexión PostgreSQL
            # Ejemplo: 'postgresql://user:password@localhost:5432/database_name'
            # Puedes usar variables de entorno o configuración directa
            db_url = f'postgresql://{server_bd_user}:{server_bd_password}@{server_bd_url}/{server_bd_name}'
            
            log.info(f"Conectando a PostgreSQL en {db_url}")
            # Crear engine con echo=False para producción
            self._engine = create_engine(db_url, echo=True)
            
            # Crear todas las tablas
            Base.metadata.create_all(self._engine)
            
            # Crear sesión
            Session = sessionmaker(bind=self._engine)
            self._session = Session()
            
            log.info("Conexión establecida con PostgreSQL")
            
        except SQLAlchemyError as e:
            log.error(f"Error conectando a PostgreSQL")
            raise
    
    @property
    def session(self):
        """Getter para la sesión"""
        return self._session
    # ============== METODO ESPECIAL CARRERA INICIADA ==============
    def Iniciar_Carrera(self, start_time: datetime | None = None) -> int:
        """
        Añade a la tabla `clasificacion` todos los inscritos cuya `edicion`
        coincida con el año actual (date.today().year) y fija `tiempo_p1`
        al mismo instante (por defecto, ahora mismo).  
        Devuelve el número total de corredores que quedan en la clasificación
        tras la operación (tanto los insertados como los actualizados).
        """
        if start_time is None:
            start_time = datetime.now()

        curr_year = date.today().year
        total_afectados = 0

        try:
            # 1) Traemos TODOS los inscritos de la edición actual
            inscritos = self.obtener_inscritos_por_edicion(curr_year)

            # 2) Para cada inscrito: insertar o actualizar su clasificación
            for ins in inscritos:
                clasif = self.obtener_clasificacion_por_inscrito(ins.id, curr_year)

                if clasif:
                    # Ya estaba en la tabla → solo actualizamos tiempo_p1
                    clasif.tiempo_p1 = start_time
                    self.actualizar(clasif)
                else:
                    # No existe → creamos nuevo objeto Clasificacion
                    nueva_clasif = Clasificacion(
                        id_inscrito = ins.id,
                        edicion     = curr_year,
                        tiempo_p1   = start_time,
                        finalizado  = False
                    )
                    self.insertar(nueva_clasif)

                total_afectados += 1

            return total_afectados

        except SQLAlchemyError as e:
            # Cualquier error: rollback y relanzar
            self._session.rollback()
            log.error("Error en Iniciar_Carrera", exc_info=e)
            raise
        
       
    # =================== MÉTODOS CRUD GENÉRICOS ===================
    
    def insertar(self, objeto):
        """Inserta un objeto en la base de datos"""
        try:
            self._session.add(objeto)
            self._session.commit()
            return objeto
        except SQLAlchemyError as e:
            self._session.rollback()
            log.error("Error insertando", exc_info=e)
            raise
    
    def obtener_por_id(self, tabla, id):
        """Obtiene un registro por ID"""
        try:
            return self._session.query(tabla).filter(tabla.id == id).first()
        except SQLAlchemyError as e:
            log.error(f"Error obteniendo por ID",  exc_info=e)
            return None
    
    def obtener_todos(self, tabla):
        """Obtiene todos los registros de una tabla"""
        try:
            return self._session.query(tabla).all()
        except SQLAlchemyError as e:
            log.error(f"Error obteniendo todos", exc_info=e)
            return []
    
    def actualizar(self, objeto):
        """Actualiza un objeto en la base de datos"""
        try:
            self._session.merge(objeto)
            self._session.commit()
            return objeto
        except SQLAlchemyError as e:
            self._session.rollback()
            log.error(f"Error actualizando", exc_info=e)
            raise
    
    def eliminar(self, objeto):
        """Elimina un objeto de la base de datos"""
        try:
            self._session.delete(objeto)
            self._session.commit()
            return True
        except SQLAlchemyError as e:
            self._session.rollback()
            log.error(f"Error eliminando", exc_info=e)
            return False
    
    # =================== MÉTODOS ESPECÍFICOS INSCRITOS ===================
    
    def obtener_inscrito_por_dorsal(self, dorsal, edicion):
        """Obtiene un inscrito por dorsal y edición"""
        try:
            return self._session.query(Inscrito).filter(
                Inscrito.dorsal == dorsal,
                Inscrito.edicion == edicion
            ).first()
        except SQLAlchemyError as e:
            log.error(f"Error obteniendo inscrito por dorsal", exc_info=e)
            return None
        
    def obtener_ultimo_dorsal(self, edicion, tipo_carrera):
        """Obtiene el último dorsal asignado en una edición"""
        try:
            ultimo_inscrito = self._session.query(Inscrito).filter(
                Inscrito.edicion == edicion,
                Inscrito.tipo_carrera == tipo_carrera
            ).order_by(Inscrito.id.desc()).first()
            return ultimo_inscrito.dorsal if ultimo_inscrito else None
        except SQLAlchemyError as e:
            log.error(f"Error obteniendo último dorsal", exc_info=e)
            return None
    
    def obtener_inscritos_por_tipo_carrera(self, tipo_carrera, edicion):
        """Obtiene inscritos por tipo de carrera y edición"""
        try:
            return self._session.query(Inscrito).filter(
                Inscrito.tipo_carrera == tipo_carrera,
                Inscrito.edicion == edicion
            ).all()
        except SQLAlchemyError as e:
            log.error(f"Error obteniendo inscritos por tipo", exc_info=e)  
            return []
    
    def obtener_inscritos_por_nombre(self, nombre):
        """Obtiene inscritos por nombre (búsqueda parcial)"""
        try:
            return self._session.query(Inscrito).filter(
                Inscrito.nombre.ilike(f'%{nombre}%')
            ).all()
        except SQLAlchemyError as e:
            log.error(f"Error obteniendo inscritos por nombre", exc_info=e)
            return []
    
    def obtener_inscritos_por_edicion(self, edicion):
        """Obtiene todos los inscritos de una edición"""
        try:
            return self._session.query(Inscrito).filter(
                Inscrito.edicion == edicion
            ).all()
        except SQLAlchemyError as e:
            log.error(f"Error obteniendo inscritos por edición", exc_info=e)
            return []
    
    def obtener_inscritos_por_tipo_carrera(self, tipo, edicion):
        """Obtiene todos los inscritos de una edición"""
        try:
            return self._session.query(Inscrito).filter(
                Inscrito.tipo_carrera == tipo,
                Inscrito.edicion == edicion
            ).all()
        except SQLAlchemyError as e:
            log.error(f"Error obteniendo inscritos por edición", exc_info=e)
            return []    
    
    
    # =================== MÉTODOS ESPECÍFICOS CLASIFICACIONES ===================
    
    def obtener_clasificacion_por_inscrito(self, id_inscrito, edicion):
        """Obtiene la clasificación de un inscrito en una edición"""
        try:
            return self._session.query(Clasificacion).filter(
                Clasificacion.id_inscrito == id_inscrito,
                Clasificacion.edicion == edicion
            ).first()
        except SQLAlchemyError as e:
            log.error(f"Error obteniendo clasificación por inscrito", exc_info=e)
            return None
    
    def obtener_clasificaciones_por_edicion(self, edicion):
        """Obtiene todas las clasificaciones de una edición"""
        try:
            return self._session.query(Clasificacion).filter(
                Clasificacion.edicion == edicion
            ).all()
        except SQLAlchemyError as e:
            log.error(f"Error obteniendo clasificaciones por edición", exc_info=e)
            return []
    
    def obtener_finalizados_por_edicion(self, edicion):
        """Obtiene solo los corredores que han finalizado en una edición"""
        try:
            return self._session.query(Clasificacion).filter(
                Clasificacion.edicion == edicion,
                Clasificacion.finalizado == True
            ).all()
        except SQLAlchemyError as e:
            log.error(f"Error obteniendo finalizados por edición", exc_info=e)
            return []
    
    # =================== UTILIDADES ===================
    
    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        if self._session:
            self._session.close()
        if self._engine:
            self._engine.dispose()
        log.info("Conexión a la base de datos cerrada")
    
    def ejecutar_query_personalizada(self, query):
        """Ejecuta una query personalizada"""
        try:
            return self._session.execute(query).fetchall()
        except SQLAlchemyError as e:
            log.error(f"Error ejecutando query personalizada", exc_info=e)
            return []


# =================== EJEMPLO DE USO ===================
if __name__ == "__main__":
    # Crear instancia singleton
    print("Iniciando conexión a la base de datos...\n\n\n\n")
    db = TrailDataBase()
    print("Conexión establecida.\n\n\n\n")
    
    # # Ejemplo de uso
    # try:
        
        
    # #     # filas = db.Iniciar_Carrera()   # hora de salida = ahora
    # #     # print(f"\n\n\n{filas} corredores añadidos a clasificacion")
        
    # #     # Clasificacion = db.obtener_clasificaciones_por_edicion(date.today().year)
    # #     # print(f"Clasificaciones de la edición {date.today().year}:")
    # #     # for clasif in Clasificacion:
    # #     #     print(f"Dorsal: {clasif.inscrito.dorsal} | {clasif.inscrito.nombre} | {clasif.inscrito.apellidos} | {clasif.inscrito.ccaa} | "
    # #     #           f"Edición: {clasif.edicion} | "
    # #     #           f"Tiempo Final: {clasif.tiempo_final}, ")
    # #     #         #   Tiempo P1: {clasif.tiempo_p1}, Finalizado: {clasif.finalizado}")
        
    #     #  inscrito = db.obtener_ultimo_dorsal(date.today().year, 'andarines')
    #     #  print(f"Último dorsal asignado en la edición {date.today().year}: {inscrito}")
        
        
        
    # except Exception as e:
    #      print(f"Error en ejemplo: {e}")
    
    # finally:
    #     # Cerrar conexión al finalizar
    #     db.cerrar_conexion()
    