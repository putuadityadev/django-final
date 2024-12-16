from django.test import TestCase, Client
from django.urls import reverse
from ecommerceapp.models import Product, Contact, Orders
from django.contrib.auth.models import User

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            product_name="MacBook Pro",
            category="Laptop",
            subcategory="Apple",
            price=2000,
            desc="A high-performance laptop.",
        )

    def test_product_creation(self):
        self.assertEqual(self.product.product_name, "MacBook Pro")
        self.assertEqual(self.product.category, "Laptop")
        self.assertEqual(self.product.price, 2000)

    def test_product_string_representation(self):
        self.assertEqual(str(self.product), "MacBook Pro")


class ContactModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            phone_number="123456789",
            desc="Need help with a product.",
        )

    def test_contact_creation(self):
        self.assertEqual(self.contact.name, "John Doe")
        self.assertEqual(self.contact.email, "johndoe@example.com")
        self.assertEqual(self.contact.desc, "Need help with a product.")


class OrdersModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.order = Orders.objects.create(
            user=self.user,
            items_json="{'1': {'name': 'iPhone', 'quantity': 1}}",
            amount=1000,
            name="Jane Doe",
            email="janedoe@example.com",
        )

    def test_order_creation(self):
        self.assertEqual(self.order.amount, 1000)
        self.assertEqual(self.order.name, "Jane Doe")
        self.assertEqual(self.order.email, "janedoe@example.com")


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.product = Product.objects.create(
            product_name="iPhone",
            category="Phone",
            subcategory="Apple",
            price=1000,
            desc="A high-end smartphone.",
        )

    def test_homepage_accessible(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        response = self.client.get(reverse("product-detail", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "iPhone")

    def test_checkout_view_requires_login(self):
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_authenticated_checkout_access(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)


class FormsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_contact_form_submission(self):
        response = self.client.post(reverse("contact"), {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "desc": "I need help with my order.",
            "phone_number": "123456789",
        })
        self.assertEqual(response.status_code, 200)  # Assuming it renders a success message
        self.assertTrue(Contact.objects.filter(email="john.doe@example.com").exists())


class IntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.product = Product.objects.create(
            product_name="iPad",
            category="Tablet",
            subcategory="Apple",
            price=800,
            desc="A powerful tablet.",
        )

    def test_full_order_workflow(self):
        self.client.login(username="testuser", password="password123")

        # Add product to cart (simplified for test case)
        cart = {"1": {"name": self.product.product_name, "quantity": 1}}
        response = self.client.post(reverse("checkout"), {
            "items_json": str(cart),
            "amount": 800,
            "name": "John Doe",
            "email": "john@example.com",
            "address1": "123 Street",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001",
            "phone": "123456789",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Orders.objects.filter(email="john@example.com").exists())
