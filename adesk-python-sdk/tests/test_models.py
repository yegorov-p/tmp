import unittest
from adesk_python_sdk.adesk.models.base_model import BaseModel
from adesk_python_sdk.adesk.models.projects import Project, ProjectCategory, ProjectManager
from adesk_python_sdk.adesk.models.transactions import TransactionCategory
from adesk_python_sdk.adesk.models.custom_reports import CustomReportGroup, CustomReportEntry, CustomReportValue
from adesk_python_sdk.adesk.models.bank_accounts import BankAccount
from adesk_python_sdk.adesk.models.tags import Tag


class TestBaseModel(unittest.TestCase):
    def test_init_with_none_data(self):
        model = BaseModel(None)
        self.assertIsNotNone(model._data) # Should be initialized to {}
        self.assertEqual(model._data, {})

    def test_repr(self):
        model = BaseModel({"id": 1, "name": "Test"})
        # Basic check, __repr__ in BaseModel is simple
        self.assertIn("<BaseModel(", repr(model)) 

    def test_from_list_empty(self):
        items = BaseModel.from_list([])
        self.assertEqual(items, [])

    def test_from_list_with_data(self):
        data = [{"id": 1}, {"id": 2}]
        items = BaseModel.from_list(data)
        self.assertEqual(len(items), 2)
        self.assertIsInstance(items[0], BaseModel)
        self.assertEqual(items[0]._data.get("id"), 1)


class TestProjectModel(unittest.TestCase):
    def test_project_instantiation(self):
        data = {
            "id": 123,
            "name": "Project Alpha",
            "description": "Alpha description",
            "isArchived": False,
            "category": {"id": 1, "name": "Software"},
            "manager": {"id": 10, "name": "John Doe"}
        }
        project = Project(data)
        self.assertEqual(project.id, 123)
        self.assertEqual(project.name, "Project Alpha")
        self.assertEqual(project.description, "Alpha description")
        self.assertFalse(project.is_archived)
        
        self.assertIsInstance(project.category, ProjectCategory)
        self.assertEqual(project.category.id, 1)
        self.assertEqual(project.category.name, "Software")

        self.assertIsInstance(project.manager, ProjectManager)
        self.assertEqual(project.manager.id, 10)
        self.assertEqual(project.manager.name, "John Doe")

    def test_project_missing_optional_keys(self):
        data = {"id": 456, "name": "Project Beta"}
        project = Project(data)
        self.assertEqual(project.id, 456)
        self.assertEqual(project.name, "Project Beta")
        self.assertIsNone(project.description)
        self.assertIsNone(project.category)
        self.assertIsNone(project.manager)

    def test_project_with_none_data(self):
        project = Project(None)
        self.assertIsNone(project.id)
        self.assertIsNone(project.name)


class TestTransactionCategoryModel(unittest.TestCase):
    def test_transaction_category_instantiation(self):
        data = {
            "id": 1,
            "name": "Office Supplies",
            "type": 2, # expenses
            "kind": 1, # operational
            "isOwnerTransfer": False
        }
        category = TransactionCategory(data)
        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "Office Supplies")
        self.assertEqual(category.type, 2)
        self.assertEqual(category.kind, 1)
        self.assertFalse(category.is_owner_transfer)

    def test_transaction_category_missing_keys(self):
        data = {"id": 2, "name": "Consulting Income"}
        category = TransactionCategory(data)
        self.assertEqual(category.id, 2)
        self.assertEqual(category.name, "Consulting Income")
        self.assertIsNone(category.type)
        self.assertIsNone(category.kind)


class TestCustomReportGroupModel(unittest.TestCase):
    def test_custom_report_group_instantiation(self):
        data = {
            "id": 101,
            "name": "Marketing KPIs",
            "apiName": "marketingKPIs",
            "color": "blue",
            "reportSection": "marketing"
        }
        group = CustomReportGroup(data)
        self.assertEqual(group.id, 101)
        self.assertEqual(group.name, "Marketing KPIs")
        self.assertEqual(group.api_name, "marketingKPIs")
        self.assertEqual(group.color, "blue")
        self.assertEqual(group.report_section, "marketing")

class TestBankAccountModel(unittest.TestCase):
    def test_bank_account_instantiation(self):
        data = {
            "id": 1, "name": "Main Account", "currency": "USD", 
            "amount": "1234.56", "initialAmount": "100.00"
        }
        account = BankAccount(data)
        self.assertEqual(account.id, 1)
        self.assertEqual(account.name, "Main Account")
        self.assertEqual(account.currency, "USD")
        self.assertEqual(account.amount, 1234.56) # Check type conversion
        self.assertEqual(account.initial_amount, 100.00)

    def test_bank_account_invalid_amount(self):
        data = {"id": 2, "name": "Test Account", "amount": "not-a-number"}
        account = BankAccount(data)
        self.assertIsNone(account.amount) # Should be None due to conversion error

class TestTagModel(unittest.TestCase):
    def test_tag_instantiation(self):
        data = {"id": 5, "name": "Urgent", "color": "red"}
        tag = Tag(data)
        self.assertEqual(tag.id, 5)
        self.assertEqual(tag.name, "Urgent")
        self.assertEqual(tag.color, "red")

if __name__ == '__main__':
    unittest.main()
