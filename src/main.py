import flet as ft
from tradingview_ta import TA_Handler, Interval, Exchange

def get_data(symbol, exchange="NSE", screener="india"):
    try:
        handler = TA_Handler(
            symbol=symbol,
            exchange=exchange,
            screener=screener,
            interval=Interval.INTERVAL_1_DAY
        )
        data = handler.get_indicators([
            'description', 'close', 'change', 'volume', 'RSI', 'ADX',
            'price_52_week_high', 'price_52_week_low', 'EMA50', 'EMA200'
        ])
        recom = handler.get_analysis().summary["RECOMMENDATION"]
        return [data, recom]
    except:
        return None

def main(page: ft.Page):
    page.title = "Routes test app"

    def update(e):
        symbol = text_field.value.strip().upper()
        data = get_data(symbol)
        if data:
            text.value = text.value + str(data) +"\n\n"
        else:
            text.value = f"something went wrong {symbol}"
        text_field.value = ""
        page.update()

    def clear(e):
        text.value = ""
        page.update()

    text_field =ft.TextField()
    btn = ft.ElevatedButton(text ="Fetch",on_click=update)
    text = ft.Text("")
    cbtn = ft.ElevatedButton("clear",on_click = clear)


    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("InputPage"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                    text_field,
                    btn,
                    ft.ElevatedButton("Visit results", on_click=lambda _: page.go("/result")),
                ],
            )
        )
        if page.route == "/result":
            page.views.append(
                ft.View(
                    "/result",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                        text,
                        cbtn,
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main)
