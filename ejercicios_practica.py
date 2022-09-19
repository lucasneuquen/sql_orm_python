#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import sqlite3
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///secundaria.db")
base = declarative_base()


class Tutor(base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"Tutor: {self.name}"



class Estudiante(base):
    __tablename__ = "estudiante"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)
    tutor_id = Column(Integer, ForeignKey("tutor.id"))

    tutor = relationship("Tutor")

    def __repr__(self):
        return f"Estudiante: {self.name}, edad {self.age}, grado {self.grade}, tutor {self.tutor.name}"




def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    base.metadata.drop_all(engine)
    # Crear las tablas
    base.metadata.create_all(engine)

def fill():
    print('Completemos esta tablita!')
   
    tutores =["Marcos", "Sofía", "Daniel"]
   
    for x in range(len(tutores)):
        insert_tutor(tutores[x])
    

    estudiantes = [ ("Andrés", 13, 2, 1),
                    ("Vanesa", 17, 2, 2),
                    ("Pablo", 14, 1, 3),
                    ("Ludmila", 14, 2, 1),
                    ("Estefano", 16, 4, 3),
                    ("Mateo", 13, 4, 1)]

    for x in range(len(estudiantes)):
            insert_estudiante(estudiantes[x][0] ,estudiantes[x][1], estudiantes[x][2], estudiantes[x][3])




def fetch():
    print('Comprobemos su contenido, ¿qué hay en la tabla?')
    
   
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Buscar todos los estudiantes
    query = session.query(Estudiante)

    # Imprimir en pantalla cada objeto que traiga la query
    # Realizar un bucle para imprimir de una fila a la vez
    for estudiante in query:
        print(estudiante)



def search_by_tutor(tutor):
    print('Operación búsqueda!')
    # Esta función recibe como parámetro el nombre de un posible tutor.
    # Crear una query para imprimir en pantalla
    # aquellos estudiantes que tengan asignado dicho tutor.

    # Crear la session
    # Para poder realizar esta query debe usar join, ya que
    # deberá crear la query para la tabla estudiante pero
    # buscar por la propiedad de tutor.name    
    
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Estudiante).join(Estudiante.tutor).filter(Tutor.name == tutor)
        
    print("Estudiantes del tutor", tutor)
    for x in query:
            print(x.name)

 



def modify(id, nuevo_tutor):
    print('Modificando la tabla')
    # Deberá actualizar el tutor de un estudiante, cambiarlo para eso debera:
    
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 1) buscar con una query el tutor por "tutor.name" usando nuevo_tutor
    # pasado como parámetro y obtener el objeto del tutor
    query = session.query(Tutor).filter(Tutor.name == nuevo_tutor)
    tutor_act = query.first()
    
    # 2) buscar con una query el estudiante por "estudiante.id" usando
    # el id pasado como parámetro
    query = session.query(Estudiante).filter(Estudiante.id == id)
    estudiante_act = query.first()
    
    # 3) actualizar el objeto de tutor del estudiante con el obtenido
    # en el punto 1 y actualizar la base de datos
    estudiante_act.tutor = tutor_act

    # Aunque la persona ya existe, como el id coincide
    # se actualiza sin generar una nueva entrada en la DB
    session.add(estudiante_act)
    session.commit()

    print("Estudiante actualizado Id:", id)
    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # la función update_persona_nationality



def count_grade(grade):
    print('Estudiante por grado')
    # Utilizar la sentencia COUNT para contar cuantos estudiante
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado

    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(Estudiante).filter(Estudiante.grade == grade).count()
    print("Estudiantes en grado:", grade, "encontrados:", result)
    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función count_persona

def insert_estudiante(name, age, grade, tutor_id):
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear un nuevo estudiante
    nuevo_estudiante = Estudiante(name=name, age=age, grade=grade, tutor_id=tutor_id)
   
    # Agregar el nuevo estudiante a la DB
    session.add(nuevo_estudiante)
    session.commit()

def insert_tutor(name):
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear un nuevo tutor
    nuevo_tutor = Tutor(name=name)

    # Agregar el nuevo tutor a la DB
    session.add(nuevo_tutor)
    session.commit()


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")

    create_schema()   # create and reset database (DB)
    fill()
    fetch()
    

    tutor = 'Daniel'
    search_by_tutor(tutor)

    nuevo_tutor = 'Oscar'
    id = 2
    modify(id, nuevo_tutor)

    grade = 2
    count_grade(grade)


    