
import unittest
from Calendar import Calendar


def hash_password(password):
    return hash(password)


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = hash_password(password)
        self.calendar = Calendar(self)
        self.identifier = '@' + str(id(self))


class TestUser(unittest.TestCase):
    def setUp(self):

        self.user = User('test_user', 'password123')

    def test_user_attributes(self):

        self.assertEqual(self.user.login, 'test_user')
        self.assertNotEqual(self.user.password, 'password123')  # Пароль должен быть захеширован
        self.assertIsInstance(self.user.calendar, Calendar)  # Пользователь должен иметь свой календарь
        self.assertTrue(self.user.identifier.startswith('@'))  # Идентификатор должен начинаться с "@"

    def test_password_hashing(self):
        # проверка хэширования пароля
        hashed_password = hash_password("password123")
        self.assertNotEqual(hashed_password, 'password123')  # Захешированный пароль не должен совпадать с исходным
        self.assertEqual(self.user.password, hashed_password)  # Проверка, что захешированный пароль совпадает


if __name__ == "__main__":
    unittest.main()
