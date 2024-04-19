import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from . import coding

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


def add_user(login: str, password: str, number: str, chatid: str):
    from . import __all_models
    c_tpl = coding.code(login, password, int(number))
    user = __all_models.User()
    user.login = c_tpl[0]
    user.password = c_tpl[1]
    user.chatid = chatid
    db_sess = create_session()
    db_sess.add(user)
    db_sess.commit()


def get_user(chatid: str, number: str) -> tuple[str, ...] | None:
    from . import __all_models
    db_sess = create_session()
    for user in db_sess.query(__all_models.User).filter(__all_models.User.chatid == chatid):
        return coding.decode(int(user.login), int(user.password), int(number))
    return None
