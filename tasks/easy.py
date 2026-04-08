transactions = [
    # high risk ->block
    {"amount": 20000, "time": 2, "is_foreign": True,  "user_risk": 0.9,  "transaction_count_1hr": 8, "label": "block"},
    {"amount": 15000, "time": 1, "is_foreign": True,  "user_risk": 0.8,  "transaction_count_1hr": 6, "label": "block"},
    {"amount": 250000,"time": 5, "is_foreign": True,  "user_risk": 0.95, "transaction_count_1hr": 7, "label": "block"},
    {"amount": 50000, "time": 1, "is_foreign": False, "user_risk": 0.8,  "transaction_count_1hr": 7, "label": "block"},

    # medium risk ->flag
    {"amount": 7000, "time": 23, "is_foreign": True,  "user_risk": 0.6, "transaction_count_1hr": 3, "label": "flag"},
    {"amount": 9000, "time": 3,  "is_foreign": False, "user_risk": 0.7, "transaction_count_1hr": 4, "label": "flag"},
    {"amount": 4000, "time": 1,  "is_foreign": True,  "user_risk": 0.5, "transaction_count_1hr": 2, "label": "flag"},
    {"amount": 6000, "time": 22, "is_foreign": False, "user_risk": 0.6, "transaction_count_1hr": 3, "label": "flag"},

    #  Low risk → approve
    {"amount": 100,  "time": 14, "is_foreign": False, "user_risk": 0.2, "transaction_count_1hr": 1, "label": "approve"},
    {"amount": 200,  "time": 12, "is_foreign": False, "user_risk": 0.3, "transaction_count_1hr": 2, "label": "approve"},
    {"amount": 500,  "time": 9,  "is_foreign": False, "user_risk": 0.3, "transaction_count_1hr": 1, "label": "approve"},
    {"amount": 800,  "time": 16, "is_foreign": False, "user_risk": 0.2, "transaction_count_1hr": 2, "label": "approve"},

    #  Edge cases (important)
    {"amount": 12000, "time": 14, "is_foreign": False, "user_risk": 0.4, "transaction_count_1hr": 2, "label": "flag"},
    {"amount": 300,   "time": 2,  "is_foreign": True,  "user_risk": 0.7, "transaction_count_1hr": 5, "label": "flag"},
]