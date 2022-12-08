from rocksdict import Rdict
import rocksDB.helper as bytes
import rocksDB.constants

DB_PATH = './db_path'

def delete_db():
    Rdict.destroy(DB_PATH)

def get_total_input_rows():
        val = Rdict(DB_PATH)[rocksDB.constants.NUM_ROWS.encode()]
        assert val is not None
        return bytes.bytes_to_int(val)