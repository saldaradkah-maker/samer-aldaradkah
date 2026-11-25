import json
import os
from datetime import datetime
import flet as ft


ARABIC_DAYS = [
    "السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"
]

PYTHON_WEEKDAY_TO_ARABIC = {
    0: "الاثنين", 1: "الثلاثاء", 2: "الأربعاء",
    3: "الثلاثاء", 4: "الجمعة", 5: "السبت", 6: "الأحد"
}
PYTHON_WEEKDAY_TO_ARABIC[3] = "الخميس"

DEFAULT_ITEMS = [
    {"name": "ماء 1.5 لتر", "qty": 0, "buy_d": 0, "buy_f": 800, "sell_d": 0, "sell_f": 900},
    {"name": "شفرات", "qty": 4, "buy_d": 8, "buy_f": 500, "sell_d": 9, "sell_f": 600},
    {"name": "حلو 24 حبه", "qty": 0, "buy_d": 1, "buy_f": 900, "sell_d": 2, "sell_f": 400},
    {"name": "عصير باكيت", "qty": 0, "buy_d": 1, "buy_f": 850, "sell_d": 3, "sell_f": 600},
    {"name": "بسكوت 50 فلس", "qty": 4, "buy_d": 1, "buy_f": 950, "sell_d": 2, "sell_f": 400},
    {"name": "بسكوت 100 فلس (نوع 1)", "qty": 9, "buy_d": 2, "buy_f": 0, "sell_d": 2, "sell_f": 400},
    {"name": "طن", "qty": 0, "buy_d": 23, "buy_f": 0, "sell_d": 28, "sell_f": 800},
    {"name": "معمول 20 حبه", "qty": 14, "buy_d": 0, "buy_f": 800, "sell_d": 0, "sell_f": 900},
    {"name": "فستق", "qty": 0, "buy_d": 1, "buy_f": 900, "sell_d": 2, "sell_f": 500},
    {"name": "سردين", "qty": 0, "buy_d": 30, "buy_f": 0, "sell_d": 32, "sell_f": 500},
    {"name": "كيك 12 حبه", "qty": 10, "buy_d": 0, "buy_f": 950, "sell_d": 1, "sell_f": 200},
    {"name": "بسكوت 100 فلس (نوع 2)", "qty": 5, "buy_d": 1, "buy_f": 900, "sell_d": 2, "sell_f": 400},
    {"name": "حلو 10 حبات", "qty": 0, "buy_d": 0, "buy_f": 800, "sell_d": 1, "sell_f": 0},
    {"name": "شيبس 48 حبه", "qty": 0, "buy_d": 3, "buy_f": 750, "sell_d": 4, "sell_f": 800},
    {"name": "شيبس 84 حبه", "qty": 0, "buy_d": 6, "buy_f": 750, "sell_d": 8, "sell_f": 400},
    {"name": "شيبس 50 حبه", "qty": 0, "buy_d": 4, "buy_f": 250, "sell_d": 5, "sell_f": 0},
    {"name": "شيبس 60 حبه", "qty": 0, "buy_d": 4, "buy_f": 750, "sell_d": 6, "sell_f": 0},
    {"name": "شيبس 50 حبه (نوع 2)", "qty": 0, "buy_d": 4, "buy_f": 500, "sell_d": 5, "sell_f": 0},
    {"name": "مقرمشات 120 حبه", "qty": 0, "buy_d": 11, "buy_f": 0, "sell_d": 12, "sell_f": 0},
    {"name": "شيبس 120 حبه", "qty": 0, "buy_d": 11, "buy_f": 0, "sell_d": 12, "sell_f": 0},
    {"name": "اندومي", "qty": 0, "buy_d": 7, "buy_f": 500, "sell_d": 8, "sell_f": 400},
    {"name": "شطه", "qty": 1, "buy_d": 7, "buy_f": 500, "sell_d": 9, "sell_f": 0},
    {"name": "كولا 24 حبه", "qty": 0, "buy_d": 5, "buy_f": 500, "sell_d": 6, "sell_f": 0},
    {"name": "راس العبد", "qty": 5, "buy_d": 2, "buy_f": 900, "sell_d": 3, "sell_f": 600},
    {"name": "جلي", "qty": 10, "buy_d": 1, "buy_f": 900, "sell_d": 2, "sell_f": 400},
    {"name": "عصير 350 فلس", "qty": 4, "buy_d": 7, "buy_f": 0, "sell_d": 8, "sell_f": 400},
    {"name": "بف باف", "qty": 12, "buy_d": 0, "buy_f": 790, "sell_d": 8, "sell_f": 400},
    {"name": "شيبس 150 فلس", "qty": 0, "buy_d": 6, "buy_f": 250, "sell_d": 7, "sell_f": 500},
    {"name": "مطعمات", "qty": 5, "buy_d": 6, "buy_f": 0, "sell_d": 7, "sell_f": 200},
    {"name": "كب كيك", "qty": 0, "buy_d": 2, "buy_f": 750, "sell_d": 3, "sell_f": 0},
    {"name": "حلو 36 حبه", "qty": 0, "buy_d": 3, "buy_f": 300, "sell_d": 3, "sell_f": 600},
    {"name": "عصير 150 فلس", "qty": 0, "buy_d": 4, "buy_f": 800, "sell_d": 5, "sell_f": 400},
    {"name": "ماليزي", "qty": 1, "buy_d": 7, "buy_f": 500, "sell_d": 10, "sell_f": 0},
]

DEFAULT_BRANCHES = [
    "قيادة الكتيبة", "الغباوي", "القهوة", "الطافح القديم",
    "الدجنية", "الظليل", "التدريب", "المكتب"
]

DEFAULT_BRANCH_META = {
    "قيادة الكتيبة": {"cash_d": 188, "cash_f": 0, "disc_d": 0, "disc_f": 0},
    "الغباوي": {"cash_d": 0, "cash_f": 0, "disc_d": 0, "disc_f": 0},
    "القهوة": {"cash_d": 39, "cash_f": 0, "disc_d": 0, "disc_f": 0},
    "الطافح القديم": {"cash_d": 0, "cash_f": 0, "disc_d": 0, "disc_f": 0},
    "الدجنية": {"cash_d": 0, "cash_f": 0, "disc_d": 0, "disc_f": 0},
    "الظليل": {"cash_d": 0, "cash_f": 0, "disc_d": 0, "disc_f": 0},
    "التدريب": {"cash_d": 227, "cash_f": 0, "disc_d": 0, "disc_f": 0},
    "المكتب": {"cash_d": 227, "cash_f": 0, "disc_d": 0, "disc_f": 0},
}


def to_fils(d, f):
    return int(d) * 1000 + int(f)


def fmt_decimal(fils):
    sign = "-" if fils < 0 else ""
    a = abs(int(round(fils)))
    return f"{sign}{a // 1000}.{a % 1000:03d}"


def arabic_sort_key(text):
    s = str(text or "").strip().lower()
    table = str.maketrans({
        "أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا",
        "ى": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي"
    })
    return s.translate(table)


def main(page: ft.Page):
    page.title = "نظام الجرد والمبيعات وتوزيع البضاعة - مقهى الجندي والفروع"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    storage_dir = os.environ.get("FLET_APP_STORAGE_DATA") or os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(storage_dir, "canteen_inventory_data.json")

    def load_data():
        if os.path.exists(save_path):
            try:
                with open(save_path, "r", encoding="utf-8") as f:
                    d = json.load(f)
                return (
                    d.get("items", [dict(x) for x in DEFAULT_ITEMS]),
                    d.get("branches", list(DEFAULT_BRANCHES)),
                    d.get("branch_cash", {}),
                    d.get("branch_discounts", {}),
                    d.get("branch_qtys", {}),
                    d.get("archived_invoices", []),
                )
            except Exception:
                pass
        b_cash, b_disc, b_qtys = {}, {}, {}
        for b in DEFAULT_BRANCHES:
            meta = DEFAULT_BRANCH_META.get(b, {"cash_d": 0, "cash_f": 0, "disc_d": 0, "disc_f": 0})
            b_cash[b] = {"d": meta["cash_d"], "f": meta["cash_f"]}
            b_disc[b] = {"d": meta["disc_d"], "f": meta["disc_f"]}
            b_qtys[b] = {}
        return [dict(x) for x in DEFAULT_ITEMS], list(DEFAULT_BRANCHES), b_cash, b_disc, b_qtys, []

    items, branches, branch_cash, branch_discounts, branch_qtys, archived_invoices = load_data()
    items.sort(key=lambda x: (arabic_sort_key(x.get("name", "")), x.get("name", "")))

    def persist():
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump({
                "items": items,
                "branches": branches,
                "branch_cash": branch_cash,
                "branch_discounts": branch_discounts,
                "branch_qtys": branch_qtys,
                "archived_invoices": archived_invoices,
            }, f, ensure_ascii=False, indent=2)

    def notify(msg):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    # مؤشرات الكاش والفرق الرئيسية
    banner_cash = ft.Text("0.000 د", weight=ft.FontWeight.BOLD, size=15, color=ft.Colors.GREEN_800)
    banner_buy = ft.Text("0.000 د", weight=ft.FontWeight.BOLD, size=15, color=ft.Colors.BLUE_800)
    banner_diff = ft.Text("0.000 د", weight=ft.FontWeight.BOLD, size=15, color=ft.Colors.RED_800)

    # --- تبويب 1: الجرد الرئيسي ---
    kpi_buy = ft.Text("0.000 د", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.BLUE_800)
    kpi_sell = ft.Text("0.000 د", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.TEAL_800)
    kpi_profit = ft.Text("0.000 د", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.GREEN_800)

    tf_name = ft.TextField(label="اسم المادة", expand=True)
    tf_qty = ft.TextField(label="العدد", width=95, keyboard_type=ft.KeyboardType.NUMBER)
    tf_bd = ft.TextField(label="شراء (دينار)", width=110, keyboard_type=ft.KeyboardType.NUMBER)
    tf_bf = ft.TextField(label="شراء (فلس)", width=110, keyboard_type=ft.KeyboardType.NUMBER)
    tf_sd = ft.TextField(label="بيع (دينار)", width=110, keyboard_type=ft.KeyboardType.NUMBER)
    tf_sf = ft.TextField(label="بيع (فلس)", width=110, keyboard_type=ft.KeyboardType.NUMBER)

    main_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("المادة")),
            ft.DataColumn(ft.Text("العدد"), numeric=True),
            ft.DataColumn(ft.Text("إفرادي الشراء"), numeric=True),
            ft.DataColumn(ft.Text("إفرادي البيع"), numeric=True),
            ft.DataColumn(ft.Text("إجمالي الشراء"), numeric=True),
            ft.DataColumn(ft.Text("إجمالي البيع"), numeric=True),
            ft.DataColumn(ft.Text("الربح"), numeric=True),
            ft.DataColumn(ft.Text("المنزل"), numeric=True),
            ft.DataColumn(ft.Text("الفرق"), numeric=True),
        ],
        rows=[],
    )

    # --- تبويب 2: المواقع ---
    dd_branch = ft.Dropdown(label="الفرع / الموقع", options=[ft.dropdown.Option(b) for b in branches], value=branches[0] if branches else None, width=200)
    tf_cash_d = ft.TextField(label="نقد (دينار)", width=110, keyboard_type=ft.KeyboardType.NUMBER)
    tf_cash_f = ft.TextField(label="نقد (فلس)", width=110, keyboard_type=ft.KeyboardType.NUMBER)
    tf_disc_d = ft.TextField(label="خصم (دينار)", width=110, keyboard_type=ft.KeyboardType.NUMBER)
    tf_disc_f = ft.TextField(label="خصم (فلس)", width=110, keyboard_type=ft.KeyboardType.NUMBER)
    tf_new_branch = ft.TextField(label="اسم فرع جديد", width=180)

    branches_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("الفرع")),
            ft.DataColumn(ft.Text("البضاعة"), numeric=True),
            ft.DataColumn(ft.Text("الخصم"), numeric=True),
            ft.DataColumn(ft.Text("النقد"), numeric=True),
            ft.DataColumn(ft.Text("المستحق"), numeric=True),
            ft.DataColumn(ft.Text("الفرق"), numeric=True),
        ],
        rows=[],
    )

    # --- تبويب 3: سحب بضاعة فرع ---
    dd_det_branch = ft.Dropdown(label="الفرع", options=[ft.dropdown.Option(b) for b in branches], value=branches[0] if branches else None, width=180)
    dd_det_item = ft.Dropdown(label="المادة", options=[ft.dropdown.Option(it["name"]) for it in items], value=items[0]["name"] if items else None, width=220)
    tf_det_qty = ft.TextField(label="العدد المسحوب", width=120, keyboard_type=ft.KeyboardType.NUMBER)
    lbl_det_total = ft.Text("إجمالي الفرع: 0.000 د", weight=ft.FontWeight.BOLD, size=15, color=ft.Colors.GREEN_800)

    det_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("المادة")),
            ft.DataColumn(ft.Text("العدد"), numeric=True),
            ft.DataColumn(ft.Text("السعر"), numeric=True),
            ft.DataColumn(ft.Text("الإجمالي"), numeric=True),
        ],
        rows=[],
    )

    # --- تبويب 4: الأرشيف ---
    today_dt = datetime.now()
    dd_arch_branch = ft.Dropdown(label="الفرع", options=[ft.dropdown.Option(b) for b in branches], value=branches[0] if branches else None, width=180)
    dd_arch_day = ft.Dropdown(label="اليوم", options=[ft.dropdown.Option(d) for d in ARABIC_DAYS], value=PYTHON_WEEKDAY_TO_ARABIC.get(today_dt.weekday(), "الأربعاء"), width=130)
    tf_arch_date = ft.TextField(label="التاريخ", value=today_dt.strftime("%Y-%m-%d"), width=140)
    tf_arch_rep = ft.TextField(label="اسم المندوب", width=180)

    archive_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("رقم الفاتورة")),
            ft.DataColumn(ft.Text("الفرع")),
            ft.DataColumn(ft.Text("اليوم")),
            ft.DataColumn(ft.Text("التاريخ")),
            ft.DataColumn(ft.Text("المندوب")),
            ft.DataColumn(ft.Text("البضاعة"), numeric=True),
            ft.DataColumn(ft.Text("الكاش"), numeric=True),
            ft.DataColumn(ft.Text("الفرق"), numeric=True),
        ],
        rows=[],
    )

    def sync_branch_fields(e=None):
        b = dd_branch.value
        if b:
            c = branch_cash.get(b, {"d": 0, "f": 0})
            d = branch_discounts.get(b, {"d": 0, "f": 0})
            tf_cash_d.value = str(c.get("d", 0))
            tf_cash_f.value = str(c.get("f", 0))
            tf_disc_d.value = str(d.get("d", 0))
            tf_disc_f.value = str(d.get("f", 0))
            page.update()

    dd_branch.on_change = sync_branch_fields

    def refresh_ui(e=None):
        tot_b, tot_s = 0, 0
        main_table.rows.clear()
        for it in items:
            q = int(it.get("qty", 0))
            bu = to_fils(it.get("buy_d", 0), it.get("buy_f", 0))
            su = to_fils(it.get("sell_d", 0), it.get("sell_f", 0))
            bt = q * bu
            st = q * su
            pr = st - bt
            tot_b += bt
            tot_s += st
            dist = sum(int(branch_qtys.get(b, {}).get(it["name"], 0)) for b in branches)
            diff = q - dist
            main_table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(it["name"])),
                ft.DataCell(ft.Text(str(q))),
                ft.DataCell(ft.Text(fmt_decimal(bu))),
                ft.DataCell(ft.Text(fmt_decimal(su))),
                ft.DataCell(ft.Text(fmt_decimal(bt))),
                ft.DataCell(ft.Text(fmt_decimal(st))),
                ft.DataCell(ft.Text(fmt_decimal(pr))),
                ft.DataCell(ft.Text(str(dist))),
                ft.DataCell(ft.Text(f"+{diff}" if diff > 0 else str(diff))),
            ]))

        kpi_buy.value = f"{fmt_decimal(tot_b)} د"
        kpi_sell.value = f"{fmt_decimal(tot_s)} د"
        kpi_profit.value = f"{fmt_decimal(tot_s - tot_b)} د"

        price_map = {it["name"]: to_fils(it.get("sell_d", 0), it.get("sell_f", 0)) for it in items}
        branches_table.rows.clear()
        tot_cash_all, tot_disc_all = 0, 0
        for b in branches:
            g = sum(int(q) * price_map.get(k, 0) for k, q in branch_qtys.get(b, {}).items())
            c = to_fils(branch_cash.get(b, {}).get("d", 0), branch_cash.get(b, {}).get("f", 0))
            d = to_fils(branch_discounts.get(b, {}).get("d", 0), branch_discounts.get(b, {}).get("f", 0))
            tot_cash_all += c
            tot_disc_all += d
            net_due = max(0, g - d)
            df = c - net_due
            branches_table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(b)),
                ft.DataCell(ft.Text(fmt_decimal(g))),
                ft.DataCell(ft.Text(fmt_decimal(d))),
                ft.DataCell(ft.Text(fmt_decimal(c))),
                ft.DataCell(ft.Text(fmt_decimal(net_due))),
                ft.DataCell(ft.Text(fmt_decimal(df))),
            ]))

        net_buy_all = max(0, tot_b - tot_disc_all)
        banner_cash.value = f"{fmt_decimal(tot_cash_all)} د"
        banner_buy.value = f"{fmt_decimal(net_buy_all)} د"
        banner_diff.value = f"{fmt_decimal(tot_cash_all - net_buy_all)} د"

        det_table.rows.clear()
        sel_b = dd_det_branch.value
        if sel_b:
            b_tot = 0
            for it in items:
                q = int(branch_qtys.get(sel_b, {}).get(it["name"], 0))
                if q > 0:
                    su = price_map.get(it["name"], 0)
                    rt = q * su
                    b_tot += rt
                    det_table.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(it["name"])),
                        ft.DataCell(ft.Text(str(q))),
                        ft.DataCell(ft.Text(fmt_decimal(su))),
                        ft.DataCell(ft.Text(fmt_decimal(rt))),
                    ]))
            lbl_det_total.value = f"إجمالي ({sel_b}): {fmt_decimal(b_tot)} د"

        archive_table.rows.clear()
        for inv in archived_invoices:
            archive_table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(inv.get("inv_id", ""))),
                ft.DataCell(ft.Text(inv.get("branch", ""))),
                ft.DataCell(ft.Text(inv.get("day", ""))),
                ft.DataCell(ft.Text(inv.get("date", ""))),
                ft.DataCell(ft.Text(inv.get("rep", ""))),
                ft.DataCell(ft.Text(fmt_decimal(inv.get("goods_fils", 0)))),
                ft.DataCell(ft.Text(fmt_decimal(inv.get("cash_fils", 0)))),
                ft.DataCell(ft.Text(fmt_decimal(inv.get("diff_fils", 0)))),
            ]))

        page.update()

    dd_det_branch.on_change = refresh_ui

    def add_or_update_item(e):
        name = (tf_name.value or "").strip()
        if not name:
            notify("أدخل اسم المادة")
            return
        try:
            q = int(tf_qty.value or 0)
            bd, bf = int(tf_bd.value or 0), int(tf_bf.value or 0)
            sd, sf = int(tf_sd.value or 0), int(tf_sf.value or 0)
        except ValueError:
            notify("أدخل أرقاماً صحيحة")
            return

        existing = next((x for x in items if x["name"] == name), None)
        obj = {"name": name, "qty": q, "buy_d": bd, "buy_f": bf, "sell_d": sd, "sell_f": sf}
        if existing:
            existing.update(obj)
        else:
            items.append(obj)
        items.sort(key=lambda x: (arabic_sort_key(x.get("name", "")), x.get("name", "")))
        dd_det_item.options = [ft.dropdown.Option(x["name"]) for x in items]
        persist()
        refresh_ui()
        notify("تم الحفظ بنجاح")

    def clear_main_qty(e):
        for it in items:
            it["qty"] = 0
        persist()
        refresh_ui()
        notify("تم تفريغ عمود العدد")

    def save_branch_cash_disc(e):
        b = dd_branch.value
        if not b:
            return
        try:
            branch_cash[b] = {"d": int(tf_cash_d.value or 0), "f": int(tf_cash_f.value or 0)}
            branch_discounts[b] = {"d": int(tf_disc_d.value or 0), "f": int(tf_disc_f.value or 0)}
        except ValueError:
            notify("أدخل أرقاماً صحيحة")
            return
        persist()
        refresh_ui()
        notify(f"تم تحديث بيانات {b}")

    def add_branch(e):
        b = (tf_new_branch.value or "").strip()
        if not b or b in branches:
            notify("أدخل اسم فرع جديد غير مكرر")
            return
        branches.append(b)
        branch_cash[b] = {"d": 0, "f": 0}
        branch_discounts[b] = {"d": 0, "f": 0}
        branch_qtys[b] = {}
        opts = [ft.dropdown.Option(x) for x in branches]
        dd_branch.options = opts
        dd_det_branch.options = opts
        dd_arch_branch.options = opts
        tf_new_branch.value = ""
        persist()
        refresh_ui()
        notify(f"تمت إضافة {b}")

    def save_branch_qty(e):
        b = dd_det_branch.value
        it_name = dd_det_item.value
        if not b or not it_name:
            return
        try:
            branch_qtys.setdefault(b, {})[it_name] = int(tf_det_qty.value or 0)
        except ValueError:
            notify("أدخل عدداً صحيحاً")
            return
        persist()
        refresh_ui()
        notify("تم تحديث الكمية")

    def archive_invoice(e):
        b = dd_arch_branch.value
        rep = (tf_arch_rep.value or "").strip()
        if not b or not rep:
            notify("اختر الفرع وأدخل اسم المندوب")
            return
        price_map = {it["name"]: to_fils(it.get("sell_d", 0), it.get("sell_f", 0)) for it in items}
        g = sum(int(q) * price_map.get(k, 0) for k, q in branch_qtys.get(b, {}).items())
        c = to_fils(branch_cash.get(b, {}).get("d", 0), branch_cash.get(b, {}).get("f", 0))
        d = to_fils(branch_discounts.get(b, {}).get("d", 0), branch_discounts.get(b, {}).get("f", 0))
        net_due = max(0, g - d)
        inv_id = f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{len(archived_invoices) + 1}"
        archived_invoices.insert(0, {
            "inv_id": inv_id,
            "branch": b,
            "day": dd_arch_day.value or "",
            "date": tf_arch_date.value or "",
            "rep": rep,
            "goods_fils": g,
            "discount_fils": d,
            "net_due_fils": net_due,
            "cash_fils": c,
            "diff_fils": c - net_due,
        })
        persist()
        refresh_ui()
        notify(f"تمت أرشفة الفاتورة {inv_id}")

    tab1 = ft.Column([
        ft.Row([
            ft.Card(ft.Container(ft.Column([ft.Text("إجمالي الشراء"), kpi_buy]), padding=10)),
            ft.Card(ft.Container(ft.Column([ft.Text("إجمالي البيع"), kpi_sell]), padding=10)),
            ft.Card(ft.Container(ft.Column([ft.Text("صافي الربح"), kpi_profit]), padding=10)),
        ], wrap=True),
        ft.Row([tf_name, tf_qty], wrap=True),
        ft.Row([tf_bd, tf_bf, tf_sd, tf_sf], wrap=True),
        ft.Row([
            ft.ElevatedButton("حفظ / تحديث مادة", on_click=add_or_update_item),
            ft.OutlinedButton("تفريغ عمود العدد", on_click=clear_main_qty),
        ], wrap=True),
        ft.Row([main_table], scroll=ft.ScrollMode.AUTO),
    ], spacing=10)

    tab2 = ft.Column([
        ft.Row([dd_branch, tf_cash_d, tf_cash_f, tf_disc_d, tf_disc_f], wrap=True),
        ft.Row([
            ft.ElevatedButton("تحديث نقد وخصم الفرع", on_click=save_branch_cash_disc),
            tf_new_branch,
            ft.OutlinedButton("إضافة فرع", on_click=add_branch),
        ], wrap=True),
        ft.Row([branches_table], scroll=ft.ScrollMode.AUTO),
    ], spacing=10)

    tab3 = ft.Column([
        ft.Row([dd_det_branch, dd_det_item, tf_det_qty], wrap=True),
        ft.Row([
            ft.ElevatedButton("تحديث كمية الفرع", on_click=save_branch_qty),
            lbl_det_total,
        ], wrap=True),
        ft.Row([det_table], scroll=ft.ScrollMode.AUTO),
    ], spacing=10)

    tab4 = ft.Column([
        ft.Row([dd_arch_branch, dd_arch_day, tf_arch_date, tf_arch_rep], wrap=True),
        ft.ElevatedButton("حفظ الفاتورة في الأرشيف", on_click=archive_invoice),
        ft.Row([archive_table], scroll=ft.ScrollMode.AUTO),
    ], spacing=10)

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="1. الجرد الرئيسي", content=ft.Container(tab1, padding=10)),
            ft.Tab(text="2. المواقع والنقد", content=ft.Container(tab2, padding=10)),
            ft.Tab(text="3. سحب الفروع", content=ft.Container(tab3, padding=10)),
            ft.Tab(text="4. الأرشيف", content=ft.Container(tab4, padding=10)),
        ],
        expand=1,
    )

    page.add(
        ft.AppBar(
            title=ft.Text("مقهى الجندي والفروع - صمم بواسطة: الملازم/1 سامر الدرادكه", size=14),
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
        ),
        ft.Container(
            content=ft.Row([
                ft.Card(ft.Container(ft.Column([ft.Text("مجموع الكاش المقبوض"), banner_cash]), padding=8)),
                ft.Card(ft.Container(ft.Column([ft.Text("شراء الجرد الرئيسي"), banner_buy]), padding=8)),
                ft.Card(ft.Container(ft.Column([ft.Text("الفرق (الكاش - الشراء)"), banner_diff]), padding=8)),
            ], wrap=True),
            padding=8,
        ),
        tabs,
    )
    sync_branch_fields()
    refresh_ui()


if __name__ == "__main__":
    ft.app(target=main)
