from elschool import *
from data import db_session

if __name__ == '__main__':
    db_session.global_init("db/users.db")
    db_session.add_user('Lobov_Aleksej4', 'Alexey67', '6', 'aidi')
    print(db_session.get_user('aidi', '6'))

