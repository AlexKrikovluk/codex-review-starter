#!/usr/bin/env python3
"""Simple finance tracker for digital products."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class FinanceTracker:
    def __init__(self, data_path: str | Path = "finance.json") -> None:
        self.data_path = Path(data_path)
        self.data: dict[str, Any] = {"transactions": [], "monthly": {}}
        self._load()

    def _load(self) -> None:
        if self.data_path.exists():
            self.data = json.loads(self.data_path.read_text(encoding="utf-8"))

    def _save(self) -> None:
        self.data_path.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def add_transaction(
        self,
        kind: str,
        amount: float,
        currency: str = "USD",
        category: str = "general",
        note: str = "",
    ) -> dict[str, Any]:
        dt = datetime.now(timezone.utc)
        tx = {
            "date": dt.isoformat(),
            "kind": kind,  # revenue, expense, refund
            "amount": float(amount),
            "currency": currency,
            "category": category,
            "note": note,
        }
        self.data["transactions"].append(tx)
        self._save()
        return tx

    def monthly_summary(self, year: int, month: int) -> dict[str, float]:
        rev = 0.0
        exp = 0.0
        refunds = 0.0
        for tx in self.data["transactions"]:
            dt = datetime.fromisoformat(tx["date"])
            if dt.year == year and dt.month == month:
                kind = tx["kind"]
                amount = float(tx["amount"])
                if kind == "revenue":
                    rev += amount
                elif kind == "expense":
                    exp += amount
                elif kind == "refund":
                    refunds += amount
        net = rev - exp - refunds
        margin = (net / rev * 100) if rev > 0 else 0.0
        return {
            "revenue": rev,
            "expenses": exp,
            "refunds": refunds,
            "net": net,
            "margin_percent": margin,
        }

    def export_csv(self, csv_path: str | Path) -> Path:
        path = Path(csv_path)
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["date", "kind", "amount", "currency", "category", "note"]
            )
            writer.writeheader()
            for tx in self.data["transactions"]:
                writer.writerow(tx)
        return path

    def unit_economics(
        self,
        marketing_spend: float,
        customers: int,
        avg_price: float,
        monthly_cost_per_customer: float = 0.0,
        lifetime_months: int = 12,
    ) -> dict[str, Any]:
        if customers <= 0:
            raise ValueError("customers must be > 0")
        cac = marketing_spend / customers if customers else 0.0
        ltv = float(avg_price) * float(lifetime_months)
        ltv_cac = (ltv / cac) if cac > 0 else 0.0
        payback_months = (cac / avg_price) if avg_price > 0 else 0.0
        contribution_per_customer = avg_price - monthly_cost_per_customer
        return {
            "cac": cac,
            "ltv": ltv,
            "ltv_cac_ratio": ltv_cac,
            "payback_months": payback_months,
            "contribution_per_customer": contribution_per_customer,
            "healthy": ltv_cac >= 3 and payback_months <= 12,
        }

    def pricing_advisor(
        self,
        desired_margin_percent: float,
        target_cac: float,
        monthly_cost_per_customer: float,
        lifetime_months: int = 12,
    ) -> dict[str, Any]:
        margin = desired_margin_percent / 100.0
        if margin <= 0 or monthly_cost_per_customer < 0:
            raise ValueError("invalid margin or cost")
        minimum_price = monthly_cost_per_customer / margin
        recommended_price = max(minimum_price, target_cac * 3)
        return {
            "minimum_price": minimum_price,
            "recommended_price": recommended_price,
            "assumptions": {
                "desired_margin_percent": desired_margin_percent,
                "target_cac": target_cac,
                "monthly_cost_per_customer": monthly_cost_per_customer,
                "lifetime_months": lifetime_months,
            },
        }

    def health_check(self, year: int, month: int) -> dict[str, Any]:
        summary = self.monthly_summary(year, month)
        rev = summary["revenue"]
        exp = summary["expenses"]
        refunds = summary["refunds"]
        net = summary["net"]
        refund_rate = (refunds / rev * 100) if rev > 0 else 0.0
        burn_rate = exp if net < 0 else 0.0
        return {
            "revenue": rev,
            "expenses": exp,
            "refunds": refunds,
            "net": net,
            "margin_percent": summary["margin_percent"],
            "refund_rate_percent": refund_rate,
            "burn_rate": burn_rate,
            "status": "healthy" if refund_rate < 5 and summary["margin_percent"] > 40 else "review",
        }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Finance tracker for digital products")
    parser.add_argument("--data", default="finance.json", help="JSON data file")
    sub = parser.add_subparsers(dest="command")

    add = sub.add_parser("add", help="Add transaction")
    add.add_argument("kind", choices=["revenue", "expense", "refund"])
    add.add_argument("amount", type=float)
    add.add_argument("--currency", default="USD")
    add.add_argument("--category", default="general")
    add.add_argument("--note", default="")

    summary = sub.add_parser("summary", help="Monthly summary")
    summary.add_argument("year", type=int)
    summary.add_argument("month", type=int)

    export = sub.add_parser("export", help="Export CSV")
    export.add_argument("csv_path")

    unit = sub.add_parser("unit-economics", help="Unit economics check")
    unit.add_argument("--marketing-spend", type=float, required=True)
    unit.add_argument("--customers", type=int, required=True)
    unit.add_argument("--avg-price", type=float, required=True)
    unit.add_argument("--monthly-cost", type=float, default=0.0)
    unit.add_argument("--lifetime-months", type=int, default=12)

    pricing = sub.add_parser("pricing-advisor", help="Pricing advisor")
    pricing.add_argument("--margin-percent", type=float, required=True)
    pricing.add_argument("--target-cac", type=float, required=True)
    pricing.add_argument("--monthly-cost", type=float, required=True)
    pricing.add_argument("--lifetime-months", type=int, default=12)

    health = sub.add_parser("health-check", help="Monthly health check")
    health.add_argument("year", type=int)
    health.add_argument("month", type=int)

    args = parser.parse_args()
    tracker = FinanceTracker(args.data)

    if args.command == "add":
        tx = tracker.add_transaction(
            kind=args.kind,
            amount=args.amount,
            currency=args.currency,
            category=args.category,
            note=args.note,
        )
        print(tx)
    elif args.command == "summary":
        s = tracker.monthly_summary(args.year, args.month)
        print(json.dumps(s, indent=2))
    elif args.command == "export":
        path = tracker.export_csv(args.csv_path)
        print(path)
    elif args.command == "unit-economics":
        ue = tracker.unit_economics(
            marketing_spend=args.marketing_spend,
            customers=args.customers,
            avg_price=args.avg_price,
            monthly_cost_per_customer=args.monthly_cost,
            lifetime_months=args.lifetime_months,
        )
        print(json.dumps(ue, indent=2))
    elif args.command == "pricing-advisor":
        pa = tracker.pricing_advisor(
            desired_margin_percent=args.margin_percent,
            target_cac=args.target_cac,
            monthly_cost_per_customer=args.monthly_cost,
            lifetime_months=args.lifetime_months,
        )
        print(json.dumps(pa, indent=2))
    elif args.command == "health-check":
        hc = tracker.health_check(args.year, args.month)
        print(json.dumps(hc, indent=2))
    else:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
