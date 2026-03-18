"""
Role-Based Access Control
"""

ROLES = {
    "admin": {
        "label": "Admin",
        "modules": ["dashboard", "production", "bom", "inventory", "purchase",
                    "sales", "employees", "attendance", "accounts", "reports",
                    "settings", "users"],
    },
    "manager": {
        "label": "Manager",
        "modules": ["dashboard", "production", "bom", "inventory", "purchase",
                    "sales", "employees", "attendance", "reports"],
    },
    "supervisor": {
        "label": "Supervisor",
        "modules": ["dashboard", "production", "attendance", "inventory"],
    },
    "worker": {
        "label": "Worker",
        "modules": ["dashboard", "attendance"],
    },
    "accountant": {
        "label": "Accountant",
        "modules": ["dashboard", "accounts", "sales", "purchase", "reports"],
    },
}


def has_access(role: str, module: str) -> bool:
    return module in ROLES.get(role, {}).get("modules", [])
