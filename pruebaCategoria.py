import datetime


fecha = datetime.datetime(1964, 2, 1)


def parsear_categoria(anyio):
    if anyio <= 1975:
        return "VET C"
    elif anyio >= 1976 and anyio <= 1979:
        return "VET B"
    elif anyio >= 1980 and anyio <= 1985:
        return "VET A"
    elif anyio >= 1986 and anyio <= 2007:
        return "SENIOR"
    elif anyio >= 2008:
        return "JUNIOR"
  
    
print(parsear_categoria(fecha.year))


#------------------------------------------------------------
#-------------------------------------------------------------


from utils.TrailDataBase import TrailDataBase

db = TrailDataBase()

#inscritos2025 = db.obtener_inscritos_por_edicion(datetime.datetime.now().year)
inscritos2025 = db.obtener_inscritos_por_tipo_carrera("andarines", datetime.datetime.now().year)

for inscrito in inscritos2025:
    print(f"{inscrito.dorsal} {inscrito.nombre} {inscrito.apellidos} {inscrito.ccaa} {inscrito.municipio} {parsear_categoria(inscrito.fecha_nacimiento.year)}")

