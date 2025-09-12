from database.connect import get_connection

def get_users(chat_id):
    with get_connection() as db:
        with db.cursor() as dbc:
            query = f"SELECT * FROM users WHERE chat_id = {chat_id}"
            dbc.execute(query)
            return dbc.fetchone()

def add_to_table(table_name, **kwargs):
    keys = ', '.join(kwargs.keys())
    placeholders = ', '.join(['%s'] * len(kwargs))
    values = tuple(kwargs.values())

    query = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders});"

    try:
        with get_connection() as db:
            with db.cursor() as dbc:
                dbc.execute(query, values)
                return True
    except Exception as e:
        print(f"Error inserting into {table_name}: {e}")
        return False

def get_foods():
    with get_connection() as db:
        with db.cursor() as dbc:
            dbc.execute("SELECT * FROM foods;")
            return dbc.fetchall()
        
def get_specific_food(id):
    with get_connection() as db:
        with db.cursor() as dbc:
            dbc.execute(f'SELECT * FROM foods WHERE id = {id};')
            return dbc.fetchone()
        
def change_table(query):
    try:
        with get_connection() as db:
            with db.cursor() as dbc:
                dbc.execute(query)
                db.commit()
        return True
    except Exception as e:
        return e