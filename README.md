# TDD (Test Driven Development)
> 「測試驅動開發」的開發流程，也就是「先寫測試再開發」
> 
> 此處搭配使用 pytest Module

此篇筆記內容取自英文文章[Test Driven Development with pytest](https://stackabuse.com/test-driven-development-with-pytest/)

---

- [TDD (Test Driven Development)](#tdd-test-driven-development)
  - [優點](#優點)
  - [Code Coverage(程式測試的涵蓋率)](#code-coverage程式測試的涵蓋率)
  - [Unit Test vs Integration Tests](#unit-test-vs-integration-tests)
  - [運作步驟](#運作步驟)
  - [測試指令 (可搭配VSCode套件)](#測試指令-可搭配vscode套件)
  - [實作簡易範例](#實作簡易範例)
  - [參考資料](#參考資料)

---

## 優點
* **幫助思考新功能的行為以及釐清適合的設計**
  * 藉由寫測試的輸入與輸出，預想此功能的行為與目的，以及可能面臨的情境或問題
* **增加對程式碼的信心**
  * 當測試越來越完善，後續開發新功能時，只要執行測試，便能檢查先前所有測試對應的功能是否正常運作
* **產生BUG機會低**
  * 雖不能完全消除BUG，但隨著修復BUG+新增測試，將會增加測試的守備範圍，降低產生BUG的機會
* **有時可當作文件**
  * 測試中的輸入輸出，類似於使用說明，能幫助了解如何使用該功能

---

## Code Coverage(程式測試的涵蓋率)
此處工具使用pytest-cov

涵蓋率這名詞一聽之下，感覺最好是100%，但100%並不代表沒有BUG，有可能是沒有對某特定情形執行測試，因此仍存在BUG

常見的涵蓋率指標:
* Lines of code tested
* How many defined functions are tested
* How many branches (if statements for example) are tested

過度追求Coverage，有時會有反效果。

隨著功能越來越多，許多功能之間有關聯性，因此需要增加額外的測試去檢查這些關聯性，這些額外測試可以確保品質，但卻無法提升 Code Coverage，這就可能成為盲點。

---
## Unit Test vs Integration Tests

以冰箱為例

**Unit Test** (單元測試)

Unit Test 就像做單一動作，如開門、按鈕等等，來確認特定功能是正常運行的，也就是測試`個別` module 是否照預期運作


**Integration Tests** (整合測試)

Integration Tests 就像模擬日常使用冰箱，設計一連串各種操作，開門、按鈕，轉旋鈕等等，測試多個module `整合`運行後，是否如預期結果

---

## 運作步驟

Red-Green-Refactor cycle (紅燈／綠燈／重構)循環
1. 根據功能去新增測試，此時只有測試，所以執行測試一定會失敗(紅燈)
2. 開發能通過測試的功能邏輯，先以通過測試為主，還不用優化程式碼(綠燈)
3. 重構程式碼，根據需求(效率、可讀性等等)重構程式碼，接著執行測試確保重構後的版本仍能通過測試

---

## 測試指令 (可搭配VSCode套件)

輸入指令`pytest`，便可查看測試結果
```bash
pytest
```

例如:

![image](https://github.com/wadelu23/MarkdownPicture/blob/main/pytest/pytest-result.png?raw=true)


若是使用VSCode，可安裝 [Python extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)


按照該套件說明中的`Configure tests by running the Configure Tests command` 設定

便能更清楚查看測試結果

![image](https://github.com/wadelu23/MarkdownPicture/blob/main/vscode/vscode-pytest.png?raw=true)

---

## 實作簡易範例
此處以存貨與移除存貨舉例

只列出`inventory.py`與`test_inventory.py`中`remove_stock`部分舉例，完整程式碼請查看檔案

以下pytest使用到的相關概念可搭配參考
* @pytest.fixture(測試的前置作業) - [What fixtures are](https://docs.pytest.org/en/6.2.x/fixture.html#what-fixtures-are)
* @pytest.mark.parametrize(參數化各組輸入與輸出) - [parametrizing test functions](https://docs.pytest.org/en/6.2.x/parametrize.html#pytest-mark-parametrize-parametrizing-test-functions)



1. Red
```python
# test_inventory.py


# 準備測試資料
@pytest.fixture
def ten_stock_inventory():
    """Returns an inventory with some test stock items"""
    inventory = Inventory(20)
    inventory.add_new_stock('Puma Test', 100.00, 8)
    inventory.add_new_stock('Reebok Test', 25.50, 2)
    return inventory

# 利用 parametrize 測試驗證各種情形
# 存貨為0、該品項不存在、存貨不足、正常情形
@pytest.mark.parametrize('name,quantity,exception,new_quantity,new_total', [
    ('Puma Test', 0,
        InvalidQuantityException(
            'Cannot remove a quantity of 0. Must remove at least 1 item'),
        0, 0),
    ('Not Here', 5,
        ItemNotFoundException(
            'Could not find Not Here in our stocks. Cannot remove non-existing stock'),
        0, 0),
    ('Puma Test', 25,
        InvalidQuantityException(
            'Cannot remove these 25 items. Only 8 items are in stock'),
        0, 0),
    ('Puma Test', 5, None, 3, 5)
])
def test_remove_stock(ten_stock_inventory, name, quantity, exception, new_quantity, new_total):
    try:
        ten_stock_inventory.remove_stock(name, quantity)
    except (InvalidQuantityException, NoSpaceException, ItemNotFoundException) as inst:
        assert isinstance(inst, type(exception))
        assert inst.args == exception.args
    else:
        assert ten_stock_inventory.stocks[name]['quantity'] == new_quantity
        assert ten_stock_inventory.total_items == new_total
```

2. Green
```python
# inventory.py


# 於Inventory Class中加入remove_stock，並對應各情形補充Exception以通過測試
    def remove_stock(self, name, quantity):
        if quantity <= 0:
            raise InvalidQuantityException(
                f'Cannot remove a quantity of {quantity}. Must remove at least 1 item')
        if name not in self.stocks:
            raise ItemNotFoundException(
                f'Could not find {name} in our stocks. Cannot remove non-existing stock')
        if self.stocks[name]['quantity'] - quantity <= 0:
            raise InvalidQuantityException(
                f'Cannot remove these {quantity} items. Only {self.stocks[name]["quantity"]} items are in stock')

        self.stocks[name]['quantity'] -= quantity
        self.total_items -= quantity
```

3. Refactor
   * 檢查程式碼中有無地方可再優化
   * 或是檢查有無符合團隊規範風格等

---

## 參考資料
* [Test Driven Development with pytest](https://stackabuse.com/test-driven-development-with-pytest/)
* [Full pytest documentation](https://docs.pytest.org/en/6.2.x/contents.html)
* [過高的 Test Code Coverage 將摧毀一個新專案](https://www.puritys.me/docs-blog/article-230-%E9%81%8E%E9%AB%98%E7%9A%84-Test-Code-Coverage-%E5%B0%87%E6%91%A7%E6%AF%80%E4%B8%80%E5%80%8B%E6%96%B0%E5%B0%88%E6%A1%88.html)