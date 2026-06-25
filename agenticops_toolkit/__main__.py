from __future__ import annotations

import argparse

from agenticops_toolkit.scaffold import module_plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AgenticOps portfolio helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scaffold = subparsers.add_parser("scaffold", help="Preview a module scaffold.")
    scaffold.add_argument("module_name", help="Module name, for example credit-risk-mlops.")

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "scaffold":
        plan = module_plan(args.module_name)
        print(plan.to_markdown())


if __name__ == "__main__":
    main()

