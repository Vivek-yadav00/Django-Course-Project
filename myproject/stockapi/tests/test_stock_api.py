import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from stockapi.models import Stock

@pytest.fixture
@pytest.mark.django_db
def api_client():
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def sample():
    return Stock.objects.create(ticker='test',company_name='Test Stock',price=100)


# API Mocking
@pytest.mark.django_db
def test_stock_list(api_client, sample):
    response = api_client.get(reverse('stock-list'))
    assert response.status_code == 200
    data = response.json()
    assert data["results"][0]["company_name"] == "Test Stock"


@pytest.mark.django_db
def test_create_stock(api_client):
    data={
        "ticker":"test",
        "company_name":"New Stock",
        "price":100
    }
    response=api_client.post(reverse("stock-create"),data,format="json")
    assert response.status_code ==  200
    assert response.json()["ticker"]=="test"


@pytest.mark.django_db
def test_get_stock(api_client,sample):
    response=api_client.get(reverse("stock-detail",args=[sample.id]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_stock_404(api_client):
    response=api_client.get(reverse("stock-detail",args=[100]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete(api_client,sample):
    response=api_client.delete(reverse("stock-delete",args=[sample.id]))
    assert response.status_code == 200
    assert not Stock.objects.filter(id=sample.id).exists()