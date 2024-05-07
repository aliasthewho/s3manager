import unittest
from unittest.mock import patch, MagicMock
from S3Manager import get_secret#, save_to_database, save_report_to_s3, get_last_file_name, rename_file_in_s3, query_database

class TestAWSServicesUnit(unittest.TestCase):

    @patch('my_script.boto3.client')
    def test_get_secret(self, mock_boto_client):
        # Simula una respuesta del Secrets Manager
        mock_boto_client.return_value.get_secret_value.return_value = {
            'SecretString': "{'username': 'user', 'password': 'pass', 'host': 'localhost', 'dbname': 'testdb'}"
        }
        secrets = get_secret()
        self.assertEqual(secrets['username'], 'user')
        self.assertEqual(secrets['password'], 'pass')

    # @patch('my_script.pymysql.connect')
    # def test_save_to_database(self, mock_connect):
    #     mock_connection = MagicMock()
    #     mock_cursor = MagicMock()
    #     mock_connect.return_value.__enter__.return_value = mock_connection
    #     mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    #     db_params = {'host': 'localhost', 'username': 'user', 'password': 'pass', 'dbname': 'testdb'}
    #     save_to_database(db_params, "test data")

    #     mock_cursor.execute.assert_called_once_with("INSERT INTO `reports` (`report_date`, `data`) VALUES (%s, %s)", unittest.mock.ANY)
    #     mock_connection.commit.assert_called_once()

    # @patch('my_script.boto3.client')
    # def test_save_report_to_s3(self, mock_boto_client):
    #     mock_s3 = mock_boto_client.return_value
    #     save_report_to_s3("test data", "test-bucket", "report.txt")
    #     mock_s3.put_object.assert_called_once_with(Bucket="test-bucket", Key="report.txt", Body="test data")

    # @patch('my_script.boto3.client')
    # def test_get_last_file_name(self, mock_boto_client):
    #     mock_s3 = mock_boto_client.return_value
    #     mock_s3.list_objects_v2.return_value = {
    #         'Contents': [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}, {'Key': 'file3.txt'}]
    #     }
    #     last_file = get_last_file_name("test-bucket")
    #     self.assertEqual(last_file, 'file3.txt')

    # @patch('my_script.boto3.client')
    # def test_rename_file_in_s3(self, mock_boto_client):
    #     mock_s3 = mock_boto_client.return_value
    #     rename_file_in_s3("test-bucket", "old.txt", "new.txt")
    #     mock_s3.copy_object.assert_called_once_with(Bucket="test-bucket", CopySource={'Bucket': 'test-bucket', 'Key': 'old.txt'}, Key="new.txt")
    #     mock_s3.delete_object.assert_called_once_with(Bucket="test-bucket", Key="old.txt")

    # @patch('my_script.pymysql.connect')
    # def test_query_database(self, mock_connect):
    #     mock_connection = MagicMock()
    #     mock_cursor = MagicMock()
    #     mock_connect.return_value.__enter__.return_value = mock_connection
    #     mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    #     mock_cursor.fetchall.return_value = [{'id': 1, 'data': 'result'}]
    #     db_params = {'host': 'localhost', 'username': 'user', 'password': 'pass', 'dbname': 'testdb'}
    #     result = query_database(db_params, "SELECT * FROM `reports`")
    #     self.assertEqual(result, [{'id': 1, 'data': 'result'}])

if __name__ == '__main__':
    unittest.main()
