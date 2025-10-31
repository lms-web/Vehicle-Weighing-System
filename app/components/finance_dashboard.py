import reflex as rx
from app.states.finance_state import FinanceState


def stat_card(
    title: str, value: rx.Var[str], change: str | None = None
) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-sm font-medium text-gray-500"),
        rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
        rx.cond(change, rx.el.p(change, class_name="text-xs text-gray-500")),
        class_name="rounded-xl border bg-white p-4 shadow-sm",
    )


def finance_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Finance Dashboard", class_name="text-3xl font-bold mb-6 text-gray-800"
        ),
        rx.el.div(
            stat_card(
                "Total Revenue",
                f"Ksh {FinanceState.total_revenue.to_string()}",
                "+12% from last month",
            ),
            stat_card(
                "Total Expenses",
                f"Ksh {FinanceState.total_expenses.to_string()}",
                "+5% from last month",
            ),
            stat_card(
                "Net Profit",
                f"Ksh {FinanceState.net_profit.to_string()}",
                "+15% from last month",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6",
        ),
        rx.el.div(
            rx.el.h2(
                "Revenue Trends", class_name="text-xl font-semibold mb-4 text-gray-700"
            ),
            rx.recharts.line_chart(
                rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                rx.recharts.line(
                    data_key="revenue",
                    type="monotone",
                    stroke="#8884d8",
                    stroke_width=2,
                ),
                rx.recharts.x_axis(data_key="date"),
                rx.recharts.y_axis(),
                rx.recharts.tooltip(),
                data=FinanceState.daily_revenue,
                height=300,
            ),
            class_name="bg-white p-6 rounded-xl border shadow-sm mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Accounting Entries",
                    class_name="text-xl font-semibold text-gray-700",
                ),
                rx.el.select(
                    rx.el.option("All Categories", value="ALL"),
                    rx.el.option("Revenue", value="Revenue"),
                    rx.el.option("Expense", value="Expense"),
                    on_change=FinanceState.set_filter_category,
                    default_value="ALL",
                    class_name="p-2 border rounded-lg bg-white",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Date",
                                class_name="p-3 text-left text-sm font-semibold text-gray-600",
                            ),
                            rx.el.th(
                                "Description",
                                class_name="p-3 text-left text-sm font-semibold text-gray-600",
                            ),
                            rx.el.th(
                                "Debit",
                                class_name="p-3 text-right text-sm font-semibold text-gray-600",
                            ),
                            rx.el.th(
                                "Credit",
                                class_name="p-3 text-right text-sm font-semibold text-gray-600",
                            ),
                            rx.el.th(
                                "Category",
                                class_name="p-3 text-left text-sm font-semibold text-gray-600",
                            ),
                        ),
                        class_name="bg-gray-50",
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            FinanceState.filtered_accounting_entries,
                            lambda entry: rx.el.tr(
                                rx.el.td(entry["date"], class_name="p-3 text-sm"),
                                rx.el.td(
                                    entry["description"], class_name="p-3 text-sm"
                                ),
                                rx.el.td(
                                    f"Ksh {entry['debit'].to_string()}",
                                    class_name="p-3 text-sm text-right font-mono",
                                ),
                                rx.el.td(
                                    f"Ksh {entry['credit'].to_string()}",
                                    class_name="p-3 text-sm text-right font-mono text-green-600",
                                ),
                                rx.el.td(entry["category"], class_name="p-3 text-sm"),
                                class_name="border-b hover:bg-gray-50",
                            ),
                        )
                    ),
                    class_name="w-full",
                ),
                class_name="overflow-x-auto rounded-lg border",
            ),
            class_name="bg-white p-6 rounded-xl border shadow-sm",
        ),
        class_name="p-6",
    )