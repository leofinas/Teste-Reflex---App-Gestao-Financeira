import reflex as rx
from reflex_google_auth import google_oauth_provider
from app.states.auth_state import AuthState
from app.states.finance_state import FinanceState
from app.components.auth import login_page, user_header
from app.components.dashboard import dashboard_grid
from app.components.forms import (
    income_form,
    monthly_expense_form,
    annual_expense_form,
    installment_form,
    edit_modal,
)
from app.components.lists import (
    income_list,
    monthly_expense_list,
    annual_expense_list,
    installment_list,
)


def section_container(
    form_component: rx.Component,
    list_component: rx.Component,
    bg_color: str = "bg-gray-50",
) -> rx.Component:
    return rx.el.div(
        rx.el.div(form_component, class_name="w-full md:w-1/3"),
        rx.el.div(
            list_component,
            class_name="w-full md:w-2/3 bg-gray-50/50 p-4 rounded-xl border border-gray-100/50",
        ),
        class_name=f"flex flex-col md:flex-row gap-6 p-6 rounded-2xl {bg_color} border border-gray-100 shadow-sm",
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        edit_modal(),
        user_header(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("wallet", class_name="w-8 h-8 stroke-violet-600"),
                        rx.el.h1(
                            "Visão Geral", class_name="text-2xl font-bold text-gray-900"
                        ),
                        class_name="flex items-center gap-3 mb-2",
                    ),
                    rx.el.p(
                        "Gerencie seus fluxos mensais, despesas fixas e parcelamentos com facilidade.",
                        class_name="text-gray-500",
                    ),
                    class_name="mb-8",
                ),
                dashboard_grid(),
                rx.el.div(
                    section_container(income_form(), income_list(), "bg-green-50/30"),
                    section_container(
                        monthly_expense_form(), monthly_expense_list(), "bg-red-50/30"
                    ),
                    section_container(
                        annual_expense_form(), annual_expense_list(), "bg-orange-50/30"
                    ),
                    section_container(
                        installment_form(), installment_list(), "bg-blue-50/30"
                    ),
                    class_name="grid grid-cols-1 gap-8",
                ),
                class_name="max-w-6xl mx-auto px-4 py-8",
            ),
            class_name="min-h-screen bg-gray-50 font-['Inter'] text-gray-900",
        ),
        class_name="flex flex-col min-h-screen",
        on_mount=FinanceState.load_data,
    )


def index() -> rx.Component:
    return rx.el.div(
        google_oauth_provider(
            rx.cond(AuthState.token_is_valid, dashboard_content(), login_page())
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=FinanceState.load_data)