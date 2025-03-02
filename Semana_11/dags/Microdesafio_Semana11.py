from datetime import datetime
from email import message
from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator

import smtplib

pais=['Argentina','Brasil','Colombia','Chile','Paraguay','Uruguay','Venezuela','Peru','Ecuador','Bolivia','Mexico']
acronimo= ['AR','BR','CO','CL','PY','UR','VE','PE','EC','BO','MX']
lista_fin_mundo=[2040,2080,2095,2100,2089,2093,2054,2078,2079,2083,2071]

texto=[]

for i in range(len(pais)):
    string='Pais {} ({}), Fecha fin mundo estimada: {}'.format(pais[i], acronimo[i],lista_fin_mundo[i])
    texto.append(string)

final = '\n'.join(texto)
print(final)

def enviar():
    try:
        return None
        raise Exception('Error')
        x=smtplib.SMTP('smtp.gmail.com',587)
        x.starttls()#
        # send email using password save in python variable
        x.login(Variable.get('SMTP_EMAIL_FROM'), Variable.get('SMTP_PASSWORD'))
        subject='Fechas fin del mundo'
        body_text=final
        message='Subject: {}\n\n{}'.format(subject,body_text)
        x.sendmail(Variable.get('SMTP_EMAIL_FROM'), Variable.get('SMTP_EMAIL_TO'),message)
        print('Exito')
    except Exception as exception:
        print(exception)
        print('Failure')
        raise exception
    
def enviar_fallo():
    try:
        x=smtplib.SMTP('smtp.gmail.com',587)
        x.starttls()#
        # send email using password save in python variable
        x.login(Variable.get('SMTP_EMAIL_FROM'), Variable.get('SMTP_PASSWORD'))
        subject='Fallo tu dag'
        body_text=final
        message='Fallo el dag dag_smtp_email_fin_mundo'
        x.sendmail(Variable.get('SMTP_EMAIL_FROM'), Variable.get('SMTP_EMAIL_TO'),message)
        print('Exito')
    except Exception as exception:
        print(exception)
        print('Failure')
        raise exception

default_args={
    'owner': 'Lucas T',
    'start_date': datetime(2023,7,11),
    'retries': 0,
    'catchup': False,
    'tags': ['microdesafio', 'semana 11']
}

with DAG(
    dag_id='dag_smtp_email_fin_mundo',
    default_args=default_args,
    schedule_interval='@daily') as dag:

    tarea_1=PythonOperator(
        task_id='dag_envio_fin_mundo',
        python_callable=enviar
    )

    aviso_fallo=PythonOperator(
        task_id='enviar_fallo',
        python_callable=enviar_fallo,
        trigger_rule='all_failed'
    )

    tarea_1 >> aviso_fallo
