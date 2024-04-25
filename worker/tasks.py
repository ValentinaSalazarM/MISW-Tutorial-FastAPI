from celery import Celery

celery = Celery('tasks', broker = 'redis://127.0.0.1:6379/0')

@celery.task(name="tasks.registrar_log")
def registrar_log(usuario, fecha):
    with open('log_signin.txt','a') as file:
        file.write('{} - Inicio de sesión:{}\n'.format(usuario, fecha))
