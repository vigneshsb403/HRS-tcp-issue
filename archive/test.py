import unittest
import requests

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:5000/'
    
    def test_content_length_and_transfer_encoding(self):
        headers = {
            'Content-Length': '4',
            'Transfer-Encoding': 'chunked'
        }
        data = 'test'

        response = requests.post(self.url, headers=headers, data=data)
        response_data = response.json()

        self.assertIn('Content-Length', response_data['headers'])
        self.assertIn('Transfer-Encoding', response_data['headers'])

        content_length = int(response_data['headers']['Content-Length'])
        transfer_encoding = response_data['headers']['Transfer-Encoding']

        print(f"Content-Length: {content_length}")
        print(f"Transfer-Encoding: {transfer_encoding}")

        # Check which one is actually used
        # If both headers are present, HTTP/1.1 servers should ignore the Content-Length header
        if 'chunked' in transfer_encoding:
            self.assertNotEqual(content_length, len(data))
        else:
            self.assertEqual(content_length, len(data))

if __name__ == '__main__':
    unittest.main()

