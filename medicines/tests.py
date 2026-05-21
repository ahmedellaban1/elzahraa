from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from medicines.models import Medicine

User = get_user_model()

class MedicineSearchTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testdoctor',
            password='testpassword',
            role='doctor',
            first_name='Dr. Test',
            last_name='Doctor'
        )
        
        # Create active medicines
        self.med_active_1 = Medicine.objects.create(
            trade_name='Panadol',
            scientific_name='Paracetamol',
            concentration=500,
            concentration_unit='mg',
            is_active=True,
            created_by=self.user
        )
        self.med_active_2 = Medicine.objects.create(
            trade_name='Brufen',
            scientific_name='Ibuprofen',
            concentration=400,
            concentration_unit='mg',
            is_active=True,
            created_by=self.user
        )
        # Create inactive medicine
        self.med_inactive = Medicine.objects.create(
            trade_name='Aspirin',
            scientific_name='Acetylsalicylic acid',
            concentration=100,
            concentration_unit='mg',
            is_active=False,
            created_by=self.user
        )

    def test_search_anonymous_redirects(self):
        url = reverse('medicines:search_medicines')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # redirects to login

    def test_search_authenticated_returns_all_active_by_default(self):
        self.client.login(username='testdoctor', password='testpassword')
        url = reverse('medicines:search_medicines')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('results', data)
        # Only active medicines should be returned
        self.assertEqual(len(data['results']), 2)
        
        # Verify names contain trade name, scientific name, and concentration display
        trade_names = [res['text'] for res in data['results']]
        self.assertTrue(any('Panadol' in name for name in trade_names))
        self.assertTrue(any('Brufen' in name for name in trade_names))
        self.assertFalse(any('Aspirin' in name for name in trade_names))

    def test_search_by_query(self):
        self.client.login(username='testdoctor', password='testpassword')
        url = reverse('medicines:search_medicines')
        
        # Search by trade name
        response = self.client.get(url, {'q': 'pan'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertIn('Panadol', data['results'][0]['text'])

        # Search by scientific name
        response = self.client.get(url, {'q': 'ibu'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertIn('Brufen', data['results'][0]['text'])
