import reflex as rx
from app.states.finance_state import FinanceState


def summary_card(
    title: str, value: rx.Var | str, icon: str, color_class: str, bg_class: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-6 h-6 {color_class}"),
            class_name=f"p-3 rounded-full {bg_class} mr-4",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm text-gray-500 font-medium"),
            rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
        ),
        class_name="flex items-center p-6 bg-white rounded-xl shadow-sm border border-gray-100 transition-transform hover:scale-[1.02] duration-300",
    )


def pie_chart_legend_item(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="w-3 h-3 rounded-full mr-2",
            style={"background_color": item["fill"]},
        ),
        rx.el.span(item["name"], class_name="text-sm text-gray-600 font-medium flex-1"),
        rx.el.div(
            rx.cond(
                FinanceState.hide_values,
                rx.el.span("R$ **** ", class_name="text-sm font-bold text-gray-900"),
                rx.el.span(
                    item["value_str"], class_name="text-sm font-bold text-gray-900"
                ),
            ),
            rx.el.span(
                item["pct_str"], class_name="text-sm font-medium text-gray-500 ml-1"
            ),
            class_name="flex items-center",
        ),
        class_name="flex items-center mb-2",
    )


def spending_distribution_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Distribuição por Categoria",
            class_name="text-lg font-semibold text-gray-800 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.cond(
                    FinanceState.pie_chart_data.length() > 0,
                    rx.recharts.pie_chart(
                        rx.recharts.graphing_tooltip(),
                        rx.recharts.pie(
                            data=FinanceState.pie_chart_data,
                            data_key="value",
                            name_key="name",
                            cx="50%",
                            cy="50%",
                            inner_radius=60,
                            outer_radius=80,
                            padding_angle=5,
                            stroke="#ffffff",
                            stroke_width=2,
                        ),
                        height=250,
                        width="100%",
                    ),
                    rx.el.div(
                        rx.icon("pie-chart", class_name="w-12 h-12 text-gray-200 mb-2"),
                        rx.el.p(
                            "Sem dados de despesas", class_name="text-sm text-gray-400"
                        ),
                        class_name="flex flex-col items-center justify-center h-full",
                    ),
                ),
                class_name="flex-1 min-h-[250px] flex items-center justify-center",
            ),
            rx.el.div(
                rx.cond(
                    FinanceState.pie_chart_data.length() > 0,
                    rx.foreach(FinanceState.pie_chart_data, pie_chart_legend_item),
                    rx.el.p(
                        "Adicione despesas para ver o gráfico",
                        class_name="text-sm text-gray-400 text-center italic",
                    ),
                ),
                rx.el.div(
                    rx.el.span("Total", class_name="text-sm font-medium text-gray-500"),
                    rx.el.span(
                        rx.cond(
                            FinanceState.hide_values,
                            "R$ ****",
                            f"R$ {FinanceState.total_monthly_spending:.2f}",
                        ),
                        class_name="text-lg font-bold text-gray-900",
                    ),
                    class_name="flex justify-between items-center mt-4 pt-4 border-t border-gray-100",
                ),
                class_name="w-full md:w-64 flex flex-col justify-center p-4",
            ),
            class_name="flex flex-col md:flex-row gap-4",
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-100",
    )


def dashboard_grid() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            summary_card(
                "Renda Mensal",
                rx.cond(
                    FinanceState.hide_values,
                    "R$ ****",
                    f"R$ {FinanceState.total_monthly_income:.2f}",
                ),
                "trending-up",
                "stroke-emerald-600",
                "bg-emerald-50",
            ),
            summary_card(
                "Despesas Mensais",
                rx.cond(
                    FinanceState.hide_values,
                    "R$ ****",
                    f"R$ {FinanceState.total_monthly_spending:.2f}",
                ),
                "trending-down",
                "stroke-rose-600",
                "bg-rose-50",
            ),
            summary_card(
                "Saldo Mensal",
                rx.cond(
                    FinanceState.hide_values,
                    "R$ ****",
                    f"R$ {FinanceState.monthly_balance:.2f}",
                ),
                "wallet",
                rx.cond(
                    FinanceState.monthly_balance >= 0,
                    "stroke-emerald-600",
                    "stroke-rose-600",
                ),
                rx.cond(
                    FinanceState.monthly_balance >= 0, "bg-emerald-50", "bg-rose-50"
                ),
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        spending_distribution_chart(),
        class_name="mb-10",
    )