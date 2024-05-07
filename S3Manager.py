import boto3
import pymysql
from datetime import datetime

def get_secret():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    secret_value = client.get_secret_value(SecretId='my-db-credentials')
    return eval(secret_value['SecretString'])

def save_to_database(db_params, data):
    connection = pymysql.connect(host=db_params['host'],
                                 user=db_params['username'],
                                 password=db_params['password'],
                                 database=db_params['dbname'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `reports` (`report_date`, `data`) VALUES (%s, %s)"
            cursor.execute(sql, (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), data))
        connection.commit()

def save_report_to_s3(data, bucket, report_name):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=report_name, Body=data)

def get_last_file_name(bucket):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket)
    files = [obj['Key'] for obj in response['Contents']]
    return files[-1] if files else None

def rename_file_in_s3(bucket, old_name, new_name):
    s3 = boto3.client('s3')
    s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': old_name}, Key=new_name)
    s3.delete_object(Bucket=bucket, Key=old_name)

def query_database(db_params, query):
    connection = pymysql.connect(host=db_params['host'],
                                 user=db_params['username'],
                                 password=db_params['password'],
                                 database=db_params['dbname'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    return result
