# tests/test_views.py
from flask_testing import TestCase
from wsgi import app, init_product

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        init_product()


    def test_products_json(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        #print (len(products))
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 2) # 2 is not a mistake here.

    def test_product_delete_json_ok(self):
        response = self.client.delete("/api/v1/products/2")
        products = response.json
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/api/v1/products")
        products = response.json
        #print (len(products))
        self.assertIsInstance(products, list)
        self.assertEqual(len(products), 2)

