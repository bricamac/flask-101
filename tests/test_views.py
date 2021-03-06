# tests/test_views.py
from flask_testing import TestCase
from wsgi import app, init_product
import json

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        init_product()


    def test_products_json(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 2) # 2 is not a mistake here.

    def test_product_one_json(self):
        response = self.client.get("/api/v1/products/2")
        products = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(products,dict)
        self.assertDictEqual(products, {'id': 2, 'name': 'Socialive.tv'})

    def test_product_delete_json_ok(self):
        response = self.client.delete("/api/v1/products/2")
        products = response.json
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/api/v1/products")
        products = response.json
        #print (len(products))
        self.assertIsInstance(products, list)
        self.assertEqual(len(products), 2)

    def test_product_delete_json_ko(self):
        response = self.client.delete("/api/v1/products/20002")
        products = response.json
        self.assertEqual(response.status_code, 404)

    def test_product_create_ok(self):
        response=self.client.post("/api/v1/products", data=json.dumps(dict(name="cafe")),content_type='application/json')
        self.assertEqual(response.status_code, 201)
        products = response.json
        self.assertIsInstance(products,dict)
        products = response.json
        #print(products)
        nouvelleid=products["id"]
        response = self.client.get("/api/v1/products/{}".format(nouvelleid))
        products = response.json
        self.assertIsInstance(products, dict)
        self.assertDictEqual(products, {'id': nouvelleid , 'name': 'cafe'})


    def test_product_create_ko(self):
        response=self.client.post("/api/v1/products", data=json.dumps(dict(truc="cafe")),content_type='application/json')
        self.assertEqual(response.status_code, 422)

    def test_product_update_ko_notexisting(self):
        response=self.client.patch("/api/v1/products/33333", data=json.dumps(dict(name="the")),content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_product_update_ko_baddata(self):
        response=self.client.patch("/api/v1/products/2", data=json.dumps(dict(truc="the")),content_type='application/json')
        self.assertEqual(response.status_code, 422)

    def test_product_update_ko_empty(self):
        response=self.client.patch("/api/v1/products/2", data=json.dumps(dict(name="")),content_type='application/json')
        self.assertEqual(response.status_code, 422)

    def test_product_update_ok(self):

        response=self.client.patch("/api/v1/products/3", data=json.dumps(dict(name="the")),content_type='application/json')
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/api/v1/products/3")
        products = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(products, dict)
        self.assertDictEqual(products, {'id': 3 , 'name': 'the'})


