# bot creado por gazarrillo a base de https://blog.pythonanywhere.com/148/

from flask import Flask, request
import telepot
import urllib3
import time
import json

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "fad46b80-9bb8-4a13-be7e-5843b52c97ca"
bot = telepot.Bot('1783724025:AAFJV84tnVOiccGNBKkI2aIKFVlnV9VIV0o')
bot.setWebhook("https://gazarrillo.pythonanywhere.com/{}".format(secret), max_connections=1)

app = Flask(__name__)

faq = {
    "/start": "¡Hola! Bienvenido\nMi nombre es CEIQ-bot estoy aquí para ayudarte.\n\nPara seleccionar una opción dale click al número que aparece a la izquierda de la opción que deseas consultar.\n/1 . ¿Cuál es el Calendario Académico?\n/2 . Dudas relacionadas a Cobranzas\n/3 . Dudas relacionadas con solicitudes de documentos, cambio de carrera, graduaciones, retiros y re-inscripción de trimestre\n/4 . Dudas Relacionadas con la Inscripción\n/5 . Dudas sobre Trabajo de Grado y Proyecto de Ingeniería\n/6 . Link al “Qué de qué” de materias\n/7 . ¿Cuándo son las pruebas de ubicación de inglés?\n/8 . ¿Cuales son los pasos para solicitar una pasantía?\n/9 . ¿Cuáles son las agrupaciones y selecciones estudiantiles de la Universidad?\n/10 . ¿Cuál es el horario de transporte?\n/11 . ¿A quién acudir si presento un problema con alguna materia?\n/12 . ¿Dónde puedo conseguir el flujograma de la carrera?\n/13 . ¿Cuales son los beneficios socioeconómicos o becas que tiene la Universidad?\n/14 . Dudas sobre el Servicio Comunitario\n/15 . Quiero información sobre el seguro universitario\n/16 . Información de Contacto con la Escuela",
    "/1": "Puedes conseguir el calendario actual en el siguiente enlace:\nhttps://www.unimet.edu.ve/calendarios-academicos/",
    "/2": "Espero que las siguientes opciones respondan tu duda:\n/C1 . ¿Cuáles son los contactos de caja?\n/C2 . ¿Cuál es el costo de la matrícula?\n/C3 . ¿Cuáles son los datos para transferir?\n/C4 . ¿Cuáles son los horarios de atención de caja?\n/C5 . ¿Cuál tasa de cambio debo usar para realizar el pago de la UNIMET?\n/C6 . ¿A quién acudir si presento un problema con Cobranzas?",
    "/C1": "Puedes contactar a Cobranzas a través de su email cobranzas@unimet.edu.ve o utilizando los siguientes números de teléfono:\n0212-2403694\n0212-2403693",
    "/C2": "Puedes conseguir el cuadro con los costos por materia en el correo de “realidad financiera” o en siguiente enlace:\nhttps://drive.google.com/drive/folders/1kJtjaHW2oVYs5_ab94zlHhpsoYkSuRiC?usp=sharing",
    "/C3": "Puedes encontrar los métodos de pago en el Highlight “Info Pagos” de la cuenta de Instagram de la FCE (@fceunimet).\nEste link te llevará a ella:\n https://www.instagram.com/s/aGlnaGxpZ2h0OjE4MDY3NzcxNjAwMjA2NTcy?story_media_id=2309268406719553198&igshid=11iawo4m0qeqd",
    "/C4": "Por la situación actual, Caja varía sus horarios de atención cada semana, te recomendamos ver los correos de Cobranzas que te llegaron a tu correo unimet, ahí conseguirás esa información.\n\nSi no consigues ahí la información que deseas puedes contactar a Cobranzas a través de su email cobranzas@unimet.edu.ve o utilizando los siguientes números de teléfono:\n0212-2403694\n0212-2403693",
    "/C5": "La universidad rige el cambio de dólares a bolívares por la Tasa del Banco Central de Venezuela.\nPuedes consultarla en el siguiente enlace:\n https://www.instagram.com/bcv.org.ve/?hl=es-la",
    "/C6": "Puedes contactar a Cobranzas a través de su email cobranzas@unimet.edu.ve o utilizando los siguientes números de teléfono:\n0212-2403694\n0212-2403693",
    "/C7": "Puedes calcular el monto del mes yendo a Sirius, luego a “Procesos Administrativos” y luego seleccionas “Calculadora de Becas” o puedes acceder a ella usando el siguiente link:\nhttps://calculadora-becas.web.app\nSigues los pasos y obtendrás el monto de este mes.\nRecuerda: ese monto no incluye saldos pendientes ni morosidades que ya tengas.",
    "/3": "Espero que las siguientes opciones respondan tu duda:\n/A1 . Quiero solicitar documentos académicos y notas certificadas\n/A2 . Quiero realizar un cambio de carrera\n/A3 . Quiero empezar a hacer doble titulación\n/A4 . Quiero hacer un reingreso a la Universidad\n/A5 . Quiero retirar el trimestre\n/A6 . Quiero información sobre la solicitud de grado y graduaciones",
    "/A1": "Puedes encontrar la información sobre documentos académicos y notas certificadas en el siguiente enlace:\nhttps://www.unimet.edu.ve/infoestudiante/#tab-id-15\n\nY, también puedes conseguir los costos para los araceles vigentes aquí:\nhttps://www.unimet.edu.ve/infoestudiante/#tab-id-17",
    "/A2": "Podrás conseguir toda la información para realizar el cambio de carrera en el siguiente enlace:\nhttps://www.unimet.edu.ve/infoestudiante/#tab-id-5\n\nTambién le puedes escribir al correo electrónico de la Dirección de Asesoramiento y Desarrollo Estudiantil (DADE): \ndade@unimet.edu.ve ",
    "/A3": "Podrás conseguir toda la información para realizar una doble titulación en el siguiente enlace:\nhttps://www.unimet.edu.ve/infoestudiante/#tab-id-6\n\nTambién le puedes escribir al correo electrónico de la Dirección de Asesoramiento y Desarrollo Estudiantil (DADE): \ndade@unimet.edu.ve ",
    "/A4": "Podrás conseguir toda la información para hacer un reingreso a la Universidad en el siguiente enlace:\nhttps://www.unimet.edu.ve/dade/#tab-id-3\n\nTambién le puedes escribir al correo electrónico de la Dirección de Asesoramiento y Desarrollo Estudiantil (DADE):\ndade@unimet.edu.ve",
    "/A5": "Podrás conseguir toda la información para retirar el trimestre en el siguiente enlace:\nhttps://www.unimet.edu.ve/dade/#tab-id-4\n\nTambién le puedes escribir al correo electrónico de la Dirección de Asesoramiento y Desarrollo Estudiantil (DADE):\ndade@unimet.edu.ve ",
    "/A6": "Encontrarás toda la información sobre la solicitud de grado y graduaciones en el siguiente enlace:\nhttps://www.unimet.edu.ve/la-universidad/solicitud-de-grado/\n\n¡Felicidades Ingeniero!",
    "/4": "Espero que las siguientes opciones respondan tu duda:\n/I1 . ¿Cuál es la Oferta Académica?\n/I2 . ¿Cómo solicito un permiso especial?\n/I3 . ¿A quién acudir en caso de necesitar ayuda en el turno de inscripción?\n/I4 . ¿Cuál es el número de la Sala Situacional? (Soporte de Inscripción)\n/I5 . ¿A dónde puedo llamar para solicitar la consideración de un cupo en una materia?",
    "/I1": "Puedes conseguir la oferta anual en el siguiente enlace:\nhttps://sites.google.com/unimet.edu.ve/ingenieriaunimet/oferta-anual?authuser=0",
    "/I2": "Los permisos especiales los maneja la Directora de Escuela, la Prof. María Eugénia Álvarez.\nPuedes conseguir toda la información que necesites en el siguiente enlace:\nhttps://sites.google.com/unimet.edu.ve/ingenieriaunimet/permisos-especiales?authuser=0\n\nTambién puedes escribirle a su correo: mealvarez@unimet.edu.ve",
    "/I3": "A tu correo te llegó el instructivo de Inscripción, te recomendamos leerlo ya que ahí pudieses conseguir la respuesta al problema que estás presentando.\n\nDe todas formas, en caso de presentar un problema puedes llamar a la Sala Situacional de las Inscripciones:\n0212-2403900\n(Si llamas del exterior el número de teléfono sería +582122403900)",
    "/I4": "0212-240 3900\n(Si llamas del exterior el número de teléfono sería +582122403900)",
    "/I5": "0212-240 3900\n(Si llamas del exterior el número de teléfono sería +582122403900)",
    "/5": "Conseguirás toda la información sobre los Trabajos de Grado en el siguiente enlace:\nhttps://sites.google.com/unimet.edu.ve/ingenieriaunimet/trabajo-de-grado?authuser=0",
    "/6": "Puedes conseguir el archivo del “qué de qué” con el siguiente enlace:\nhttps://drive.google.com/drive/folders/1WNlddrzJLjP9nA7EZZ7ywyOyAPg1ur-t?usp=sharing",
    "/7": "La Prueba de Ubicación de Inglés del trimestre 2021-3 fue el 14 de Mayo, las futuras fechas serán publicadas por el Departamento de Inglés a principios del próximo trimestre.\nSi presentas un problema o quieres más información puedes escribirle a la Jefa del Departamento de Inglés, la Prof. María Ochoa (mochoa@unimet.edu.ve)",
    "/8": "Para solicitar una pasantía, primero, te recomendamos hablar con la Directora de Escuela, la Prof. María Eugenia Álvarez (mealvarez@unimet.edu.ve) y podrás conseguir toda la información en la siguiente página:\nhttps://www.unimet.edu.ve/infoestudiante/#tab-id-11",
    "/9": "La Universidad cuenta con 28 Agrupaciones activas, con 5 Selecciones Culturales y con 14 Selecciones Deportivas. ¿Cómo te puedo ayudar?\n/B1 . Información sobre las Agrupaciones Estudiantiles\n/B2 . Información sobre las Selecciones Culturales\n/B3 . Información sobre las Selecciones Deportivas",
    "/B1": "Si deseas información sobre las Agrupaciones puedes ir a este enlace:\nhttps://www.unimet.edu.ve/agrupaciones-estudiantiles/#tab-id-1",
    "/B2": "Si deseas información sobre las Selecciones Culturales puedes ir a sus instagram:\nBanda de Jazz en Concreto: @jazzenconcreto\nEnsamble de Excelencia Artística MUSICUM: @musicumunimet\nOrfeón UNIMET: @orfeonunimet\nTeatro Thespis: @teatrothespis\nMetro Danza: @metro_danza\n",
    "/B3": "Si deseas información sobre las Selecciones Deportivas puedes ir a este enlace:\nhttps://www.unimet.edu.ve/selecciones-deportivas/",
    "/10": "El horario del transporte, durante la pandemia, varía mucho dependiendo de las semanas.\nPuedes escribirle al Coronel (R) Artemio Boada para preguntarle, su correo es:\naboada@unimet.edu.ve",
    "/11": "A continuación encontrarás una lista de los departamentos de la Escuela de Ingeniería Química y la información de contacto del jefe/a correspondiente a ese departamento.\n(Nota: Si no sabes a qué departamento pertenece la materia a la cual presentas problema puedes escribirle a alguien del Centro de Estudiantes)\n\nDepartamento de Iniciativas Emprendedoras\nGilberto Márvez, jefe: gmarvez@unimet.edu.ve / 0212-240 3478\n\nDepartamento de Gerencia y Planificación\nJosé Fuenmayor, jefe: jfuenmayor@unimet.edu.ve / 0212-240 3613\n\nDepartamento de Ciencias de la Educación\nMilagros Briceño, jefa: mbriceno@unimet.edu.ve / 0212-240 3513\n\nDepartamento de Ciencias del Comportamiento\nIsamary Arenas, jefa: iarenas@unimet.edu.ve / 0212-240 3529 ó 0212-240 3530\n\nDepartamento de Desarrollo Integral\nYuherqui Guaimaro, jefa: yguaimaro@unimet.edu.ve / 0212-240 3396 ó 0212-240 3652\n\nDepartamento de Humanidades\nNapoleón Franceschi, jefe: nfranceschi@unimet.edu.ve / 0212-240 3523\n\nDepartamento de Física\nMartha Elena Galavís, jefa: mgalavis@unimet.edu.ve / 0212-240 3514 ó 240 3515\n\nDepartamento de Inglés\nMaría Natalia Ochoa, jefa: mochoa@unimet.edu.ve / 0212-240 3525 ó 0212-240 3526\n\nDepartamento de Lingüística\nVanessa Courleander, jefa: vcourleander@unimet.edu.ve / 0212-240 3527 ó 0212-240 3589\n\nDepartamento de Matemáticas\nLida Niño, jefa: lnino@unimet.edu.ve / 0212-240 3573 ó 0212-240 3574\n\nDepartamento de Química\nRosa Rodríguez, jefa: rrodriguez@unimet.edu.ve / 0212-240 3531\n\nDepartamento de la Construcción y Desarrollo Sustentable\nYazenia Frontado, jefa:  yfrontado@unimet.edu.ve / 0212-240 3287\n\nDepartamento de Energía y Automatización\nAidaelena Smith, jefa: asmith@unimet.edu.ve / 0212-240 3487 ó 0212-240 3885 ó 0212-240 3493\n\nDepartamento de Producción Industrial\nGermán Crespo, jefe: gcrespo@unimet.edu.ve / 0212-240 3550 ó 0212-240 3885\n\nDepartamento de Gestión de Proyectos y Sistemas\nDoris Baptista, jefa: dbaptista@unimet.edu.ve / 0212-240 388",
    "/12": "Puedes conseguir el flujograma de ingeniería química en el siguiente enlace:\nhttps://www.unimet.edu.ve/wp-content/uploads/2020/09/Flujograma-Ingenier%C3%ADa-Qu%C3%ADmica.pdf\n\nEl flujograma de las demás carreras lo puedes conseguir aquí: https://www.unimet.edu.ve/infoestudiante/#tab-id-",
    "/13": "Puedes conseguir información de los beneficios socioeconómicos en el siguiente enlace:\nhttps://www.unimet.edu.ve/infoestudiante/#tab-id-9\n\nTambién puedes escribir al correo de la Dirección de Apoyo SocioEconómico (DASE) a su correo electrónico:\ndase@unimet.edu.ve",
    "/14": "El servicio comunitario es uno de los requisitos para graduarte ¿Cómo te puedo ayudar?\n/S1 . ¿Dónde puedo conseguir información sobre el Servicio Comunitario?\n/S2 . ¿Cuales son los Programas de Servicio Comunitario que hay activos?\n/S3 . ¿Cuales son las asignaturas prelatorias para ver el Servicio Comunitario?",
    "/S1": "Puedes obtener información sobre los Servicios Comunitarios en el siguiente enlace:\nhttps://www.unimet.edu.ve/infoestudiante/#tab-id-12",
    "/S2": "Puedes obtener la lista de los Programas de Servicio Comunitario activos en el siguiente enlace:\nhttps://www.unimet.edu.ve/infoestudiante/#tab-id-12",
    "/S3": "Las asignaturas que prelan Servicio Comunitario son:\n\nFGEDI08 – Responsabilidad Social y Participación Cuidadana\nFGEDI09 – Liderazgo Ciudadano y Desarrollo Sostenible",
    "/15": "Puedes conseguir el tríptico donde se explican las condiciones y detalles del seguro aquí:\nhttps://www.unimet.edu.ve/dade/#tab-id-5",
    "/16": "Los contactos de mis “jefes” son:\n\nDirectora de Escuela: Prof. María Eugénia Álvarez (mealvarez@unimet.edu.ve)\nPresidente del CEIQ: Alejandro Ghysbrecht Salas (0412-9725444 / gh.alejandro@correo.unimet.edu.ve)\nConsejero de IQ: Jose Hidalgo (0414-3119649 / jose.hidalgo@correo.unimet.edu.ve)\nConsejero de IQ: Lino Marino (0424-2959485 / l.marino@correo.unimet.edu.ve)",
    "/si": "¡Me alegro! estoy a la orden para lo que necesites\nHasta luego.",
    "/no": "Lamento escuchar eso 😢. Si deseas que vuelva a mostrar el menú principal aprieta el siguiente comando:\n/start\n\nSi quieres hablar con alguien “real” (como que si fuese a hacerlo mejor que un robot 😒) aprieta el siguiente comando:\n/16",
    "/creador": "Giovanni Zarrillo",
    "/69": "Nice ;)",
    "/420": "Oye, aquí hacemos drogas pero no de esas"
    }

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        if "text" in update["message"]:
            text = update["message"]["text"]

            try:

                if text in ["/start","/2","/3","/4","/9","/14","/69","/420","/si","/no"]:
                    bot.sendMessage(chat_id, faq[text])
                elif text in ["Gracias","gracias","gracias bot","Gracias bot","gracias ceiq bot","Gracias ceiq bot","gracias ceiq-bot","Gracias ceiq-bot"]:
                    bot.sendMessage(chat_id, "¡De nada!\nSiempre para servirte.")
                else:
                    bot.sendMessage(chat_id, faq[text])
                    time.sleep(5)
                    bot.sendMessage(chat_id, "¿Esta respuesta respondió tu pregunta?\n/si\n/no")

            except Exception as e:
                bot.sendMessage(chat_id, "Error")
        else:
            bot.sendMessage(chat_id, "Error")
    return "OK"






