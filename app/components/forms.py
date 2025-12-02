import reflex as rx
from app.states.finance_state import FinanceState, CATEGORIES


def base_input_field(
    label: str,
    name: str,
    type_: str = "text",
    placeholder: str = "",
    default_value: rx.Var | str = "",
    key: str = "",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            type=type_,
            name=name,
            placeholder=placeholder,
            default_value=default_value,
            key=key,
            step=rx.cond(type_ == "number", "0.01", None),
            required=True,
            class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all text-sm",
        ),
        class_name="mb-3",
    )


def category_select_field(default_value: rx.Var | str = "") -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Categoria *", class_name="block text-sm font-medium text-gray-700 mb-1"
        ),
        rx.el.select(
            rx.el.option(
                "Selecione uma categoria...",
                value="",
                disabled=True,
                selected=rx.cond(default_value == "", True, False),
            ),
            rx.foreach(
                CATEGORIES,
                lambda cat: rx.el.option(
                    cat, value=cat, selected=rx.cond(cat == default_value, True, False)
                ),
            ),
            name="category",
            required=True,
            class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all text-sm",
        ),
        class_name="mb-3",
    )


def submit_button(text: str) -> rx.Component:
    return rx.el.button(
        rx.icon("plus", class_name="w-4 h-4 mr-2"),
        text,
        type="submit",
        class_name="w-full flex items-center justify-center px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors font-medium text-sm mt-2 shadow-sm hover:shadow-md",
    )


def edit_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Editar Item", class_name="text-lg font-bold text-gray-900 mb-4"
                ),
                rx.el.form(
                    rx.cond(
                        FinanceState.editing_item_type == "income",
                        rx.el.div(
                            base_input_field(
                                "Fonte",
                                "name",
                                "text",
                                default_value=FinanceState.editing_item_data["name"],
                                key=f"edit_name_{FinanceState.editing_item_index}",
                            ),
                            base_input_field(
                                "Valor Mensal",
                                "amount",
                                "number",
                                default_value=FinanceState.editing_item_data["amount"],
                                key=f"edit_amount_{FinanceState.editing_item_index}",
                            ),
                        ),
                    ),
                    rx.cond(
                        (FinanceState.editing_item_type == "monthly_expense")
                        | (FinanceState.editing_item_type == "annual_expense"),
                        rx.el.div(
                            base_input_field(
                                "Nome da Despesa",
                                "name",
                                "text",
                                default_value=FinanceState.editing_item_data["name"],
                                key=f"edit_exp_name_{FinanceState.editing_item_index}",
                            ),
                            base_input_field(
                                "Valor",
                                "amount",
                                "number",
                                default_value=FinanceState.editing_item_data["amount"],
                                key=f"edit_exp_amount_{FinanceState.editing_item_index}",
                            ),
                            category_select_field(
                                default_value=FinanceState.editing_item_data["category"]
                            ),
                        ),
                    ),
                    rx.cond(
                        FinanceState.editing_item_type == "installment",
                        rx.el.div(
                            base_input_field(
                                "Item",
                                "name",
                                "text",
                                default_value=FinanceState.editing_item_data["name"],
                                key=f"edit_inst_name_{FinanceState.editing_item_index}",
                            ),
                            base_input_field(
                                "Valor Total",
                                "total_amount",
                                "number",
                                default_value=FinanceState.editing_item_data[
                                    "total_amount"
                                ],
                                key=f"edit_inst_total_{FinanceState.editing_item_index}",
                            ),
                            base_input_field(
                                "Número de Parcelas",
                                "count",
                                "number",
                                default_value=FinanceState.editing_item_data[
                                    "installments_count"
                                ],
                                key=f"edit_inst_count_{FinanceState.editing_item_index}",
                            ),
                            category_select_field(
                                default_value=FinanceState.editing_item_data["category"]
                            ),
                        ),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            type="button",
                            on_click=FinanceState.cancel_edit,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors",
                        ),
                        rx.el.button(
                            "Salvar",
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-violet-600 rounded-lg hover:bg-violet-700 transition-colors",
                        ),
                        class_name="flex justify-end gap-3 mt-6",
                    ),
                    on_submit=FinanceState.save_edit,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-6 w-full max-w-md z-50",
            ),
        ),
        open=FinanceState.is_editing,
        on_open_change=FinanceState.cancel_edit,
    )


def income_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Adicionar Renda",
            class_name="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2",
        ),
        rx.el.form(
            base_input_field("Fonte", "name", "text", "ex: Salário"),
            base_input_field("Valor Mensal", "amount", "number", "0.00"),
            submit_button("Adicionar"),
            on_submit=FinanceState.add_income,
            reset_on_submit=True,
            class_name="bg-white p-5 rounded-xl shadow-sm border border-gray-100",
        ),
    )


def monthly_expense_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Adicionar Despesa Mensal",
            class_name="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2",
        ),
        rx.el.form(
            base_input_field("Nome da Despesa", "name", "text", "ex: Aluguel"),
            base_input_field("Valor", "amount", "number", "0.00"),
            category_select_field(),
            submit_button("Adicionar"),
            on_submit=FinanceState.add_monthly_expense,
            reset_on_submit=True,
            class_name="bg-white p-5 rounded-xl shadow-sm border border-gray-100",
        ),
    )


def annual_expense_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Adicionar Despesa Anual",
            class_name="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2",
        ),
        rx.el.form(
            base_input_field("Nome da Despesa", "name", "text", "ex: IPVA"),
            base_input_field("Valor", "amount", "number", "0.00"),
            category_select_field(),
            submit_button("Adicionar"),
            on_submit=FinanceState.add_annual_expense,
            reset_on_submit=True,
            class_name="bg-white p-5 rounded-xl shadow-sm border border-gray-100",
        ),
    )


def installment_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Adicionar Parcelamento",
            class_name="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2",
        ),
        rx.el.form(
            base_input_field("Item", "name", "text", "ex: Notebook"),
            base_input_field("Valor Total", "total_amount", "number", "0.00"),
            base_input_field("Número de Parcelas", "count", "number", "12"),
            category_select_field(),
            submit_button("Adicionar"),
            on_submit=FinanceState.add_installment,
            reset_on_submit=True,
            class_name="bg-white p-5 rounded-xl shadow-sm border border-gray-100",
        ),
    )