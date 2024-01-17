# Установка Flake8 (если не установлен)
# pip install flake8

import subprocess


def test_pep8_compliance():
    """
    Тестирование соблюдения стандарта PEP 8 с использованием Flake8.
    """
    try:
        # Запуск Flake8 для текущего рабочего каталога
        result = subprocess.run(
            ["flake8"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Проверка кода завершения
        if result.returncode == 0:
            print("Код соответствует PEP 8.")
        else:
            # Вывод ошибок, если они есть
            print("Нарушения PEP 8 обнаружены:")
            print(result.stdout)

    except FileNotFoundError:
        print("Flake8 не установлен. Установите, используя 'pip install flake8'.")


if __name__ == "__main__":
    test_pep8_compliance()
