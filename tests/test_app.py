import unittest
from fastapi.testclient import TestClient
from main import app


class TestRecipes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test client for all tests"""
        cls.client = TestClient(app)

    def test_create_recipe(self):
        response = self.client.post("/api/recipes/", json={
            "title": "Паста карбонара",
            "cooking_time": 20,
            "ingredients": ["паста", "бекон", "яйца", "сыр"],
            "description": "Вкусное итальянское блюдо"
        })
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], "Паста карбонара")
        self.assertIn("id", data)

    def test_get_all_recipes(self):
        response = self.client.get("/api/recipes/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        if data:
            self.assertIn("title", data[0])
            self.assertIn("views", data[0])

    def test_create_invalid_recipe_negative_time(self):
        response = self.client.post("/api/recipes/", json={
            "title": "Блинчики",
            "cooking_time": -15,
            "ingredients": ["мука", "молоко", "яйца"],
            "description": "Сладкие блины"
        })
        self.assertEqual(response.status_code, 422)

    def test_create_invalid_recipe_empty_ingredient(self):
        response = self.client.post("/api/recipes/", json={
            "title": "Омлет",
            "cooking_time": 10,
            "ingredients": ["яйца", ""],
            "description": "Быстрый завтрак"
        })
        self.assertEqual(response.status_code, 422)

    def test_get_recipe_detail(self):
        create_response = self.client.post("/api/recipes/", json={
            "title": "Борщ",
            "cooking_time": 60,
            "ingredients": ["свекла", "капуста", "мясо", "картошка"],
            "description": "Классический украинский суп"
        })
        recipe_id = create_response.json()["id"]

        response = self.client.get(f"/api/recipes/{recipe_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Борщ")
        self.assertIn("ingredients", data)
        self.assertIn("description", data)


if __name__ == "__main__":
    unittest.main()
