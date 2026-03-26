# Python: 3.9.7
# QT5 (pyqt5)
# Libreria para crear ejecutables (pyinstaller)
# pip install pyinstaller
# Librerias
import sys, re, pandas, json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import *

# Clase 
class Aplicacion(QMainWindow):
    # Constructor
    def __init__(self):
        # Constructor de la clase heredada
        super(Aplicacion, self).__init__()
        # Cargar la interfaz
        loadUi(r"C:\Python 19-21\Aplicaciones\interfaz.ui",self)
        # Validadores
        self.txtID.setValidator(QIntValidator())
        self.txtCantidad.setValidator(QIntValidator())
        self.txtPrecio.setValidator(QDoubleValidator())
        # Ajustar las columnas al ancho de la tabla
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Importar los datos y mostrarlos en el frontend
        self.importar()
        self.mostrar_datos()
        # Vincular botones
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnBuscar.clicked.connect(self.buscar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnActualizar.clicked.connect(self.actualizar)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnImportar.clicked.connect(self.importar)
        self.btnExportar.clicked.connect(self.exportar)
        # Deshabilitar, eliminar y actualizar
        self.btnEliminar.setEnabled(False)
        self.btnActualizar.setEnabled(False)

    def agregar(self):
        try:
            id = int(self.txtID.text())
            producto = str(self.txtProducto.text())
            cantidad = int(self.txtCantidad.text())
            precio = float(self.txtPrecio.text())

            if id == 0:
                QMessageBox.warning(self,"ID","El ID no puede ser cero")
                return
            
            if producto == 0:
                QMessageBox.warning(self,"Producto","Capture el nombre del producto")
                return
            
            if cantidad == 0:
                QMessageBox.warning(self,"Cantidad","La cantidad no puede ser cero")
                return
            
            if precio == 0:
                QMessageBox.warning(self,"Precio","El Precio no puede ser cero")
                return
            # Cargar el inventario
            inventario = self.importar()
            # Revisar que no haya ID duplicados
            # p recorre los registros del inventario (JSON)
            # Si alguno de los valores de la columna ID es igual al id... se detiene
            if any(p["ID"] == id for p in inventario):
                QMessageBox.warning(self,"Error","El ID ingresado ya fue asignado")
                return 
            
            if any(p["PRODUCTO"] == producto for p in inventario):
                QMessageBox.warning(self,"Error",f"El producto {producto} anteriormente ya fue registrado")
                return 
            # Agregar la informacion al inventario
            registro = {"ID": id,
                        "PRODUCTO": producto,
                        "CANTIDAD": cantidad,
                        "PRECIO": precio
                        }

            inventario.append(registro)

            # Guardar la informacion
            self.guardar_datos(inventario)

            # Limpiar la interfaz
            self.txtID.clear()
            self.txtProducto.clear()
            self.txtCantidad.clear()
            self.txtPrecio.clear()

            QMessageBox.information(self,"Registro","Informacion registrada con exito")

            self.mostrar_datos()

        except ValueError:
            QMessageBox.warning(self,"Error","Corrobore la informacion capturada")
    
    def buscar(self):
        try:
            id = int(self.txtID.text())

            inventario = self.importar()

            producto_encontrado = False

            # Buscar el ID dentro del inventario
            for producto in inventario:
                if producto["ID"] == id:
                    # Si el ID existe llevamos los datos al frontend
                    self.txtProducto.setText(producto["PRODUCTO"])
                    self.txtCantidad.setText(str(producto["CANTIDAD"]))
                    self.txtPrecio.setText(str(producto["PRECIO"]))
                    producto_encontrado = True
                    QMessageBox.information(self,"Atencion","Producto encontrado")
                    # Habilitar "Eliminar" y "Actualizar"
                    self.btnEliminar.setEnabled(True)
                    self.btnActualizar.setEnabled(True)
                    break # Salir del ciclo

            if producto_encontrado == False:
                QMessageBox.warning(self,"Error","El ID mostrado no existe")
                

        except ValueError:
            QMessageBox.warning(self,"Error","Capture un ID valido")

            
    def eliminar(self):
        try:
            id = int(self.txtID.text())

            if id == 0:
                QMessageBox.warning(self,"Error","El ID no puede ser cero")
                return
            
            # Cargar el inventario
            inventario = self.importar()

            # Objeto que recibe los productos cuyo ID no es el de la variable 'id'
            # p es el iterador que recorre el inventario
            # invenvario contiene todos los registros
            # p for p = en la variable/iterador 'p' se conserva el registro sies diferente de la variable id
            movimiento = [p for p in inventario if p["ID"] != id]

            # Determinar si el id ingresado existe
            if len(movimiento) == len(inventario):
                QMessageBox.warning(self,"Error","El ID no existe")
            else:
                # Refrescar el archivo
                self.guardar_datos(movimiento)
                # Actualizar la interfaz
                self.mostrar_datos()

                # Deshabilitar eliminar y actualizar
                #Habilitar "Eliminar" y "Actualizar"
                self.btnEliminar.setEnabled(False)
                self.btnActualizar.setEnabled(False)
                QMessageBox.information(self,"Eliminar","Registro eliminado con exito")
        except ValueError:
            QMessageBox.warning(self,"Error","Capture un ID valido")


    def actualizar(self):    
        # Obtener los datos de las cajas
        id = int(self.txtID.text())
        producto_nuevo = str(self.txtProducto.text())
        cantidad_nuevo = int(self.txtCantidad.text())
        precio_nuevo = float(self.txtPrecio.text())
        # Cargar el inventario
        inventario = self.importar()
        # Buscar el producto a través del ID
        for producto in inventario:
        # Reemplazo de datos en las columnas especificadas
            if producto["ID"] == id:
                producto["PRODUCTO"] = producto_nuevo
                producto["CANTIDAD"] = cantidad_nuevo
                producto["PRECIO"] = precio_nuevo
                QMessageBox.information(self,"Actualizacion","Registro actualizado con exito")
                # Refrescar datos e interfaz
                self.guardar_datos(inventario)
                self.mostrar_datos()
                break


    def cancelar(self):
        # Limpiar
        self.txtID.clear()
        self.txtProducto.clear()
        self.txtCantidad.clear()
        self.txtPrecio.clear()
        # Deshabilitar "Eliminar" y "Actualizar"
        self.btnEliminar.setEnabled(False)
        self.btnActualizar.setEnabled(False)
        QMessageBox.information(self,"Atencion","Se canceló la operacion")


    def exportar(self):
        # Cargo los datos actuales
        inventario = self.importar()

        # Configurar la ruta de salida
        with open("C:/Python 19-21/Aplicaciones/inventario.json","w") as archivo:
            json.dump(inventario, archivo, indent=4)

        QMessageBox.information(self,"Atencion","Archivo exportado con exito")
        

    def importar(self):
        try:
            with open("C:/Python 19-21/Aplicaciones/inventario.json") as archivo:
                # Devolver los datos del archivo al sistema
                # Los datos estaran disponibles a nivel digital
                return json.load(archivo)
        except FileNotFoundError:
            QMessageBox.warning(self,"Error","Error al cargar el archivo")

    def mostrar_datos(self):
        # Mandar llamar los datos
        inventario = self.importar()
        # Limpiar la tabla
        self.tabla.setRowCount(0)
        # Llenar la tabla con los datos
        # Fila = iterador de los registros (saber cuantas veces voy a recorrerlo)
        # producto = objeto que puede extraer el valor del registro JSON
        # enumerate(inventario) = cuenta la cantidad de diccionarios del JSON
        for fila, producto in enumerate(inventario):
            # Agregar una fila nueva a la tabla del frontend
            self.tabla.insertRow(fila)
            # Incorporar los datos a las celdas de cada fila de la tabla
            id = QTableWidgetItem(str(producto["ID"]))
            prod = QTableWidgetItem(str(producto["PRODUCTO"]))
            cantidad = QTableWidgetItem(str(producto["CANTIDAD"]))
            precio = QTableWidgetItem(str(producto["PRECIO"]))

            self.tabla.setItem(fila,0,id)
            self.tabla.setItem(fila,1,prod)
            self.tabla.setItem(fila,2,cantidad)
            self.tabla.setItem(fila,3,precio)

                      
    def guardar_datos(self, inventario):
            # Guardar la información dentro del archivo JSON
            with open("C:/Python 19-21/Aplicaciones/inventario.json","w") as archivo:
                json.dump(inventario, archivo, indent=4)                
        

# Estructura de arranque
if __name__ == "__main__":
    # Instancia del backend
    app = QApplication(sys.argv)
    # Instancia del frontend
    aplicacion = Aplicacion()
    # Muestro la interfaz
    aplicacion.show()
    # Ejecuto el programa
    app.exec()