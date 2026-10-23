import uuid

from lib.db import (
    create_customer,
    delete_customer,
    get_customer,
    update_customer,
)

def make_customer_data():
    unique_id = uuid.uuid4().hex[:8]

    return {
        "firstname": "Test",
        "lastname": "Customer",
        "email": f"test.{unique_id}@example.com",
        "passwd": "test-password-placeholder",
    }

def test_create_customer(connection):
    customer_data = make_customer_data()

    customer_id = create_customer(connection, customer_data)

    try:
        customer = get_customer(connection, customer_id)

        assert customer is not None
        assert customer[0] == customer_id
        assert customer[1] == customer_data["firstname"]
        assert customer[2] == customer_data["lastname"]
        assert customer[3] == customer_data["email"]
    finally:
        delete_customer(connection, customer_id)

def test_update_customer(connection):
    customer_data = make_customer_data()
    customer_id = create_customer(connection, customer_data)

    updated_data = {
        "firstname": "Updated",
        "lastname": "Customer",
        "email": f"updated.{uuid.uuid4().hex[:8]}@example.com",
    }

    try:
        affected_rows = update_customer(
            connection, customer_id, updated_data
        )

        customer = get_customer(connection, customer_id)

        assert affected_rows == 1
        assert customer[1] == updated_data["firstname"]
        assert customer[2] == updated_data["lastname"]
        assert customer[3] == updated_data["email"]
    finally:
        delete_customer(connection, customer_id)


def test_update_nonexistent_customer(connection):
    customer_id = 999999999

    affected_rows = update_customer(
        connection,
        customer_id,
        {
            "firstname": "Updated",
            "lastname": "Customer",
            "email": "updated.nonexistent@example.com",
        },
    )

    assert affected_rows == 0
    assert get_customer(connection, customer_id) is None

def test_delete_customer(connection):
    customer_data = make_customer_data()
    customer_id = create_customer(connection, customer_data)

    affected_rows = delete_customer(connection, customer_id)

    assert affected_rows == 1
    assert get_customer(connection, customer_id) is None

def test_delete_nonexistent_customer(connection):
    customer_id = 999999999

    affected_rows = delete_customer(connection, customer_id)

    assert affected_rows == 0
    assert get_customer(connection, customer_id) is None