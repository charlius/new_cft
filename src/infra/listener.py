from src.app.horario_process import horarioProcess
from src.app.notas_process import notasProcess
from flask_restful import Resource


class listenerLogin(Resource):

    def get(self, rut, password, periodo):
        try:

            data = notasProcess(
                rut,
                password
            ).get_data(periodo)

            data["horario"] = horarioProcess(rut, password).get_data()

            return data
        except Exception as ex:
            return {
                "error": "Verifica tu contraseña o ponte en contacto con soporte"
            }, 404