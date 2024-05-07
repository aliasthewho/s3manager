import unittest
from moto import mock_s3
import boto3
import pymysql
from my_script import save_to_database, save_report_to_s3, get_last_file_name, rename_file_in_s3, query_database

class TestAWSServicesIntegration(unittest.TestCase):

    @mock_s3
    def setUp(self):
        self.bucket_name = "test-bucket"
        self.s3_client = boto3.client("s3", region_name="us-east-1")
        self.s3_client.create_bucket(Bucket=self.bucket_name)

    @mock_s3
    def test_save_report_to_s3_integration(self):
        save_report_to_s3("test data", self.bucket_name, "report.txt")
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key="report.txt")
        self.assertEqual(response['Body'].read().decode(), "test data")

    @mock_s3
    def test_get_last_file_name_integration(self):
        self.s3_client.put_object(Bucket=self.bucket_name, Key="file1.txt", Body="test data")
        self.s3_client.put_object(Bucket=self.bucket_name, Key="file2.txt", Body="test data")
        self.s3_client.put_object(Bucket=self.bucket_name, Key="file3.txt", Body="test data")
        last_file = get_last_file_name(self.bucket_name)
        self.assertEqual(last_file, "file3.txt")

    @mock_s3
    def test_rename_file_in_s3_integration(self):
        self.s3_client.put_object(Bucket=self.bucket_name, Key="old.txt", Body="test data")
        rename_file_in_s3(self.bucket_name, "old.txt", "new.txt")
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key="new.txt")
        self.assertEqual(response['Body'].read().decode(), "test data")
        with self.assertRaises(self.s3_client.exceptions.NoSuchKey):
            self.s3_client.get_object(Bucket=self.bucket_name, Key="old.txt")

    def test_save_to_database_integration(self):
        # Configura la base de datos MySQL en un entorno local o remoto
        db_params = {'host': 'localhost', 'username': 'root', 'password': 'root', 'dbname': 'testdb'}
        connection = pymysql.connect(host=db_params['host'],
                                     user=db_params['username'],
                                     password=db_params['password'],
                                     database=db_params['dbname'],
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                cursor.execute("CREATE TABLE IF NOT EXISTS `reports` (`id` int AUTO_INCREMENT PRIMARY KEY, `report_date` datetime, `data` text)")

        save_to_database(db_params, "test data")
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM `reports`")
                result = cursor.fetchall()
                self.assertGreater(len(result), 0)

    def test_query_database_integration(self):
        db_params = {'host': 'localhost', 'username': 'root', 'password': 'root', 'dbname': 'testdb'}
        result = query_database(db_params, "SELECT * FROM `reports`")
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()
