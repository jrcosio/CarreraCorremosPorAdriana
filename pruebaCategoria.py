import datetime

#------------------------------------------------------------
#-------------------------------------------------------------


from utils.TrailDataBase import TrailDataBase

# db = TrailDataBase()

# #inscritos2025 = db.obtener_inscritos_por_edicion(datetime.datetime.now().year)
# inscritos2025 = db.obtener_inscritos_por_tipo_sexo("M","trail",2025)

# for incrito in inscritos2025:
#     print(incrito.nombre)


class main():
    
    def __init__(self):
        self.db = TrailDataBase()
        self.inscritosM = self.db.obtener_inscritos_por_tipo_sexo("M","trail",2025)
        #....flet
        
    
    
    def pintar_incritos(self):
        
        for inscrito in self.inscritosM:
            print(inscrito.nombre) 
        
if __name__ == "__main__":
    a = main()
    
    a.pintar_incritos()