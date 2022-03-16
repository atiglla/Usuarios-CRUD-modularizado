from flask_app.config.mysqlconnection import connectToMySQL
from .classrooms import Classroom
from .hobbies import Hobbie
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.classroom_id = data['classroom_id']

        classroom = Classroom.muestra_salon_2(data['classroom_id'])
        self.classroom = classroom

        self.hobbies = []

        self.password = data['password']

    @classmethod
    def muestra_usuarios(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('nuevo_esquema').query_db(query)
        users = []
        for u in results:
            usr = cls(u)
            users.append(usr)
        return users
    
    @classmethod
    def guardar(cls, formulario):
        query = "INSERT INTO users (first_name, last_name, email, classroom_id, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(classroom_id)s, %(password)s)"
        result = connectToMySQL('nuevo_esquema').query_db(query, formulario)
        return result
    

    @classmethod
    def mostrar(cls, formulario): #form= {"id": "1"}
        query = "SELECT * FROM users LEFT JOIN users_has_hobbies ON users.id = user_id LEFT JOIN hobbies ON hobbies.id = hobbie_id WHERE users.id = %(id)s"
        result = connectToMySQL('nuevo_esquema').query_db(query, formulario)
        usr = result[0]
        user = cls(usr)
        print(result)
        for h in result:
            hobbie_data = {
                "id": h['hobbies.id'],
                "name": h['name'],
                "created_at": h['hobbies.created_at'],
                "updated_at": h['hobbies.updated_at']
            }

            hobbie = Hobbie(hobbie_data)
            user.hobbies.append(hobbie)
            

        return user

    @staticmethod
    def valida_user(user): #Se ysa en var
        es_valido = True
        if len(user['first_name']) < 3:
            flash("first_name debe tener al menos 3 caracteres")
            es_valido = False
        if len(user['last_name']) < 3:
            flash("first_name debe tener de al menos 3 caracteres")
            es_valido = False
        if not EMAIL_REGEX.match(user['email']):
            flash("El correo electrónico es inválido")
            es_valido = False
        return es_valido