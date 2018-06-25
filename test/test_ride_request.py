import unittest
import os
import json
from models import ride_models
from Api import create_app

class TestRideRequest(unittest.TestCase):
    def setUp(self):
        """initialize app and define variables"""
        self.app = create_app(config_name="testing")
        self.app.config["TESTING"]=True
        self.client = self.app.test_client()

    def test_post_ride_request(self):
        """test usesr can create ride request """
        response = self.client.post(
            "api/v1/user/request",
            data=json.dumps(dict
                    (location="Nairobi",
                    destination="Kisumu"
                    )),
                    content_type = "application/json"
                    )
        self.assertEqual(response.status_code,201)
    
    def test_location_not_empty(self):
        """Test field not empty"""
        response = self.client.post(
            "api/v1/user/request",
            data=json.dumps(dict
                    (location="",
                    destination="Kisumu"
                    )),
                    content_type = "application/json"
                    )
        self.assertEqual(response.status_code,400)
        # self.assertEqual()
        pass

    def test_request_no_space(self):
        """test user enters no spaces"""
        response = self.client.post(
            "api/v1/user/request",
            data=json.dumps(dict
                    (location="Nairobi",
                    destination="Kisumu"
                    )),
                    content_type = "application/json"
                    )
        self.assertEqual(response.status_code,201)
        pass

    def tearDown(self):
        pass