#!/usr/bin/env python3
"""
Setup script: crea e popola il database SQLite con 5 anni di dati storici
per oltre 100 ETF principali usando yfinance.

Uso: python setup_database.py
"""

import sqlite3
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import sys

DB_PATH = "etf_database.db"
START_DATE = (datetime.now() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")
END_DATE = datetime.now().strftime("%Y-%m-%d")

# Lista completa di ETF principali: (symbol, nome, categoria)
ETF_LIST = [
    # ── US Broad Market ──────────────────────────────────────────
    ("SPY",  "SPDR S&P 500 ETF Trust",                              "US Large Cap"),
    ("IVV",  "iShares Core S&P 500 ETF",                           "US Large Cap"),
    ("VOO",  "Vanguard S&P 500 ETF",                               "US Large Cap"),
    ("QQQ",  "Invesco QQQ Trust (NASDAQ-100)",                     "US Technology/Growth"),
    ("VTI",  "Vanguard Total Stock Market ETF",                    "US Total Market"),
    ("DIA",  "SPDR Dow Jones Industrial Average ETF",              "US Large Cap"),
    ("RSP",  "Invesco S&P 500 Equal Weight ETF",                   "US Large Cap Equal Weight"),
    ("MDY",  "SPDR S&P MidCap 400 ETF",                           "US Mid Cap"),
    ("IWM",  "iShares Russell 2000 ETF",                           "US Small Cap"),
    ("IWB",  "iShares Russell 1000 ETF",                           "US Large Cap"),
    ("IJH",  "iShares Core S&P Mid-Cap ETF",                       "US Mid Cap"),
    ("IJR",  "iShares Core S&P Small-Cap ETF",                     "US Small Cap"),

    # ── US Sectors (SPDR) ────────────────────────────────────────
    ("XLF",  "Financial Select Sector SPDR Fund",                  "US Financials"),
    ("XLK",  "Technology Select Sector SPDR Fund",                 "US Technology"),
    ("XLE",  "Energy Select Sector SPDR Fund",                     "US Energy"),
    ("XLV",  "Health Care Select Sector SPDR Fund",                "US Healthcare"),
    ("XLI",  "Industrial Select Sector SPDR Fund",                 "US Industrials"),
    ("XLY",  "Consumer Discretionary Select Sector SPDR Fund",    "US Consumer Discretionary"),
    ("XLC",  "Communication Services Select Sector SPDR Fund",    "US Communication"),
    ("XLB",  "Materials Select Sector SPDR Fund",                  "US Materials"),
    ("XLP",  "Consumer Staples Select Sector SPDR Fund",           "US Consumer Staples"),
    ("XLRE", "Real Estate Select Sector SPDR Fund",                "US Real Estate"),
    ("XLU",  "Utilities Select Sector SPDR Fund",                  "US Utilities"),

    # ── International Developed ──────────────────────────────────
    ("EFA",  "iShares MSCI EAFE ETF",                              "International Developed"),
    ("VEA",  "Vanguard FTSE Developed Markets ETF",                "International Developed"),
    ("IEFA", "iShares Core MSCI EAFE ETF",                         "International Developed"),
    ("VGK",  "Vanguard FTSE Europe ETF",                           "Europe"),
    ("EZU",  "iShares MSCI Eurozone ETF",                          "Eurozone"),
    ("EWJ",  "iShares MSCI Japan ETF",                             "Japan"),
    ("EWG",  "iShares MSCI Germany ETF",                           "Germany"),
    ("EWU",  "iShares MSCI United Kingdom ETF",                    "United Kingdom"),
    ("EWC",  "iShares MSCI Canada ETF",                            "Canada"),
    ("EWA",  "iShares MSCI Australia ETF",                         "Australia"),
    ("EWL",  "iShares MSCI Switzerland ETF",                       "Switzerland"),
    ("EWP",  "iShares MSCI Spain ETF",                             "Spain"),
    ("EWQ",  "iShares MSCI France ETF",                            "France"),
    ("EWI",  "iShares MSCI Italy ETF",                             "Italy"),

    # ── Emerging Markets ─────────────────────────────────────────
    ("EEM",  "iShares MSCI Emerging Markets ETF",                  "Emerging Markets"),
    ("VWO",  "Vanguard FTSE Emerging Markets ETF",                 "Emerging Markets"),
    ("IEMG", "iShares Core MSCI Emerging Markets ETF",             "Emerging Markets"),
    ("FXI",  "iShares China Large-Cap ETF",                        "China"),
    ("EWZ",  "iShares MSCI Brazil ETF",                            "Brazil"),
    ("INDA", "iShares MSCI India ETF",                             "India"),
    ("EWT",  "iShares MSCI Taiwan ETF",                            "Taiwan"),
    ("EWY",  "iShares MSCI South Korea ETF",                       "South Korea"),
    ("EWH",  "iShares MSCI Hong Kong ETF",                         "Hong Kong"),

    # ── Fixed Income – Government ────────────────────────────────
    ("AGG",  "iShares Core U.S. Aggregate Bond ETF",               "US Aggregate Bond"),
    ("BND",  "Vanguard Total Bond Market ETF",                     "US Total Bond"),
    ("TLT",  "iShares 20+ Year Treasury Bond ETF",                 "US Long-Term Treasury"),
    ("IEF",  "iShares 7-10 Year Treasury Bond ETF",                "US Mid-Term Treasury"),
    ("SHY",  "iShares 1-3 Year Treasury Bond ETF",                 "US Short-Term Treasury"),
    ("GOVT", "iShares U.S. Treasury Bond ETF",                     "US Treasury"),
    ("TIPS", "iShares TIPS Bond ETF",                              "US Inflation-Protected"),
    ("BNDX", "Vanguard Total International Bond ETF",              "International Bond"),
    ("EMB",  "iShares J.P. Morgan USD EM Bond ETF",                "Emerging Market Bond"),

    # ── Fixed Income – Corporate / High Yield ────────────────────
    ("LQD",  "iShares iBoxx $ IG Corporate Bond ETF",              "US Investment Grade Bond"),
    ("HYG",  "iShares iBoxx $ High Yield Corporate Bond ETF",      "US High Yield Bond"),
    ("JNK",  "SPDR Bloomberg High Yield Bond ETF",                 "US High Yield Bond"),
    ("MUB",  "iShares National Muni Bond ETF",                     "US Municipal Bond"),
    ("VCIT", "Vanguard Intermediate-Term Corporate Bond ETF",      "US Corporate Bond"),

    # ── Commodities ──────────────────────────────────────────────
    ("GLD",  "SPDR Gold Shares",                                   "Gold"),
    ("IAU",  "iShares Gold Trust",                                 "Gold"),
    ("SLV",  "iShares Silver Trust",                               "Silver"),
    ("USO",  "United States Oil Fund",                             "Oil"),
    ("DBC",  "Invesco DB Commodity Index Tracking Fund",           "Broad Commodities"),
    ("PDBC", "Invesco Optimum Yield Diversified Commodity ETF",    "Broad Commodities"),
    ("DBA",  "Invesco DB Agriculture Fund",                        "Agriculture"),
    ("COPX", "Global X Copper Miners ETF",                         "Copper Mining"),
    ("UNG",  "United States Natural Gas Fund",                     "Natural Gas"),

    # ── Real Estate ──────────────────────────────────────────────
    ("VNQ",  "Vanguard Real Estate ETF",                           "US Real Estate"),
    ("IYR",  "iShares U.S. Real Estate ETF",                       "US Real Estate"),
    ("VNQI", "Vanguard Global ex-U.S. Real Estate ETF",            "International Real Estate"),
    ("REM",  "iShares Mortgage Real Estate ETF",                   "Mortgage REITs"),

    # ── Technology & Innovation ──────────────────────────────────
    ("VGT",  "Vanguard Information Technology ETF",                "US Technology"),
    ("FTEC", "Fidelity MSCI Information Technology ETF",           "US Technology"),
    ("SOXX", "iShares Semiconductor ETF",                          "Semiconductors"),
    ("IGV",  "iShares Expanded Tech-Software Sector ETF",          "Software"),
    ("ARKK", "ARK Innovation ETF",                                 "Disruptive Innovation"),
    ("ARKQ", "ARK Autonomous Technology & Robotics ETF",           "Robotics/AI"),
    ("ARKG", "ARK Genomic Revolution ETF",                         "Genomics"),
    ("CIBR", "First Trust NASDAQ Cybersecurity ETF",               "Cybersecurity"),
    ("BOTZ", "Global X Robotics & Artificial Intelligence ETF",    "Robotics/AI"),
    ("AIQ",  "Global X Artificial Intelligence & Technology ETF",  "Artificial Intelligence"),

    # ── Clean Energy ─────────────────────────────────────────────
    ("ICLN", "iShares Global Clean Energy ETF",                    "Clean Energy"),
    ("TAN",  "Invesco Solar ETF",                                  "Solar Energy"),
    ("FAN",  "First Trust Global Wind Energy ETF",                 "Wind Energy"),
    ("QCLN", "First Trust NASDAQ Clean Edge Green Energy ETF",     "Clean Energy"),
    ("DRIV", "Global X Autonomous & Electric Vehicles ETF",        "Electric Vehicles"),
    ("LIT",  "Global X Lithium & Battery Tech ETF",                "Lithium/Battery"),

    # ── Healthcare & Biotech ─────────────────────────────────────
    ("IBB",  "iShares Biotechnology ETF",                          "Biotechnology"),
    ("XBI",  "SPDR S&P Biotech ETF",                               "Biotechnology"),
    ("IHF",  "iShares U.S. Healthcare Providers ETF",              "Healthcare Providers"),

    # ── Dividend ─────────────────────────────────────────────────
    ("VYM",  "Vanguard High Dividend Yield ETF",                   "US High Dividend"),
    ("DVY",  "iShares Select Dividend ETF",                        "US High Dividend"),
    ("DGRO", "iShares Core Dividend Growth ETF",                   "US Dividend Growth"),
    ("NOBL", "ProShares S&P 500 Dividend Aristocrats ETF",         "US Dividend Aristocrats"),
    ("SCHD", "Schwab U.S. Dividend Equity ETF",                    "US Dividend"),
    ("SDY",  "SPDR S&P Dividend ETF",                              "US High Dividend"),

    # ── Factor / Smart Beta ──────────────────────────────────────
    ("MTUM", "iShares MSCI USA Momentum Factor ETF",               "US Momentum"),
    ("QUAL", "iShares MSCI USA Quality Factor ETF",                "US Quality"),
    ("VLUE", "iShares MSCI USA Value Factor ETF",                  "US Value"),
    ("USMV", "iShares MSCI USA Min Vol Factor ETF",                "US Min Volatility"),
    ("SPLV", "Invesco S&P 500 Low Volatility ETF",                 "US Low Volatility"),
    ("MOAT", "VanEck Morningstar Wide Moat ETF",                   "US Wide Moat"),
    ("SPYG", "SPDR Portfolio S&P 500 Growth ETF",                  "US Growth"),
    ("SPYV", "SPDR Portfolio S&P 500 Value ETF",                   "US Value"),

    # ── Leveraged ────────────────────────────────────────────────
    ("TQQQ", "ProShares UltraPro QQQ (3x)",                        "US Technology 3x Leveraged"),
    ("SQQQ", "ProShares UltraPro Short QQQ (-3x)",                 "US Technology 3x Inverse"),
    ("UPRO", "ProShares UltraPro S&P500 (3x)",                     "US Large Cap 3x Leveraged"),
    ("SPXU", "ProShares UltraPro Short S&P500 (-3x)",              "US Large Cap 3x Inverse"),
    ("SSO",  "ProShares Ultra S&P500 (2x)",                        "US Large Cap 2x Leveraged"),
    ("SDS",  "ProShares UltraShort S&P500 (-2x)",                  "US Large Cap 2x Inverse"),

    # ── Multi-Asset ──────────────────────────────────────────────
    ("AOR",  "iShares Core Growth Allocation ETF",                 "Multi-Asset Growth"),
    ("AOM",  "iShares Core Moderate Allocation ETF",               "Multi-Asset Moderate"),
    ("AOA",  "iShares Core Aggressive Allocation ETF",             "Multi-Asset Aggressive"),
]


def create_database() -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS etf_info (
            symbol       TEXT PRIMARY KEY,
            name         TEXT NOT NULL,
            category     TEXT,
            currency     TEXT DEFAULT 'USD',
            last_updated TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS etf_prices (
            symbol    TEXT NOT NULL,
            date      TEXT NOT NULL,
            open      REAL,
            high      REAL,
            low       REAL,
            close     REAL,
            volume    INTEGER,
            adj_close REAL,
            PRIMARY KEY (symbol, date),
            FOREIGN KEY (symbol) REFERENCES etf_info(symbol)
        )
    """)

    c.execute("CREATE INDEX IF NOT EXISTS idx_prices_symbol      ON etf_prices(symbol)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_prices_date        ON etf_prices(date)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_prices_symbol_date ON etf_prices(symbol, date)")

    conn.commit()
    conn.close()
    print("✓ Schema database creato")


def download_and_store(symbol: str, name: str, category: str, conn: sqlite3.Connection) -> bool:
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=START_DATE, end=END_DATE, auto_adjust=False)

        if hist.empty:
            print(f"  ⚠  Nessun dato per {symbol}")
            return False

        info = ticker.fast_info
        currency = getattr(info, "currency", "USD") or "USD"

        # Normalizza colonne
        hist = hist.reset_index()
        hist["Date"] = pd.to_datetime(hist["Date"]).dt.strftime("%Y-%m-%d")

        adj_col = "Adj Close" if "Adj Close" in hist.columns else "Close"

        c = conn.cursor()

        c.execute("""
            INSERT OR REPLACE INTO etf_info (symbol, name, category, currency, last_updated)
            VALUES (?, ?, ?, ?, ?)
        """, (symbol, name, category, currency, datetime.now().strftime("%Y-%m-%d")))

        rows = []
        for _, row in hist.iterrows():
            vol = row.get("Volume", 0)
            rows.append((
                symbol,
                row["Date"],
                float(row["Open"])   if pd.notna(row.get("Open"))   else None,
                float(row["High"])   if pd.notna(row.get("High"))   else None,
                float(row["Low"])    if pd.notna(row.get("Low"))    else None,
                float(row["Close"])  if pd.notna(row.get("Close"))  else None,
                int(vol)             if pd.notna(vol)               else 0,
                float(row[adj_col]) if pd.notna(row.get(adj_col))  else None,
            ))

        c.executemany("""
            INSERT OR REPLACE INTO etf_prices
                (symbol, date, open, high, low, close, volume, adj_close)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, rows)

        conn.commit()
        print(f"  ✓ {len(rows):5d} record salvati")
        return True

    except Exception as exc:
        print(f"  ✗ Errore: {exc}")
        return False


def main() -> None:
    print("=" * 65)
    print("  ETF Database Setup")
    print(f"  Periodo: {START_DATE}  →  {END_DATE}")
    print(f"  ETF da scaricare: {len(ETF_LIST)}")
    print("=" * 65)

    create_database()

    conn = sqlite3.connect(DB_PATH)
    ok, fail = 0, []

    for i, (symbol, name, category) in enumerate(ETF_LIST, 1):
        print(f"\n[{i:3d}/{len(ETF_LIST)}] {symbol:6s} — {name}")
        if download_and_store(symbol, name, category, conn):
            ok += 1
        else:
            fail.append(symbol)
        time.sleep(0.4)   # rispetta rate limit Yahoo Finance

    conn.close()

    print("\n" + "=" * 65)
    print(f"  ✓ Completati: {ok}/{len(ETF_LIST)}")
    if fail:
        print(f"  ✗ Falliti:   {', '.join(fail)}")
    print("=" * 65)
    print("\nOra avvia il server con: uvicorn app:app --reload")


if __name__ == "__main__":
    main()
