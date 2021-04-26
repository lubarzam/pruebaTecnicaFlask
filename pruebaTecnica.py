# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, abort, reqparse
from itertools import combinations_with_replacement, product, islice
import string
import pandas as pd


# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)



#crear combinatios de letras del alfabeto 4 veces
letras = combinations_with_replacement(string.ascii_uppercase, 4)
#crear combinación de digitos 3 veces
digitos = combinations_with_replacement(string.digits, 3)

#crea las patentes como tuplas de 4 letras y 3 digitos
patentes = tuple(product(letras, digitos)) 



def buscar_patente(patente_code):

	""" busca la patente ingresada"""


	i = 0 #inicializa el contador que corrsponderá al id de la patente encontrada

	for p in patentes:  #recorre el lisatdo de patentes
			
		if patente_code==p: # compara el valor ingresado con la patente generada

			
			# si corresponde la patente se devuelve en formato de string, uniendo las tuplas de letras y numeros
			return {'patente':f'{"".join(p[0])}'+f'{"".join(p[1])}', 'id':i}
		i+=1 #incrementa el id 

	return False # si no se ha retornado una patente es porque noe xite y retorna False


def buscar_id(patente_id):

	if patente_id > len(patentes): #verifica si el id está dentro del dominio 

		#retorna el error correspondiente
		return {'error':'El id excede el total de patentes'} 



	#busca la patente en las lista de acuerdo a la posición entregada
	patente_code = list(islice(patentes, patente_id, patente_id+1))[0]


	#retorna el id y la patente en formato de String uniendo las tuplas de letras y numeros
	return {'id':patente_id, 'patente':f'{"".join(patente_code[0])}'f'{"".join(patente_code[1])}'}



class BuscarId(Resource): # Resource correspondiente al primer endpoint solicitado. Se entrega una patente y retorna un ID

	# corresponds to the GET request.
	# this function is called whenever there
	# is a GET request for this resource
	def get(self, patente_code):

		

		if patente_code.isalnum(): # verifica si la patente ingresada es alfanumerica

			#separa la patente en elementos de una tupla
			exploded_patente = [d for d in patente_code]

			#crea una tupla para almacenar los priemros cuatro elementos que corresponden a las letras				
			letras = tuple(exploded_patente[:4])

			#crea una tupla para almacenar los elemento del 4 en adelante que correspodne a los numeros
			numeros = tuple(exploded_patente[4:])

			#crea una tupla con las tuplas de letras y numeros
			patente_tuple = (letras, numeros)

			# llama a la función buscar_patente(), entregando la patente en formato de tupla
			patente_id = buscar_patente(patente_tuple)

			#si el valor retornado es verdadero se devuelve al cliente
			if patente_id:
				
				return patente_id

			# si el valor retornado es False significa que al patente no fue encontrada
			else: return {'error': 'Patente no encontrada'}

		else: # Si la patente ingresada no es alfanumerica no puede ser procesada y se muestra el error

			return {'error': 'La patente debe ser alfanumerica'}



class BuscarPatente(Resource):


	# corresponds to the GET request.
	# this function is called whenever there
	# is a GET request for this resource
	def get(self, patente_id):

		if patente_id.isnumeric(): # verifica si el id ingresado es numerico

			#llama a la función buscar_id(), entregando el id como entero
			return buscar_id(int(patente_id))

		else: #si el id no está en formato numérico se muestra el erro correspondiente
			return {'error': 'El id debe ser un numero entero'}





class SumaMatriz(Resource):
	"""docstring for SumaMatriz"""
	def get(self):
		
		#recibe todos los parámetros ingresado por url
		r=request.args.get('r') 
		c=request.args.get('c')
		x=request.args.get('x')
		y=request.args.get('y')
		z=request.args.get('z')
	

		#verifica si todos los parámetros requeridos han sido ingresados y con valor numérico.
		for param in [r,c,x,y,z]:
			if not param.isnumeric(): # si hay algun parámetro que posee valor no numérico (o vacío) se muestra el eeror correspondiente

				return {'error':'Uno de los parametros ingresado no es numerico'}


		# ya validados los parámetros son convertidos a enteros				
		r=int(r)
		c=int(c)
		x=int(x)
		y=int(y)
		z=int(z)

		if r>0 and c>0 and x>=0 and y>=0 and z>0 and z<=1000000:

			# se crea un dataframe vacío con R filas x C columnas
			df= pd.DataFrame(index=range(0,r), columns=range(0,c))


			#se itera a travpes de las filas del dataframe para ir asignando sus valores
			for i, row in df.iterrows():
			    if i==0: # si es la primera fila se asigna el valor de Z
			         df.iloc[i] = z
			    else: # si una fila distinta a la primera se asigna el valro de Z mas el valor de la fila anterior menos 1
			        df.iloc[i] = z + df.iloc[i-1]-1
			       
			#Se redefine la matriz considerando solo als filas y columnas delimitadas por y y x
			df=df.iloc[0:y+1, 0:x+1]
			

			#se calcula la sumatoria de las filas y se asigna al dataframe de una columna sum_rows
			sum_rows=df.sum(axis=1)

			#Se calcula la sumatorio de la columna que contiene la sumatoria de las filas y se asigna a la variable suma
			suma=sum_rows.sum(axis=0)
			
			#La variable suma es convertida en entero
			suma=int(suma)

			# el valor de la sumatoria es retornado al usuario
			return {'Suma de la submatriz x, y:':suma}

		else:
			return {'error':'Alguno de los parametros ingresados no cumple las restricciones'}




		



# adding the defined resources along with their corresponding urls
api.add_resource(BuscarId, '/buscar_patente/<string:patente_code>')
api.add_resource(BuscarPatente, '/buscar_id/<string:patente_id>')
api.add_resource(SumaMatriz, '/sumar_matriz')
#api.add_resource(square, '/square/<int:num>')


# driver function
if __name__ == '__main__':

	app.run(debug = True)
