from rocksdict import Rdict

def delete_db():
    Rdict.destroy('../db_path')