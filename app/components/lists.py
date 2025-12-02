import reflex as rx
from app.states.finance_state import (
    FinanceState,
    IncomeItem,
    ExpenseItem,
    InstallmentItem,
    CATEGORY_DEFINITIONS,
)


def delete_button(on_click: rx.event.EventType) -> rx.Component:
    return rx.el.button(
        rx.icon("trash-2", class_name="w-4 h-4 text-red-500"),
        on_click=on_click,
        class_name="p-2 hover:bg-red-50 rounded-full transition-colors",
        title="Excluir item",
    )


def edit_button(on_click: rx.event.EventType) -> rx.Component:
    return rx.el.button(
        rx.icon("pencil", class_name="w-4 h-4 text-blue-500"),
        on_click=on_click,
        class_name="p-2 hover:bg-blue-50 rounded-full transition-colors mr-1",
        title="Editar item",
    )


def category_badge(category: str) -> rx.Component:
    icon_cases = [
        (cat, details["icon"]) for cat, details in CATEGORY_DEFINITIONS.items()
    ]
    icon_name = rx.match(category, *icon_cases, CATEGORY_DEFINITIONS["Outros"]["icon"])
    cls_cases = [
        (
            cat,
            f"inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {details['color_cls']}",
        )
        for cat, details in CATEGORY_DEFINITIONS.items()
    ]
    default_cls = f"inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {CATEGORY_DEFINITIONS['Outros']['color_cls']}"
    return rx.el.span(
        rx.icon(icon_name, class_name="w-3 h-3 mr-1.5"),
        category,
        class_name=rx.match(category, *cls_cases, default_cls),
        title=category,
    )


def empty_state(text: str) -> rx.Component:
    return rx.el.div(
        rx.icon("clipboard-list", class_name="w-8 h-8 text-gray-300 mb-2"),
        rx.el.p(text, class_name="text-sm text-gray-400"),
        class_name="flex flex-col items-center justify-center py-8 text-center border-2 border-dashed border-gray-100 rounded-xl",
    )


def income_item(item: IncomeItem, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(item["name"], class_name="font-medium text-gray-800"),
            rx.el.p(
                rx.cond(FinanceState.hide_values, "R$ ****", f"R$ {item['amount']}"),
                class_name="text-sm text-green-600 font-semibold",
            ),
        ),
        rx.el.div(
            edit_button(FinanceState.start_edit_income(index)),
            delete_button(FinanceState.remove_income(index)),
            class_name="flex items-center",
        ),
        class_name="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-100 shadow-sm hover:shadow-md transition-shadow mb-2",
    )


def expense_item(
    item: ExpenseItem,
    index: int,
    on_remove: rx.event.EventType,
    on_edit: rx.event.EventType,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(item["name"], class_name="font-medium text-gray-800 mr-2"),
                category_badge(item.get("category", "Outros")),
                class_name="flex items-center mb-1",
            ),
            rx.el.p(
                rx.cond(FinanceState.hide_values, "R$ ****", f"R$ {item['amount']}"),
                class_name="text-sm text-red-600 font-semibold",
            ),
        ),
        rx.el.div(
            edit_button(on_edit),
            delete_button(on_remove),
            class_name="flex items-center",
        ),
        class_name="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-100 shadow-sm hover:shadow-md transition-shadow mb-2",
    )


def installment_item_display(item: InstallmentItem, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(item["name"], class_name="font-medium text-gray-800 mr-2"),
                category_badge(item.get("category", "Outros")),
                class_name="flex items-center mb-1",
            ),
            rx.el.div(
                rx.el.span(
                    rx.cond(
                        FinanceState.hide_values,
                        "Total: R$ ****",
                        f"Total: R$ {item['total_amount']}",
                    ),
                    class_name="text-xs text-gray-500 mr-2",
                ),
                rx.el.span(
                    f"{item['installments_count']}x",
                    class_name="text-xs bg-gray-100 px-2 py-0.5 rounded text-gray-600",
                ),
            ),
            rx.el.p(
                rx.cond(
                    FinanceState.hide_values,
                    "R$ **** /mês",
                    f"R$ {item['installment_value']:.2f}/mês",
                ),
                class_name="text-sm text-orange-600 font-semibold mt-1",
            ),
        ),
        rx.el.div(
            edit_button(FinanceState.start_edit_installment(index)),
            delete_button(FinanceState.remove_installment(index)),
            class_name="flex items-center",
        ),
        class_name="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-100 shadow-sm hover:shadow-md transition-shadow mb-2",
    )


def income_list() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Renda Mensal", class_name="text-lg font-semibold text-gray-800 mb-4"),
        rx.cond(
            FinanceState.monthly_income.length() > 0,
            rx.el.div(
                rx.foreach(
                    FinanceState.monthly_income, lambda item, i: income_item(item, i)
                ),
                class_name="space-y-2",
            ),
            empty_state("Nenhuma renda cadastrada"),
        ),
    )


def monthly_expense_list() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Despesas Fixas", class_name="text-lg font-semibold text-gray-800 mb-4"
        ),
        rx.cond(
            FinanceState.monthly_expenses.length() > 0,
            rx.el.div(
                rx.foreach(
                    FinanceState.monthly_expenses,
                    lambda item, i: expense_item(
                        item,
                        i,
                        lambda: FinanceState.remove_monthly_expense(i),
                        lambda: FinanceState.start_edit_monthly_expense(i),
                    ),
                ),
                class_name="space-y-2",
            ),
            empty_state("Nenhuma despesa cadastrada"),
        ),
    )


def annual_expense_list() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Despesas Anuais", class_name="text-lg font-semibold text-gray-800 mb-4"
        ),
        rx.cond(
            FinanceState.annual_expenses.length() > 0,
            rx.el.div(
                rx.foreach(
                    FinanceState.annual_expenses,
                    lambda item, i: expense_item(
                        item,
                        i,
                        lambda: FinanceState.remove_annual_expense(i),
                        lambda: FinanceState.start_edit_annual_expense(i),
                    ),
                ),
                class_name="space-y-2",
            ),
            empty_state("Nenhuma despesa anual cadastrada"),
        ),
    )


def installment_list() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Parcelamentos", class_name="text-lg font-semibold text-gray-800 mb-4"
        ),
        rx.cond(
            FinanceState.installments.length() > 0,
            rx.el.div(
                rx.foreach(
                    FinanceState.installments,
                    lambda item, i: installment_item_display(item, i),
                ),
                class_name="space-y-2",
            ),
            empty_state("Nenhum parcelamento cadastrado"),
        ),
    )