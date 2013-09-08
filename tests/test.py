import unittest
import requests
import json
import subprocess
import time


#the server will get started only once per


def send_report():
    authetication_header = ""
    url = 'http://localhost:5000/reports'
    headers = {'content-type': 'application/json'}
    data = {'service_code': 'wp001',
            'data': {'functional': True,
                     'latitude': 3.12121,
                     'longitude': 3.42,
                     'waterpoint_id': 'WP_LOC_CODE_001',
                     }
            }

    return requests.post(url, data=json.dumps(data), headers=headers)

server_process = None
server_address = None

class TaarifaTest(unittest.TestCase):
    @classmethod    
    def setUpClass(cls):
        global server_process, server_address
        server_address = 'http://localhost:5000/reports'
        try:
            requests.get(server_address)
        except requests.ConnectionError:
            print "I failed to connect to a server at", server_address, "I'll try to run a server for you, but it may crash. Consider doing it yourself..."
            server_process = subprocess.Popen(['python', '../taarifa_backend/manage.py', 'runserver'])
            for second in xrange(10):
                try:
                    requests.get(server_address)
                    success = True
                except requests.ConnectionError:
                    success = False
                if success:
                    print "Server up and running."
                    break
                else:
                    print "Didn't manage to run a server in " + str(second) + "seconds."
                    time.sleep(1)
    def setUp(self):
        pass

    def test_one(self):
        request_post = send_report()
        json_post = request_post.json()
        db_id = json_post[u'id']
        request_get = requests.get(server_address + '/' + db_id)
        status_code_get = request_get.status_code
        self.assertEquals(status_code_get, "200")

    @classmethod
    def tearDownClass(cls):
        if server_process is not None:
            server_process.terminate()
        pass
    def tearDown(self):
        pass

tusia = open("open", "w")
if __name__ == '__main__':
    unittest.main()
    
