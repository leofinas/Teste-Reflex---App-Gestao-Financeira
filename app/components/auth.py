import reflex as rx
from reflex_google_auth import google_login
from app.states.auth_state import AuthState
from app.states.finance_state import FinanceState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("wallet", class_name="w-12 h-12 stroke-violet-600"),
                class_name="p-4 bg-violet-50 rounded-full mb-6",
            ),
            rx.el.h1(
                "Gestor Financeiro", class_name="text-3xl font-bold text-gray-900 mb-2"
            ),
            rx.el.p(
                "Controle suas finanças pessoais com facilidade e segurança.",
                class_name="text-gray-500 mb-8 text-center max-w-sm",
            ),
            rx.el.div(
                google_login(),
                class_name="w-full flex justify-center transform hover:scale-105 transition-transform duration-200",
            ),
            class_name="flex flex-col items-center justify-center p-10 bg-white rounded-2xl shadow-xl border border-gray-100 w-full max-w-md",
        ),
        class_name="min-h-screen w-full flex items-center justify-center bg-gray-50 font-['Inter']",
    )


def user_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=AuthState.tokeninfo["picture"],
                    class_name="w-9 h-9 rounded-full border border-gray-200",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.tokeninfo["name"],
                        class_name="text-sm font-semibold text-gray-900 leading-none",
                    ),
                    rx.el.p(
                        AuthState.tokeninfo["email"],
                        class_name="text-xs text-gray-500 mt-1 leading-none",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        FinanceState.hide_values,
                        rx.icon("eye", class_name="w-4 h-4"),
                        rx.icon("eye-off", class_name="w-4 h-4"),
                    ),
                    on_click=FinanceState.toggle_privacy,
                    class_name="p-2 text-gray-500 hover:text-violet-600 hover:bg-violet-50 rounded-full transition-colors mr-2",
                    title="Ocultar/Mostrar valores",
                ),
                rx.el.button(
                    rx.el.span("Sair", class_name="mr-2"),
                    rx.icon("log-out", class_name="w-4 h-4"),
                    on_click=AuthState.logout,
                    class_name="flex items-center px-3 py-1.5 text-sm font-medium text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors border border-transparent hover:border-red-100",
                ),
                class_name="flex items-center",
            ),
            class_name="max-w-6xl mx-auto px-4 flex justify-between items-center h-16",
        ),
        class_name="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm backdrop-blur-sm bg-white/90",
    )