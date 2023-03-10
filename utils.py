from pymongo import MongoClient


def get_db_handle(db_name, host, port, username, password):

    client = MongoClient(host=host,
                        port=int(port),
                        username=username,
                        password=password
                        )
    db_handle = client['db_name']
    return db_handle, client


client = MongoClient("mongodb+srv://tiles_admin:@cluster0.9zduqby.mongodb.net/?retryWrites=true&w=majority")
db = client['tiles']
