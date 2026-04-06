"""
Seed script for the Billing module.

Creates all prerequisite master records needed before Customer Accounts
can progress through the workflow, then seeds sample Customer Account records.

Run with:
    bench --site <site> execute water.billing.seed_data.seed
"""

import frappe


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def create_if_missing(doctype, name, **fields):
    """Insert a document only when it does not already exist. Returns the name."""
    if not frappe.db.exists(doctype, name):
        doc = frappe.new_doc(doctype)
        for k, v in fields.items():
            setattr(doc, k, v)
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"  Created {doctype}: {name}")
    else:
        print(f"  Exists  {doctype}: {name}")
    return name


# ---------------------------------------------------------------------------
# 1. Bill Types
#    "Tariff" and "Standing Charge" are used by billing_actions.py for
#    auto-billing. The rest are available for manual bill creation.
# ---------------------------------------------------------------------------

def seed_bill_types():
    print("\n[1] Bill Types")
    for name in [
        "Tariff",           # water consumption brackets (auto-billed)
        "Standing Charge",  # flat monthly charge (auto-billed)
        "Meter Rent",       # monthly meter rental fee
        "Sewer",            # sewer / sanitation charge
        "Penalty",          # late payment or reconnection penalty
        "Other",            # miscellaneous charges
    ]:
        create_if_missing("Bill Type", name, name_1=name)


# ---------------------------------------------------------------------------
# 2. Customer Types  (aligned with ERPNext Customer Groups)
#    ERPNext already has: Individual, Commercial, Non Profit, Government
#    Additional groups created here to cover full water utility range.
# ---------------------------------------------------------------------------

CUSTOMER_TYPES = [
    "Individual",
    "Commercial",
    "Non Profit",
    "Government",
    "Industrial",
    "School",
    "Health Facility",
    "Religious Organization",
    "Agricultural",
    "Water Kiosk",
]


def seed_erp_customer_groups():
    """Ensure each customer type exists as an ERPNext Customer Group."""
    print("\n[2a] ERPNext Customer Groups")
    existing = {r[0] for r in frappe.db.sql(
        "SELECT name FROM `tabCustomer Group`"
    )}
    for ctype in CUSTOMER_TYPES:
        if ctype not in existing:
            doc = frappe.new_doc("Customer Group")
            doc.customer_group_name = ctype
            doc.parent_customer_group = "All Customer Groups"
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"  Created Customer Group: {ctype}")
        else:
            print(f"  Exists  Customer Group: {ctype}")


def seed_customer_types():
    print("\n[2b] Water Customer Types")
    for name in CUSTOMER_TYPES:
        create_if_missing("Customer Type", name, name_1=name)


# ---------------------------------------------------------------------------
# 3. Billing Areas  — Uasin Gishu County, Kenya
#    Structure: Main Zone (root) → Sub-County (group) → Ward (leaf)
#    Zone A / B / C are kept as-is (already seeded).
# ---------------------------------------------------------------------------

def _create_area(name, parent=None, is_group=False):
    if frappe.db.exists("Billing Area", name):
        print(f"  Exists  Billing Area: {name}")
        return
    doc = frappe.new_doc("Billing Area")
    doc.billing_area_name = name
    doc.is_group = 1 if is_group else 0
    if parent:
        doc.parent_billing_area = parent
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Created Billing Area: {name}")


def seed_billing_areas():
    print("\n[3] Billing Areas (Uasin Gishu County wards)")

    # Root already exists as "Main Zone"
    root = "Main Zone"

    # Sub-counties → wards
    sub_counties = {
        "Ainabkoi": [
            "Ainabkoi/Olare",
            "Kaptagat",
            "Kapsoya",
            "Kimumu",
        ],
        "Kapseret": [
            "Simat/Kapseret",
            "Megun",
            "Langas",
            "Racecourse",
        ],
        "Kesses": [
            "Ngenyilel",
            "Tarakwa",
            "Cheptiret/Kipchamo",
            "Tulwet/Chuiyat",
        ],
        "Moiben": [
            "Moiben Town",
            "Karuna/Meibeki",
            "Ziwa",
            "Moi's Bridge",
        ],
        "Soy": [
            "Soy Town",
            "Burnt Forest",
            "Kuinet/Kabiyet",
            "Chepterwai",
        ],
        "Turbo": [
            "Turbo Town",
            "Huruma",
            "Kabenes",
            "Ngeria",
        ],
    }

    for sub_county, wards in sub_counties.items():
        _create_area(sub_county, parent=root, is_group=True)
        for ward in wards:
            _create_area(ward, parent=sub_county, is_group=False)


# ---------------------------------------------------------------------------
# 4. Billing Periods  (full calendar year 2026)
# ---------------------------------------------------------------------------

def seed_billing_period():
    print("\n[4] Billing Periods")
    periods = [
        ("January 2026",   "2026-01-01", "2026-01-31"),
        ("February 2026",  "2026-02-01", "2026-02-28"),
        ("March 2026",     "2026-03-01", "2026-03-31"),
        ("April 2026",     "2026-04-01", "2026-04-30"),
        ("May 2026",       "2026-05-01", "2026-05-31"),
        ("June 2026",      "2026-06-01", "2026-06-30"),
        ("July 2026",      "2026-07-01", "2026-07-31"),
        ("August 2026",    "2026-08-01", "2026-08-31"),
        ("September 2026", "2026-09-01", "2026-09-30"),
        ("October 2026",   "2026-10-01", "2026-10-31"),
        ("November 2026",  "2026-11-01", "2026-11-30"),
        ("December 2026",  "2026-12-01", "2026-12-31"),
    ]
    for name, start, end in periods:
        create_if_missing(
            "Billing Period", name,
            name_of_billing_period=name,
            start_date=start,
            end_date=end,
        )


# ---------------------------------------------------------------------------
# 5. Bill Items
#    One Standing Charge per customer type is picked by billing_actions.py
#    (list_of_standing_charges[0]).  Tariff brackets are sorted by
#    start_reading and applied progressively.
#    Meter Rent, Sewer, Penalty are available for manual billing.
#
#    Schema: (item_name, bill_type, customer_type, amount,
#             start_reading, end_reading, flat_rate)
# ---------------------------------------------------------------------------

def seed_bill_items():
    print("\n[5] Bill Items")

    items = [
        # ── Individual ────────────────────────────────────────────────────
        ("Individual Fixed Charge",          "Standing Charge", "Individual",            150.0,  0,   0,  "No"),
        ("Individual Meter Rent",            "Meter Rent",      "Individual",             50.0,  0,   0,  "No"),
        ("Individual Water 0-6",             "Tariff",          "Individual",             45.0,  0,   6,  "No"),
        ("Individual Water 6-20",            "Tariff",          "Individual",             70.0,  6,  20,  "No"),
        ("Individual Water 20+",             "Tariff",          "Individual",             95.0, 20,   0,  "No"),
        ("Individual Sewer",                 "Sewer",           "Individual",            100.0,  0,   0,  "No"),
        ("Individual Penalty",               "Penalty",         "Individual",            200.0,  0,   0,  "No"),

        # ── Commercial ────────────────────────────────────────────────────
        ("Commercial Fixed Charge",          "Standing Charge", "Commercial",            500.0,  0,   0,  "No"),
        ("Commercial Meter Rent",            "Meter Rent",      "Commercial",            100.0,  0,   0,  "No"),
        ("Commercial Water 0-20",            "Tariff",          "Commercial",             80.0,  0,  20,  "No"),
        ("Commercial Water 20-50",           "Tariff",          "Commercial",            110.0, 20,  50,  "No"),
        ("Commercial Water 50+",             "Tariff",          "Commercial",            140.0, 50,   0,  "No"),
        ("Commercial Sewer",                 "Sewer",           "Commercial",            300.0,  0,   0,  "No"),
        ("Commercial Penalty",               "Penalty",         "Commercial",            500.0,  0,   0,  "No"),

        # ── Non Profit ────────────────────────────────────────────────────
        ("Non Profit Fixed Charge",          "Standing Charge", "Non Profit",            200.0,  0,   0,  "No"),
        ("Non Profit Meter Rent",            "Meter Rent",      "Non Profit",             50.0,  0,   0,  "No"),
        ("Non Profit Water 0-10",            "Tariff",          "Non Profit",             45.0,  0,  10,  "No"),
        ("Non Profit Water 10-30",           "Tariff",          "Non Profit",             65.0, 10,  30,  "No"),
        ("Non Profit Water 30+",             "Tariff",          "Non Profit",             85.0, 30,   0,  "No"),
        ("Non Profit Sewer",                 "Sewer",           "Non Profit",            150.0,  0,   0,  "No"),

        # ── Government ────────────────────────────────────────────────────
        ("Government Fixed Charge",          "Standing Charge", "Government",            800.0,  0,   0,  "No"),
        ("Government Meter Rent",            "Meter Rent",      "Government",            150.0,  0,   0,  "No"),
        ("Government Water 0-50",            "Tariff",          "Government",             60.0,  0,  50,  "No"),
        ("Government Water 50-200",          "Tariff",          "Government",             80.0, 50, 200,  "No"),
        ("Government Water 200+",            "Tariff",          "Government",            100.0,200,   0,  "No"),
        ("Government Sewer",                 "Sewer",           "Government",            400.0,  0,   0,  "No"),

        # ── Industrial ────────────────────────────────────────────────────
        ("Industrial Fixed Charge",          "Standing Charge", "Industrial",           1500.0,  0,   0,  "No"),
        ("Industrial Meter Rent",            "Meter Rent",      "Industrial",            300.0,  0,   0,  "No"),
        ("Industrial Water 0-100",           "Tariff",          "Industrial",             90.0,  0, 100,  "No"),
        ("Industrial Water 100-500",         "Tariff",          "Industrial",            120.0,100, 500,  "No"),
        ("Industrial Water 500+",            "Tariff",          "Industrial",            150.0,500,   0,  "No"),
        ("Industrial Sewer",                 "Sewer",           "Industrial",            800.0,  0,   0,  "No"),
        ("Industrial Penalty",               "Penalty",         "Industrial",           1000.0,  0,   0,  "No"),

        # ── School ────────────────────────────────────────────────────────
        ("School Fixed Charge",              "Standing Charge", "School",                300.0,  0,   0,  "No"),
        ("School Meter Rent",                "Meter Rent",      "School",                 75.0,  0,   0,  "No"),
        ("School Water 0-30",                "Tariff",          "School",                 50.0,  0,  30,  "No"),
        ("School Water 30-100",              "Tariff",          "School",                 70.0, 30, 100,  "No"),
        ("School Water 100+",                "Tariff",          "School",                 90.0,100,   0,  "No"),
        ("School Sewer",                     "Sewer",           "School",                200.0,  0,   0,  "No"),

        # ── Health Facility ───────────────────────────────────────────────
        ("Health Facility Fixed Charge",     "Standing Charge", "Health Facility",        600.0,  0,   0,  "No"),
        ("Health Facility Meter Rent",       "Meter Rent",      "Health Facility",        120.0,  0,   0,  "No"),
        ("Health Facility Water 0-50",       "Tariff",          "Health Facility",         55.0,  0,  50,  "No"),
        ("Health Facility Water 50-200",     "Tariff",          "Health Facility",         75.0, 50, 200,  "No"),
        ("Health Facility Water 200+",       "Tariff",          "Health Facility",         95.0,200,   0,  "No"),
        ("Health Facility Sewer",            "Sewer",           "Health Facility",        350.0,  0,   0,  "No"),

        # ── Religious Organization ────────────────────────────────────────
        ("Religious Fixed Charge",           "Standing Charge", "Religious Organization", 150.0,  0,   0,  "No"),
        ("Religious Meter Rent",             "Meter Rent",      "Religious Organization",  50.0,  0,   0,  "No"),
        ("Religious Water 0-10",             "Tariff",          "Religious Organization",  40.0,  0,  10,  "No"),
        ("Religious Water 10-30",            "Tariff",          "Religious Organization",  60.0, 10,  30,  "No"),
        ("Religious Water 30+",              "Tariff",          "Religious Organization",  80.0, 30,   0,  "No"),

        # ── Agricultural ──────────────────────────────────────────────────
        ("Agricultural Fixed Charge",        "Standing Charge", "Agricultural",           250.0,  0,   0,  "No"),
        ("Agricultural Meter Rent",          "Meter Rent",      "Agricultural",            80.0,  0,   0,  "No"),
        ("Agricultural Water 0-100",         "Tariff",          "Agricultural",            35.0,  0, 100,  "No"),
        ("Agricultural Water 100-500",       "Tariff",          "Agricultural",            50.0,100, 500,  "No"),
        ("Agricultural Water 500+",          "Tariff",          "Agricultural",            70.0,500,   0,  "No"),

        # ── Water Kiosk ───────────────────────────────────────────────────
        ("Water Kiosk Fixed Charge",         "Standing Charge", "Water Kiosk",            100.0,  0,   0,  "No"),
        ("Water Kiosk Meter Rent",           "Meter Rent",      "Water Kiosk",             30.0,  0,   0,  "No"),
        ("Water Kiosk Water 0-50",           "Tariff",          "Water Kiosk",             30.0,  0,  50,  "No"),
        ("Water Kiosk Water 50-200",         "Tariff",          "Water Kiosk",             45.0, 50, 200,  "No"),
        ("Water Kiosk Water 200+",           "Tariff",          "Water Kiosk",             60.0,200,   0,  "No"),
        ("Water Kiosk Penalty",              "Penalty",         "Water Kiosk",            150.0,  0,   0,  "No"),
    ]

    for item_name, bill_type, customer_type, amount, start_reading, end_reading, flat_rate in items:
        if not frappe.db.exists("Bill Item", item_name):
            doc = frappe.new_doc("Bill Item")
            doc.item_name = item_name
            doc.bill_type = bill_type
            doc.customer_type = customer_type
            doc.amount = amount
            doc.start_reading = start_reading
            doc.end_reading = end_reading
            doc.flat_rate = flat_rate
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"  Created Bill Item: {item_name}")
        else:
            print(f"  Exists  Bill Item: {item_name}")


# ---------------------------------------------------------------------------
# 6. Billing Settings Items  (one per customer type, named by customer_type)
#    customer_account.py: frappe.get_doc("Billing Settings Item", self.customer_type)
# ---------------------------------------------------------------------------

def seed_billing_settings_items():
    print("\n[6] Billing Settings Items")

    configs = [
        {"customer_type": "Individual",            "disconnection_grace_period": 30},
        {"customer_type": "Commercial",            "disconnection_grace_period": 14},
        {"customer_type": "Non Profit",            "disconnection_grace_period": 30},
        {"customer_type": "Government",            "disconnection_grace_period": 60},
        {"customer_type": "Industrial",            "disconnection_grace_period": 14},
        {"customer_type": "School",                "disconnection_grace_period": 30},
        {"customer_type": "Health Facility",       "disconnection_grace_period": 60},
        {"customer_type": "Religious Organization","disconnection_grace_period": 30},
        {"customer_type": "Agricultural",          "disconnection_grace_period": 30},
        {"customer_type": "Water Kiosk",           "disconnection_grace_period": 7},
    ]

    for cfg in configs:
        name = cfg["customer_type"]
        if not frappe.db.exists("Billing Settings Item", name):
            doc = frappe.new_doc("Billing Settings Item")
            for k, v in cfg.items():
                setattr(doc, k, v)
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"  Created Billing Settings Item: {name}")
        else:
            print(f"  Exists  Billing Settings Item: {name}")


# ---------------------------------------------------------------------------
# 7. Customer Accounts  (Draft status – no workflow validation triggered)
# ---------------------------------------------------------------------------

def seed_customer_accounts():
    print("\n[7] Customer Accounts")

    customers = [
        # (full_name,                  phone_number,    id_no,          customer_type)
        # Individual
        ("Alice Wanjiku",              "0712345678",    "12345678",     "Individual"),
        ("Bob Otieno",                 "0723456789",    "23456789",     "Individual"),
        ("Carol Muthoni",              "0734567890",    "34567890",     "Individual"),
        ("David Kamau",                "0798765432",    "98765432",     "Individual"),
        ("Grace Njeri",                "0711223344",    "11223344",     "Individual"),
        ("James Kipchoge",             "0722334455",    "22334455",     "Individual"),
        ("Mary Achieng",               "0733445566",    "33445566",     "Individual"),
        ("Peter Mutua",                "0744556677",    "44556677",     "Individual"),
        # Commercial
        ("Eastgate Traders",           "0745678901",    "45678901",     "Commercial"),
        ("Sunrise Motors",             "0756789012",    "56789012",     "Commercial"),
        ("Westside Supermarket",       "0767890234",    "67890234",     "Commercial"),
        ("Riverbank Hotel",            "0778901345",    "78901345",     "Commercial"),
        # Government
        ("County Council Office",      "0790123567",    "90123567",     "Government"),
        ("Kenya Power Eldoret",        "0791234678",    "91234678",     "Government"),
        # School
        ("Titansoft Academy",          "0767890123",    "67890123",     "School"),
        ("Eldoret Primary School",     "0792345789",    "92345789",     "School"),
        # Health Facility
        ("St. Mary's Hospital",        "0789012456",    "89012456",     "Health Facility"),
        ("Moi Teaching Hospital",      "0793456890",    "93456890",     "Health Facility"),
        # Non Profit
        ("Red Cross Eldoret",          "0794567901",    "94567901",     "Non Profit"),
        # Industrial
        ("Uasin Gishu Mills Ltd",      "0795678012",    "95678012",     "Industrial"),
        # Religious Organization
        ("St. Patrick's Cathedral",    "0796789123",    "96789123",     "Religious Organization"),
        # Agricultural
        ("Kipchoge Farm",              "0797890234",    "97890234",     "Agricultural"),
        # Water Kiosk
        ("Langas Water Point",         "0799012456",    "99012456",     "Water Kiosk"),
        ("Huruma Kiosk",               "0700123567",    "00123567",     "Water Kiosk"),
    ]

    for full_name, phone_number, id_no, customer_type in customers:
        exists = frappe.db.exists(
            "Customer Account",
            {"full_name": full_name, "phone_number": phone_number},
        )
        if not exists:
            doc = frappe.new_doc("Customer Account")
            doc.full_name = full_name
            doc.phone_number = phone_number
            doc.id_no = id_no
            doc.customer_type = customer_type
            doc.status = "Draft"
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"  Created Customer Account: {full_name} ({customer_type})")
        else:
            print(f"  Exists  Customer Account: {full_name}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def seed():
    print("=" * 60)
    print("Seeding Billing module data …")
    print("=" * 60)

    seed_bill_types()
    seed_erp_customer_groups()
    seed_customer_types()
    seed_billing_areas()
    seed_billing_period()
    seed_bill_items()
    seed_billing_settings_items()
    seed_customer_accounts()

    print("\nDone.")
