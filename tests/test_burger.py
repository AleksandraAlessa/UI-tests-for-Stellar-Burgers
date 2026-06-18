import pytest
from unittest.mock import Mock
from praktikum.burger import Burger


# ---------- Фикстуры с моками ----------
@pytest.fixture
def mock_bun():
    """Создаёт мок булочки с заданными значениями."""
    bun = Mock()
    bun.get_name.return_value = "black bun"
    bun.get_price.return_value = 100
    return bun


@pytest.fixture
def mock_ingredient():
    """Создаёт мок ингредиента."""
    ing = Mock()
    ing.get_name.return_value = "hot sauce"
    ing.get_price.return_value = 50
    ing.get_type.return_value = "SAUCE"
    return ing


# ---------- Тесты ----------
class TestBurger:

    def test_initialization(self):
        """Проверка инициализации бургера (булочка None, список ингредиентов пуст)."""
        burger = Burger()
        assert burger.bun is None
        assert len(burger.ingredients) == 0

    def test_set_buns(self, mock_bun):
        """Проверка установки булочки."""
        burger = Burger()
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient(self, mock_ingredient):
        """Проверка добавления одного ингредиента."""
        burger = Burger()
        burger.add_ingredient(mock_ingredient)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient

    def test_add_multiple_ingredients(self, mock_ingredient):
        """Проверка добавления нескольких ингредиентов."""
        burger = Burger()
        ing2 = Mock()
        burger.add_ingredient(mock_ingredient)
        burger.add_ingredient(ing2)
        assert len(burger.ingredients) == 2
        assert burger.ingredients[0] == mock_ingredient
        assert burger.ingredients[1] == ing2

    def test_remove_ingredient(self):
        """Проверка удаления ингредиента по индексу."""
        burger = Burger()
        ing1 = Mock()
        ing2 = Mock()
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == ing2

    def test_remove_ingredient_out_of_range(self):
        """Проверка удаления по несуществующему индексу (должен выбросить IndexError)."""
        burger = Burger()
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)

    def test_move_ingredient(self):
        """Проверка перемещения ингредиента с одного индекса на другой."""
        burger = Burger()
        ing1 = Mock()
        ing2 = Mock()
        ing3 = Mock()
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.add_ingredient(ing3)
        burger.move_ingredient(0, 2)
        assert burger.ingredients[0] == ing2
        assert burger.ingredients[1] == ing3
        assert burger.ingredients[2] == ing1

    def test_move_ingredient_same_index(self):
        """Проверка перемещения на тот же индекс (ничего не меняется)."""
        burger = Burger()
        ing1 = Mock()
        burger.add_ingredient(ing1)
        burger.move_ingredient(0, 0)
        assert burger.ingredients[0] == ing1

    def test_move_ingredient_new_index_beyond_length(self):
        """При перемещении на индекс, выходящий за пределы, элемент вставляется в конец."""
        burger = Burger()
        ing1 = Mock()
        ing2 = Mock()
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.move_ingredient(0, 5)   # new_index = 5, длина списка = 2 → вставляется в конец
        assert burger.ingredients[0] == ing2
        assert burger.ingredients[1] == ing1

    def test_move_ingredient_negative_index(self):
        """При перемещении с отрицательным индексом элемент вставляется перед указанной позицией."""
        burger = Burger()
        ing1 = Mock()
        ing2 = Mock()
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.move_ingredient(1, -1)   
        assert burger.ingredients[0] == ing2
        assert burger.ingredients[1] == ing1

    @pytest.mark.parametrize("bun_price, ingredient_prices, expected", [
        (100, [50, 60], 100*2 + 50 + 60),
        (200, [], 400),
        (150, [30, 40, 50], 150*2 + 30 + 40 + 50),
    ])
    def test_get_price(self, bun_price, ingredient_prices, expected):
        """Параметризованный тест расчёта цены бургера."""
        bun = Mock()
        bun.get_price.return_value = bun_price
        burger = Burger()
        burger.set_buns(bun)
        for price in ingredient_prices:
            ing = Mock()
            ing.get_price.return_value = price
            burger.add_ingredient(ing)
        assert burger.get_price() == expected

    def test_get_price_without_bun(self):
        """Если булочка не установлена, вызов get_price должен выбросить AttributeError."""
        burger = Burger()
        with pytest.raises(AttributeError):
            burger.get_price()

    def test_get_receipt(self, mock_bun, mock_ingredient):
        """Проверка формирования чека (строки с булочками и ингредиентами)."""
        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient)
        expected = "(==== black bun ====)\n= sauce hot sauce =\n(==== black bun ====)\n\nPrice: 250"
        assert burger.get_receipt() == expected

    def test_get_receipt_multiple_ingredients(self):
        """Проверка чека с несколькими ингредиентами."""
        bun = Mock()
        bun.get_name.return_value = "white bun"
        ing1 = Mock()
        ing1.get_type.return_value = "FILLING"
        ing1.get_name.return_value = "cutlet"
        ing2 = Mock()
        ing2.get_type.return_value = "SAUCE"
        ing2.get_name.return_value = "chili sauce"

        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)

        # Мокаем get_price, чтобы не зависеть от реальных цен
        burger.get_price = Mock(return_value=600)

        expected = (
            "(==== white bun ====)\n"
            "= filling cutlet =\n"
            "= sauce chili sauce =\n"
            "(==== white bun ====)\n\n"
            "Price: 600"
        )
        assert burger.get_receipt() == expected