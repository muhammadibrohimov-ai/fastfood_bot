from database.connect import get_connection

def get_users(chat_id):
    with get_connection() as db:
        with db.cursor() as dbc:
            query = f"SELECT * FROM users WHERE chat_id = {chat_id}"
            dbc.execute(query)
            return dbc.fetchone()

def add_to_table(table_name, **kwargs):

    print("Run:", id(kwargs), kwargs.keys())

chat_id=185, 
fullname="Muhammadjon", 
username='mlkj', 
phone='+56299', 
long='40.215', 
lat='163.254'
