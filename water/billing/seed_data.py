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
# 1. Bill Types  (billing_actions.py filters on exact string match)
# ---------------------------------------------------------------------------

def seed_bill_types():
    print("\n[1] Bill Types")
    for name in ["Tariff", "Standing Charge"]:
        create_if_missing("Bill Type", name, name_1=name)


# ---------------------------------------------------------------------------
# 2. Customer Types
# ---------------------------------------------------------------------------

def seed_customer_types():
    print("\n[2] Customer Types")
    for name in ["Domestic", "Commercial", "Institution"]:
        create_if_missing("Customer Type", name, name_1=name)


# ---------------------------------------------------------------------------
# 3. Billing Area  (tree – root first, then leaf nodes)
# ---------------------------------------------------------------------------

def seed_billing_areas():
    print("\n[3] Billing Areas")

    root = "Main Zone"
    if not frappe.db.exists("Billing Area", root):
        doc = frappe.new_doc("Billing Area")
        doc.billing_area_name = root
        doc.is_group = 1
        doc.root_area = 1
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"  Created Billing Area (root): {root}")
    else:
        print(f"  Exists  Billing Area (root): {root}")

    # Leaf nodes under root
    leaves = ["Zone A", "Zone B", "Zone C"]
    for leaf in leaves:
        if not frappe.db.exists("Billing Area", leaf):
            doc = frappe.new_doc("Billing Area")
            doc.billing_area_name = leaf
            doc.is_group = 0
            doc.parent_billing_area = root
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"  Created Billing Area (leaf): {leaf}")
        else:
            print(f"  Exists  Billing Area (leaf): {leaf}")


# ---------------------------------------------------------------------------
# 4. Billing Period
# ---------------------------------------------------------------------------

def seed_billing_period():
    print("\n[4] Billing Period")
    create_if_missing(
        "Billing Period",
        "April 2026",
        name_of_billing_period="April 2026",
        start_date="2026-04-01",
        end_date="2026-04-30",
    )


# ---------------------------------------------------------------------------
# 5. Bill Items  (tariff brackets + standing charge per customer type)
#
#    billing_actions.py:
#      - filters bill_type == 'Standing Charge'  → one record per customer_type
#      - filters bill_type == 'Tariff'           → multiple brackets sorted by start_reading
# ---------------------------------------------------------------------------

def seed_bill_items():
    print("\n[5] Bill Items")

    # Schema: (item_name, bill_type, customer_type, amount, start_reading, end_reading, flat_rate)
    items = [
        # ---------- Domestic ----------
        ("Domestic Standing Charge",     "Standing Charge", "Domestic",    200.0, 0,    0,    "No"),
        ("Domestic Tariff 0-6",          "Tariff",          "Domestic",     50.0, 0,    6,    "No"),
        ("Domestic Tariff 6-20",         "Tariff",          "Domestic",     75.0, 6,    20,   "No"),
        ("Domestic Tariff 20+",          "Tariff",          "Domestic",    100.0, 20,   0,    "No"),
        # ---------- Commercial ----------
        ("Commercial Standing Charge",   "Standing Charge", "Commercial",  500.0, 0,    0,    "No"),
        ("Commercial Tariff 0-20",       "Tariff",          "Commercial",   80.0, 0,    20,   "No"),
        ("Commercial Tariff 20+",        "Tariff",          "Commercial",  120.0, 20,   0,    "No"),
        # ---------- Institution ----------
        ("Institution Standing Charge",  "Standing Charge", "Institution", 800.0, 0,    0,    "No"),
        ("Institution Tariff 0-50",      "Tariff",          "Institution",  60.0, 0,    50,   "No"),
        ("Institution Tariff 50+",       "Tariff",          "Institution",  90.0, 50,   0,    "No"),
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
        {
            "customer_type": "Domestic",
            "disconnection_grace_period": 30,
        },
        {
            "customer_type": "Commercial",
            "disconnection_grace_period": 14,
        },
        {
            "customer_type": "Institution",
            "disconnection_grace_period": 30,
        },
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
        # (full_name,         phone_number,    id_no,         customer_type)
        ("Alice Wanjiku",     "0712345678",    "12345678",    "Domestic"),
        ("Bob Otieno",        "0723456789",    "23456789",    "Domestic"),
        ("Carol Muthoni",     "0734567890",    "34567890",    "Domestic"),
        ("Eastgate Traders",  "0745678901",    "45678901",    "Commercial"),
        ("Sunrise Motors",    "0756789012",    "56789012",    "Commercial"),
        ("Upande Academy",    "0767890123",    "67890123",    "Institution"),
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
    seed_customer_types()
    seed_billing_areas()
    seed_billing_period()
    seed_bill_items()
    seed_billing_settings_items()
    seed_customer_accounts()

    print("\nDone.")
