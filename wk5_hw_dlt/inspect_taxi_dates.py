import glob
import os
from pathlib import Path

import duckdb


def main() -> None:
    # Search for DuckDB files from the repository root
    repo_root = Path(__file__).resolve().parents[2]
    patterns = [
        "**/*.duckdb",
    ]

    candidates: list[str] = []
    for pattern in patterns:
        candidates.extend(
            str(p) for p in repo_root.glob(pattern) if p.is_file() and p.suffix == ".duckdb"
        )

    if not candidates:
        print("NO_DB_FOUND")
        print(f"SEARCH_ROOT {repo_root}")
        return

    # Prefer a file that looks like it's for the taxi pipeline
    db_path = None
    for path in candidates:
        if "taxi" in os.path.basename(path):
            db_path = path
            break
    if db_path is None:
        db_path = candidates[0]

    print(f"USING_DB {db_path}")
    con = duckdb.connect(db_path)

    tables = [row[0] for row in con.execute("SHOW TABLES").fetchall()]
    print("TABLES", tables)

    for table in tables:
        cols = con.execute(f"PRAGMA table_info('{table}')").fetchall()
        dt_cols = [c[1] for c in cols if "time" in c[1].lower() or "date" in c[1].lower()]
        if not dt_cols:
            continue
        col = dt_cols[0]
        mn, mx = con.execute(f"SELECT MIN({col}), MAX({col}) FROM {table}").fetchone()
        print("RANGE", table, col, mn, mx)


if __name__ == "__main__":
    main()


