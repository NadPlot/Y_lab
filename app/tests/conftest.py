import pytest


@pytest.fixture()
def new_menu():
	return {"title": "Test Menu", "description": "Test description menu"}

