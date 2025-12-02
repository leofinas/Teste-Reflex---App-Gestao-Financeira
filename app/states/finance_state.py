import reflex as rx
import logging
from typing import TypedDict
from app.database import get_user_collection
from app.encryption import encrypt_value, decrypt_value, is_using_temp_key

CATEGORY_DEFINITIONS = {
    "Moradia": {
        "icon": "home",
        "hex": "#3b82f6",
        "color_cls": "bg-blue-100 text-blue-700 border-blue-200",
    },
    "Transporte": {
        "icon": "car",
        "hex": "#6366f1",
        "color_cls": "bg-indigo-100 text-indigo-700 border-indigo-200",
    },
    "Alimentação": {
        "icon": "utensils",
        "hex": "#22c55e",
        "color_cls": "bg-green-100 text-green-700 border-green-200",
    },
    "Saúde": {
        "icon": "heart-pulse",
        "hex": "#ef4444",
        "color_cls": "bg-red-100 text-red-700 border-red-200",
    },
    "Educação": {
        "icon": "graduation-cap",
        "hex": "#eab308",
        "color_cls": "bg-yellow-100 text-yellow-700 border-yellow-200",
    },
    "Lazer": {
        "icon": "gamepad-2",
        "hex": "#a855f7",
        "color_cls": "bg-purple-100 text-purple-700 border-purple-200",
    },
    "Comunicação": {
        "icon": "radio",
        "hex": "#00ff04",
        "color_cls": "bg-lime-100 text-lime-700 border-lime-200",
    },
    "Despesas pessoais": {
        "icon": "user",
        "hex": "#ec4899",
        "color_cls": "bg-pink-100 text-pink-700 border-pink-200",
    },
    "Outros": {
        "icon": "circle-help",
        "hex": "#6b7280",
        "color_cls": "bg-gray-100 text-gray-700 border-gray-200",
    },
}
CATEGORIES = list(CATEGORY_DEFINITIONS.keys())


class IncomeItem(TypedDict):
    name: str
    amount: float


class ExpenseItem(TypedDict):
    name: str
    amount: float
    category: str


class InstallmentItem(TypedDict):
    name: str
    total_amount: float
    installments_count: int
    installment_value: float
    category: str


class FinanceState(rx.State):
    monthly_income: list[IncomeItem] = []
    monthly_expenses: list[ExpenseItem] = []
    annual_expenses: list[ExpenseItem] = []
    installments: list[InstallmentItem] = []

    @rx.var
    def total_monthly_income(self) -> float:
        return sum((item["amount"] for item in self.monthly_income))

    @rx.var
    def total_monthly_expenses(self) -> float:
        return sum((item["amount"] for item in self.monthly_expenses))

    @rx.var
    def total_annual_expenses_monthly(self) -> float:
        return sum((item["amount"] for item in self.annual_expenses)) / 12

    @rx.var
    def total_installments_monthly(self) -> float:
        return sum((item["installment_value"] for item in self.installments))

    @rx.var
    def total_monthly_spending(self) -> float:
        return (
            self.total_monthly_expenses
            + self.total_annual_expenses_monthly
            + self.total_installments_monthly
        )

    @rx.var
    def monthly_balance(self) -> float:
        return self.total_monthly_income - self.total_monthly_spending

    @rx.var
    def pie_chart_data(self) -> list[dict[str, str | float]]:
        data = {cat: 0.0 for cat in CATEGORIES}
        for item in self.monthly_expenses:
            cat = item.get("category", "Outros")
            if cat in data:
                data[cat] += item["amount"]
            else:
                data.setdefault("Outros", 0.0)
                data["Outros"] += item["amount"]
        for item in self.annual_expenses:
            cat = item.get("category", "Outros")
            val = item["amount"] / 12
            if cat in data:
                data[cat] += val
            else:
                data.setdefault("Outros", 0.0)
                data["Outros"] += val
        for item in self.installments:
            cat = item.get("category", "Outros")
            val = item["installment_value"]
            if cat in data:
                data[cat] += val
            else:
                data.setdefault("Outros", 0.0)
                data["Outros"] += val
        total = sum(data.values())
        result = []
        for cat, value in data.items():
            if value > 0:
                pct = value / total * 100 if total > 0 else 0.0
                val_str = (
                    f"{value:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
                pct_str = f"{pct:.1f}".replace(".", ",")
                result.append(
                    {
                        "name": cat,
                        "value": round(value, 2),
                        "value_str": f"R$ {val_str}",
                        "pct_str": f"({pct_str}%)",
                        "fill": CATEGORY_DEFINITIONS.get(
                            cat, CATEGORY_DEFINITIONS["Outros"]
                        )["hex"],
                    }
                )
        return sorted(result, key=lambda x: x["value"], reverse=True)

    hide_values: bool = True
    is_editing: bool = False
    editing_item_type: str = ""
    editing_item_index: int = -1
    editing_item_data: dict = {}

    @rx.event
    def toggle_privacy(self):
        self.hide_values = not self.hide_values

    @rx.event
    def start_edit_income(self, index: int):
        self.editing_item_type = "income"
        self.editing_item_index = index
        self.editing_item_data = self.monthly_income[index]
        self.is_editing = True

    @rx.event
    def start_edit_monthly_expense(self, index: int):
        self.editing_item_type = "monthly_expense"
        self.editing_item_index = index
        self.editing_item_data = self.monthly_expenses[index]
        self.is_editing = True

    @rx.event
    def start_edit_annual_expense(self, index: int):
        self.editing_item_type = "annual_expense"
        self.editing_item_index = index
        self.editing_item_data = self.annual_expenses[index]
        self.is_editing = True

    @rx.event
    def start_edit_installment(self, index: int):
        self.editing_item_type = "installment"
        self.editing_item_index = index
        self.editing_item_data = self.installments[index]
        self.is_editing = True

    @rx.event
    def cancel_edit(self):
        self.is_editing = False
        self.editing_item_data = {}
        self.editing_item_index = -1
        self.editing_item_type = ""

    @rx.event
    async def save_edit(self, form_data: dict):
        if self.editing_item_index == -1:
            return
        try:
            if self.editing_item_type == "income":
                name = form_data.get("name", "")
                amount = float(form_data.get("amount", "0"))
                if 0 <= self.editing_item_index < len(self.monthly_income):
                    self.monthly_income[self.editing_item_index] = {
                        "name": name,
                        "amount": amount,
                    }
            elif self.editing_item_type == "monthly_expense":
                name = form_data.get("name", "")
                amount = float(form_data.get("amount", "0"))
                category = form_data.get("category", "Outros")
                if 0 <= self.editing_item_index < len(self.monthly_expenses):
                    self.monthly_expenses[self.editing_item_index] = {
                        "name": name,
                        "amount": amount,
                        "category": category,
                    }
            elif self.editing_item_type == "annual_expense":
                name = form_data.get("name", "")
                amount = float(form_data.get("amount", "0"))
                category = form_data.get("category", "Outros")
                if 0 <= self.editing_item_index < len(self.annual_expenses):
                    self.annual_expenses[self.editing_item_index] = {
                        "name": name,
                        "amount": amount,
                        "category": category,
                    }
            elif self.editing_item_type == "installment":
                name = form_data.get("name", "")
                total_amount = float(form_data.get("total_amount", "0"))
                count = int(form_data.get("count", "1"))
                category = form_data.get("category", "Outros")
                installment_value = total_amount / count if count > 0 else 0
                if 0 <= self.editing_item_index < len(self.installments):
                    self.installments[self.editing_item_index] = {
                        "name": name,
                        "total_amount": total_amount,
                        "installments_count": count,
                        "installment_value": installment_value,
                        "category": category,
                    }
            await self._save_data()
            self.is_editing = False
            return rx.toast("Item atualizado com sucesso!")
        except ValueError as e:
            logging.exception(f"Error parsing values during edit: {e}")
            return rx.toast("Erro ao salvar: verifique os valores numéricos.")
        except Exception as e:
            logging.exception(f"Error saving edit: {e}")
            return rx.toast("Erro ao salvar edição.")

    async def _save_data(self):
        """Internal helper to save state to MongoDB with encryption."""
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        if not auth_state.token_is_valid:
            return
        email = auth_state.tokeninfo.get("email")
        if not email:
            return
        collection = get_user_collection()
        if collection is not None:
            try:
                encrypted_income = [
                    {"name": item["name"], "amount": encrypt_value(item["amount"])}
                    for item in self.monthly_income
                ]
                encrypted_monthly_expenses = [
                    {
                        "name": item["name"],
                        "amount": encrypt_value(item["amount"]),
                        "category": item.get("category", "Outros"),
                    }
                    for item in self.monthly_expenses
                ]
                encrypted_annual_expenses = [
                    {
                        "name": item["name"],
                        "amount": encrypt_value(item["amount"]),
                        "category": item.get("category", "Outros"),
                    }
                    for item in self.annual_expenses
                ]
                encrypted_installments = [
                    {
                        "name": item["name"],
                        "total_amount": encrypt_value(item["total_amount"]),
                        "installments_count": item["installments_count"],
                        "installment_value": encrypt_value(item["installment_value"]),
                        "category": item.get("category", "Outros"),
                    }
                    for item in self.installments
                ]
                data = {
                    "user_email": email,
                    "monthly_income": encrypted_income,
                    "monthly_expenses": encrypted_monthly_expenses,
                    "annual_expenses": encrypted_annual_expenses,
                    "installments": encrypted_installments,
                }
                collection.replace_one({"user_email": email}, data, upsert=True)
            except Exception as e:
                logging.exception(f"Error saving data to MongoDB: {e}")
                return rx.toast("Aviso: Não foi possível salvar online.")

    @rx.event
    async def load_data(self):
        """Load and decrypt data from MongoDB if available."""
        from app.states.auth_state import AuthState

        self.monthly_income = []
        self.monthly_expenses = []
        self.annual_expenses = []
        self.installments = []
        auth_state = await self.get_state(AuthState)
        if not auth_state.token_is_valid:
            return
        email = auth_state.tokeninfo.get("email")
        if not email:
            return
        collection = get_user_collection()
        if collection is not None:
            try:
                doc = collection.find_one({"user_email": email})
                if doc:
                    raw_income = doc.get("monthly_income") or []
                    self.monthly_income = [
                        {
                            "name": item["name"],
                            "amount": decrypt_value(item.get("amount", 0)),
                        }
                        for item in raw_income
                    ]
                    raw_monthly_expenses = doc.get("monthly_expenses") or []
                    self.monthly_expenses = [
                        {
                            "name": item["name"],
                            "amount": decrypt_value(item.get("amount", 0)),
                            "category": item.get("category", "Outros"),
                        }
                        for item in raw_monthly_expenses
                    ]
                    raw_annual_expenses = doc.get("annual_expenses") or []
                    self.annual_expenses = [
                        {
                            "name": item["name"],
                            "amount": decrypt_value(item.get("amount", 0)),
                            "category": item.get("category", "Outros"),
                        }
                        for item in raw_annual_expenses
                    ]
                    raw_installments = doc.get("installments") or []
                    self.installments = [
                        {
                            "name": item["name"],
                            "total_amount": decrypt_value(item.get("total_amount", 0)),
                            "installments_count": int(
                                item.get("installments_count", 1)
                            ),
                            "installment_value": decrypt_value(
                                item.get("installment_value", 0)
                            ),
                            "category": item.get("category", "Outros"),
                        }
                        for item in raw_installments
                    ]
                    logging.info(
                        f"Loaded data for {email}: {len(self.monthly_income)} income items"
                    )
                else:
                    logging.info(f"No existing data found for {email}, starting fresh.")
            except Exception as e:
                logging.exception(f"Error loading data from MongoDB: {e}")
                return rx.toast("Erro ao carregar dados online.")
            if is_using_temp_key():
                return rx.toast(
                    "⚠️ Chave de criptografia temporária em uso. Dados não persistirão após reinício.",
                    duration=6000,
                )

    @rx.event
    async def add_income(self, form_data: dict):
        name = form_data.get("name", "")
        amount_str = form_data.get("amount", "0")
        if not name or not amount_str:
            return rx.toast("Preencha todos os campos.")
        try:
            amount = float(amount_str)
        except ValueError as e:
            logging.exception(f"Error parsing income amount: {e}")
            return rx.toast("Valor inválido.")
        self.monthly_income.append({"name": name, "amount": amount})
        await self._save_data()
        return rx.toast("Renda adicionada e salva!")

    @rx.event
    async def remove_income(self, index: int):
        if 0 <= index < len(self.monthly_income):
            self.monthly_income.pop(index)
            await self._save_data()
            return rx.toast("Renda removida.")

    @rx.event
    async def add_monthly_expense(self, form_data: dict):
        name = form_data.get("name", "")
        amount_str = form_data.get("amount", "0")
        category = form_data.get("category")
        if category not in CATEGORIES:
            category = "Outros"
        if not name or not amount_str:
            return rx.toast("Preencha todos os campos.")
        try:
            amount = float(amount_str)
        except ValueError as e:
            logging.exception(f"Error parsing monthly expense amount: {e}")
            return rx.toast("Valor inválido.")
        self.monthly_expenses.append(
            {"name": name, "amount": amount, "category": category}
        )
        await self._save_data()
        return rx.toast("Despesa mensal adicionada!")

    @rx.event
    async def remove_monthly_expense(self, index: int):
        if 0 <= index < len(self.monthly_expenses):
            self.monthly_expenses.pop(index)
            await self._save_data()
            return rx.toast("Despesa removida.")

    @rx.event
    async def add_annual_expense(self, form_data: dict):
        name = form_data.get("name", "")
        amount_str = form_data.get("amount", "0")
        category = form_data.get("category")
        if category not in CATEGORIES:
            category = "Outros"
        if not name or not amount_str:
            return rx.toast("Preencha todos os campos.")
        try:
            amount = float(amount_str)
        except ValueError as e:
            logging.exception(f"Error parsing annual expense amount: {e}")
            return rx.toast("Valor inválido.")
        self.annual_expenses.append(
            {"name": name, "amount": amount, "category": category}
        )
        await self._save_data()
        return rx.toast("Despesa anual adicionada!")

    @rx.event
    async def remove_annual_expense(self, index: int):
        if 0 <= index < len(self.annual_expenses):
            self.annual_expenses.pop(index)
            await self._save_data()
            return rx.toast("Despesa anual removida.")

    @rx.event
    async def add_installment(self, form_data: dict):
        name = form_data.get("name", "")
        total_amount_str = form_data.get("total_amount", "0")
        count_str = form_data.get("count", "1")
        category = form_data.get("category")
        if category not in CATEGORIES:
            category = "Outros"
        if not name or not total_amount_str or (not count_str):
            return rx.toast("Preencha todos os campos.")
        try:
            total_amount = float(total_amount_str)
            count = int(count_str)
            if count <= 0:
                count = 1
        except ValueError as e:
            logging.exception(f"Error parsing installment values: {e}")
            return rx.toast("Valores inválidos.")
        installment_value = total_amount / count
        self.installments.append(
            {
                "name": name,
                "total_amount": total_amount,
                "installments_count": count,
                "installment_value": installment_value,
                "category": category,
            }
        )
        await self._save_data()
        return rx.toast("Parcelamento adicionado!")

    @rx.event
    async def remove_installment(self, index: int):
        if 0 <= index < len(self.installments):
            self.installments.pop(index)
            await self._save_data()
            return rx.toast("Parcelamento removido.")