import pytest
from app.models.other_model import OtherModel  # Замініть на реальну модель
from app.database.database import SessionLocal


@pytest.fixture
def db_session():
    """
    Фікстура для створення тестової сесії бази даних.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_other_model_data():
    """
    Фікстура для створення тестових даних для моделі.
    """
    return {
        "field1": "value1",
        "field2": "value2",
        "field3": 123,
    }


def test_create_other_model(db_session, test_other_model_data):
    """
    Тест для перевірки створення нового запису в моделі.
    """
    other_model = OtherModel(**test_other_model_data)
    db_session.add(other_model)
    db_session.commit()
    db_session.refresh(other_model)

    assert other_model.id is not None, "ID should not be None"
    assert (
        other_model.field1 == test_other_model_data["field1"]
    ), "Field1 does not match"
    assert (
        other_model.field2 == test_other_model_data["field2"]
    ), "Field2 does not match"
    assert (
        other_model.field3 == test_other_model_data["field3"]
    ), "Field3 does not match"


def test_read_other_model(db_session, test_other_model_data):
    """
    Тест для перевірки читання запису з моделі.
    """
    # Створюємо запис
    other_model = OtherModel(**test_other_model_data)
    db_session.add(other_model)
    db_session.commit()
    db_session.refresh(other_model)

    # Читаємо запис
    fetched_model = db_session.query(OtherModel).filter_by(id=other_model.id).first()
    assert fetched_model is not None, "Fetched model should not be None"
    assert fetched_model.id == other_model.id, "ID does not match"
    assert fetched_model.field1 == other_model.field1, "Field1 does not match"


def test_delete_other_model(db_session, test_other_model_data):
    """
    Тест для перевірки видалення запису з моделі.
    """
    # Створюємо запис
    other_model = OtherModel(**test_other_model_data)
    db_session.add(other_model)
    db_session.commit()
    db_session.refresh(other_model)

    # Видаляємо запис
    db_session.delete(other_model)
    db_session.commit()

    # Перевіряємо, що запис видалено
    deleted_model = db_session.query(OtherModel).filter_by(id=other_model.id).first()
    assert deleted_model is None, "Model was not deleted"
