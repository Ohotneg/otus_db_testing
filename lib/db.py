from datetime import datetime

def create_customer(connection, customer_data: dict) -> int:
    query = """
        INSERT INTO ps_customer (
            id_gender,
            firstname,
            lastname,
            email,
            passwd,
            date_add,
            date_upd
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    now = datetime.now()

    values = (
        customer_data.get("id_gender", 1),
        customer_data["firstname"],
        customer_data["lastname"],
        customer_data["email"],
        customer_data["passwd"],
        now,
        now,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            customer_id = cursor.lastrowid

        connection.commit()
        return customer_id
    except Exception:
        connection.rollback()
        raise

def get_customer(connection, customer_id: int):
    query = """
        SELECT id_customer, firstname, lastname, email
        FROM ps_customer
        WHERE id_customer = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (customer_id,))
        return cursor.fetchone()

def update_customer(connection, customer_id: int, customer_data: dict) -> int:
    query = """
        UPDATE ps_customer
        SET firstname = %s,
            lastname = %s,
            email = %s,
            date_upd = %s
        WHERE id_customer = %s
    """

    values = (
        customer_data["firstname"],
        customer_data["lastname"],
        customer_data["email"],
        datetime.now(),
        customer_id,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            affected_rows = cursor.rowcount

        connection.commit()
        return affected_rows
    except Exception:
        connection.rollback()
        raise

def delete_customer(connection, customer_id: int) -> int:
    query = """
        DELETE FROM ps_customer
        WHERE id_customer = %s
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (customer_id,))
            affected_rows = cursor.rowcount

        connection.commit()
        return affected_rows
    except Exception:
        connection.rollback()
        raise