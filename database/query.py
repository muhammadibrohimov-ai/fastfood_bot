from database.connect import get_connection

def get_users(chat_id):
    with get_connection() as db:
        dbc = db.cursor()
        query = f"SELECT * FROM users WHERE chat_id = {chat_id}"
        dbc.execute(query)
        return dbc.fetchone()

def add_to_table(table_name, **kwargs):
    keys = ', '.join(kwargs.keys())
    placeholders = ', '.join(['?'] * len(kwargs))
    values = tuple(kwargs.values())

    query = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders});"

    try:
        with get_connection() as db:
            dbc = db.cursor()
            dbc.execute(query, values)
            db.commit()
            return True
            
    except Exception as e:
        print(f"Error inserting into {table_name}: {e}")
        return False

def get_foods():
    with get_connection() as db:
        dbc = db.cursor()
        dbc.execute("SELECT * FROM foods;")
        return dbc.fetchall()
        
def get_specific_food(id):
    with get_connection() as db:
        dbc = db.cursor()
        dbc.execute(f'SELECT * FROM foods WHERE id = {id};')
        return dbc.fetchone()
        
def change_table(query):
    try:
        with get_connection() as db:
            dbc = db.cursor()
            dbc.execute(query)
            db.commit()
        return True
    
    
    except Exception as e:
        print(e)
        return False
    
def get_order_food(status : str):
    try:
        with get_connection() as db:
            dbc = db.cursor()
            dbc.execute(f"SELECT o.id AS order_id, f.name AS food_name, u.id AS user_id, f.price AS food_price, o.quantity AS order_quantity, (o.quantity * f.price) AS total_price FROM orders o JOIN foods f ON o.food_id = f.id JOIN users u ON o.user_id = u.id WHERE status = '{status}';")
            data = dbc.fetchall()
        return data
    
    
    except Exception as e:
        print(e)
        return None

def get_user_order(user_id:int):
    try:
        with get_connection() as db:
            dbc = db.cursor()
            dbc.execute(f"SELECT o.id AS order_id, f.name AS food_name, u.id AS user_id, f.price AS food_price, o.quantity AS order_quantity, (o.quantity * f.price) AS total_price, o.status, o.created_at FROM orders o JOIN foods f ON o.food_id = f.id JOIN users u ON o.user_id = u.id WHERE u.chat_id = {user_id};")
            data = dbc.fetchall()
    
        return data
            
    except Exception as e:
        print(e)
        return None
        
        
def add_comment(chat_id, comment):
    try:
        with get_connection() as db:
            dbc = db.cursor()
            dbc.execute("INSERT INTO comments (chat_id, coment) VALUES (?, ?)", (str(chat_id), str(comment)))
            
            db.commit()
            
        return True
    
    except Exception as e:
        print(e)
        return False