from src.app.notas_process import notasProcess
from flask_restful import Resource


class listenerLogin(Resource):

    def get(self, rut, password, periodo):
        data = notasProcess(
            rut,
            password
        ).get_data(periodo)

        return data