import json
import os
import psycopg2

def handler(event, context):
    cursor = conectar()
    body = {
        "valorIngresos":total_ingresos(cursor, event["queryStringParameters"]["fecha_inicio"],event["queryStringParameters"]["fecha_final"]) ,
        "result":  lista_transacciones(cursor, event["queryStringParameters"]["fecha_inicio"],event["queryStringParameters"]["fecha_final"])
        
    }

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }
    

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def conectar():
    conn = psycopg2.connect(database=os.environ["RDS_DATABASE"],
                        host=os.environ["RDS_HOST"],
                        user=os.environ["RDS_USER"],
                        password=os.environ["RDS_PASSWORD"],
                        port=os.environ["RDS_PORT"])
    cursor = conn.cursor()
    return cursor

def lista_transacciones(cursor,fecha_inicio,fecha_final):

    cursor.execute("select * from pago where fechahorapago >= %s and fechahorapago<=%s",(fecha_inicio,fecha_final))

    respuesta = cursor.fetchall()

    return respuesta


def total_ingresos(cursor,fecha_inicio,fecha_final):
    cursor.execute("select sum(valorpagado) from pago where fechahorapago >= %s and fechahorapago<=%s",(fecha_inicio,fecha_final))

    respuesta = cursor.fetchone()

    return respuesta