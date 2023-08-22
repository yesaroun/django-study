from rest_framework.test import APITestCase

from rooms import models


class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Des"
    URL = "api/v1/rooms/amenities/"

    def setUp(self) -> None:
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenites(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    def test_create_amenity(self):
        new_amnity_name = "New Amenity"
        new_amnity_description = "New Amenity desc."

        response = self.client.post(
            self.URL,
            data={
                "name": new_amnity_name,
                "description": new_amnity_description,
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            data["name"],
            new_amnity_name,
        )
        self.assertEqual(
            data["description"],
            new_amnity_description,
        )

        response = self.client.post(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)
