"""
etf_catalog.py — Catalogo completo di 200+ ETF globali raggruppati per tipologia e regione.
"""

FULL_ETF_CATALOG = [
    # ── US Broad Market ───────────────────────────────────────────────────────
    {"symbol": "SPY",  "name": "SPDR S&P 500 ETF Trust",               "category": "US Large Cap",    "group_name": "US Broad Market", "region": "US"},
    {"symbol": "VOO",  "name": "Vanguard S&P 500 ETF",                  "category": "US Large Cap",    "group_name": "US Broad Market", "region": "US"},
    {"symbol": "IVV",  "name": "iShares Core S&P 500 ETF",              "category": "US Large Cap",    "group_name": "US Broad Market", "region": "US"},
    {"symbol": "VTI",  "name": "Vanguard Total Stock Market ETF",        "category": "US Total Market", "group_name": "US Broad Market", "region": "US"},
    {"symbol": "ITOT", "name": "iShares Core S&P Total US Stock Market", "category": "US Total Market", "group_name": "US Broad Market", "region": "US"},
    {"symbol": "QQQ",  "name": "Invesco QQQ Trust",                      "category": "US Large Cap Growth","group_name": "US Broad Market","region": "US"},
    {"symbol": "QQQM", "name": "Invesco Nasdaq 100 ETF",                 "category": "US Large Cap Growth","group_name": "US Broad Market","region": "US"},
    {"symbol": "IWB",  "name": "iShares Russell 1000 ETF",               "category": "US Large Cap",    "group_name": "US Broad Market", "region": "US"},
    {"symbol": "IWM",  "name": "iShares Russell 2000 ETF",               "category": "US Small Cap",    "group_name": "US Broad Market", "region": "US"},
    {"symbol": "VB",   "name": "Vanguard Small-Cap ETF",                 "category": "US Small Cap",    "group_name": "US Broad Market", "region": "US"},
    {"symbol": "IJR",  "name": "iShares Core S&P Small-Cap ETF",         "category": "US Small Cap",    "group_name": "US Broad Market", "region": "US"},
    {"symbol": "MDY",  "name": "SPDR S&P MidCap 400 ETF",                "category": "US Mid Cap",      "group_name": "US Broad Market", "region": "US"},
    {"symbol": "VO",   "name": "Vanguard Mid-Cap ETF",                   "category": "US Mid Cap",      "group_name": "US Broad Market", "region": "US"},
    {"symbol": "IJH",  "name": "iShares Core S&P Mid-Cap ETF",           "category": "US Mid Cap",      "group_name": "US Broad Market", "region": "US"},
    {"symbol": "DIA",  "name": "SPDR Dow Jones Industrial Average ETF",  "category": "US Large Cap",    "group_name": "US Broad Market", "region": "US"},
    {"symbol": "RSP",  "name": "Invesco S&P 500 Equal Weight ETF",       "category": "US Large Cap",    "group_name": "US Broad Market", "region": "US"},

    # ── US Sectors ────────────────────────────────────────────────────────────
    {"symbol": "XLK",  "name": "Technology Select Sector SPDR",          "category": "Technology",      "group_name": "US Sectors", "region": "US"},
    {"symbol": "XLF",  "name": "Financial Select Sector SPDR",           "category": "Financials",      "group_name": "US Sectors", "region": "US"},
    {"symbol": "XLV",  "name": "Health Care Select Sector SPDR",         "category": "Health Care",     "group_name": "US Sectors", "region": "US"},
    {"symbol": "XLE",  "name": "Energy Select Sector SPDR",              "category": "Energy",          "group_name": "US Sectors", "region": "US"},
    {"symbol": "XLI",  "name": "Industrial Select Sector SPDR",          "category": "Industrials",     "group_name": "US Sectors", "region": "US"},
    {"symbol": "XLC",  "name": "Communication Services Select Sector SPDR","category": "Communication", "group_name": "US Sectors", "region": "US"},
    {"symbol": "XLY",  "name": "Consumer Discretionary Select Sector SPDR","category": "Consumer Disc.", "group_name": "US Sectors", "region": "US"},
    {"symbol": "XLP",  "name": "Consumer Staples Select Sector SPDR",    "category": "Consumer Staples","group_name": "US Sectors", "region": "US"},
    {"symbol": "XLU",  "name": "Utilities Select Sector SPDR",           "category": "Utilities",       "group_name": "US Sectors", "region": "US"},
    {"symbol": "XLRE", "name": "Real Estate Select Sector SPDR",         "category": "Real Estate",     "group_name": "US Sectors", "region": "US"},
    {"symbol": "XLB",  "name": "Materials Select Sector SPDR",           "category": "Materials",       "group_name": "US Sectors", "region": "US"},
    {"symbol": "VGT",  "name": "Vanguard Information Technology ETF",    "category": "Technology",      "group_name": "US Sectors", "region": "US"},
    {"symbol": "VHT",  "name": "Vanguard Health Care ETF",               "category": "Health Care",     "group_name": "US Sectors", "region": "US"},
    {"symbol": "VFH",  "name": "Vanguard Financials ETF",                "category": "Financials",      "group_name": "US Sectors", "region": "US"},
    {"symbol": "VDE",  "name": "Vanguard Energy ETF",                    "category": "Energy",          "group_name": "US Sectors", "region": "US"},

    # ── International Developed ───────────────────────────────────────────────
    {"symbol": "EFA",  "name": "iShares MSCI EAFE ETF",                  "category": "Intl Developed",  "group_name": "International Developed", "region": "International"},
    {"symbol": "VEA",  "name": "Vanguard FTSE Developed Markets ETF",    "category": "Intl Developed",  "group_name": "International Developed", "region": "International"},
    {"symbol": "IEFA", "name": "iShares Core MSCI EAFE ETF",             "category": "Intl Developed",  "group_name": "International Developed", "region": "International"},
    {"symbol": "SCHF", "name": "Schwab International Equity ETF",        "category": "Intl Developed",  "group_name": "International Developed", "region": "International"},
    {"symbol": "EWJ",  "name": "iShares MSCI Japan ETF",                 "category": "Japan",           "group_name": "International Developed", "region": "Japan"},
    {"symbol": "EWG",  "name": "iShares MSCI Germany ETF",               "category": "Germany",         "group_name": "International Developed", "region": "Europe"},
    {"symbol": "EWU",  "name": "iShares MSCI United Kingdom ETF",        "category": "UK",              "group_name": "International Developed", "region": "Europe"},
    {"symbol": "EWQ",  "name": "iShares MSCI France ETF",                "category": "France",          "group_name": "International Developed", "region": "Europe"},
    {"symbol": "EWI",  "name": "iShares MSCI Italy ETF",                 "category": "Italy",           "group_name": "International Developed", "region": "Europe"},
    {"symbol": "EWL",  "name": "iShares MSCI Switzerland ETF",           "category": "Switzerland",     "group_name": "International Developed", "region": "Europe"},
    {"symbol": "EWP",  "name": "iShares MSCI Spain ETF",                 "category": "Spain",           "group_name": "International Developed", "region": "Europe"},
    {"symbol": "EWD",  "name": "iShares MSCI Sweden ETF",                "category": "Sweden",          "group_name": "International Developed", "region": "Europe"},
    {"symbol": "EWN",  "name": "iShares MSCI Netherlands ETF",           "category": "Netherlands",     "group_name": "International Developed", "region": "Europe"},
    {"symbol": "EWA",  "name": "iShares MSCI Australia ETF",             "category": "Australia",       "group_name": "International Developed", "region": "Asia-Pacific"},
    {"symbol": "EWC",  "name": "iShares MSCI Canada ETF",                "category": "Canada",          "group_name": "International Developed", "region": "North America"},
    {"symbol": "EWS",  "name": "iShares MSCI Singapore ETF",             "category": "Singapore",       "group_name": "International Developed", "region": "Asia-Pacific"},
    {"symbol": "EWH",  "name": "iShares MSCI Hong Kong ETF",             "category": "Hong Kong",       "group_name": "International Developed", "region": "Asia-Pacific"},
    {"symbol": "EWK",  "name": "iShares MSCI Belgium ETF",               "category": "Belgium",         "group_name": "International Developed", "region": "Europe"},
    {"symbol": "NZAC", "name": "SPDR MSCI ACWI IMI ETF",                 "category": "Global",          "group_name": "International Developed", "region": "Global"},
    {"symbol": "ACWI", "name": "iShares MSCI ACWI ETF",                  "category": "Global",          "group_name": "International Developed", "region": "Global"},
    {"symbol": "VT",   "name": "Vanguard Total World Stock ETF",         "category": "Global",          "group_name": "International Developed", "region": "Global"},

    # ── Emerging Markets ──────────────────────────────────────────────────────
    {"symbol": "EEM",  "name": "iShares MSCI Emerging Markets ETF",      "category": "Emerging Markets","group_name": "Emerging Markets", "region": "Emerging"},
    {"symbol": "VWO",  "name": "Vanguard FTSE Emerging Markets ETF",     "category": "Emerging Markets","group_name": "Emerging Markets", "region": "Emerging"},
    {"symbol": "IEMG", "name": "iShares Core MSCI Emerging Markets ETF", "category": "Emerging Markets","group_name": "Emerging Markets", "region": "Emerging"},
    {"symbol": "SCHE", "name": "Schwab Emerging Markets Equity ETF",     "category": "Emerging Markets","group_name": "Emerging Markets", "region": "Emerging"},
    {"symbol": "FXI",  "name": "iShares China Large-Cap ETF",            "category": "China",           "group_name": "Emerging Markets", "region": "Asia"},
    {"symbol": "MCHI", "name": "iShares MSCI China ETF",                 "category": "China",           "group_name": "Emerging Markets", "region": "Asia"},
    {"symbol": "KWEB", "name": "KraneShares CSI China Internet ETF",     "category": "China Tech",      "group_name": "Emerging Markets", "region": "Asia"},
    {"symbol": "INDA", "name": "iShares MSCI India ETF",                 "category": "India",           "group_name": "Emerging Markets", "region": "Asia"},
    {"symbol": "EWZ",  "name": "iShares MSCI Brazil ETF",                "category": "Brazil",          "group_name": "Emerging Markets", "region": "Latin America"},
    {"symbol": "EWT",  "name": "iShares MSCI Taiwan ETF",                "category": "Taiwan",          "group_name": "Emerging Markets", "region": "Asia"},
    {"symbol": "EWY",  "name": "iShares MSCI South Korea ETF",           "category": "South Korea",     "group_name": "Emerging Markets", "region": "Asia"},
    {"symbol": "EWW",  "name": "iShares MSCI Mexico ETF",                "category": "Mexico",          "group_name": "Emerging Markets", "region": "Latin America"},
    {"symbol": "RSX",  "name": "VanEck Russia ETF",                      "category": "Russia",          "group_name": "Emerging Markets", "region": "Europe/Asia"},
    {"symbol": "GXC",  "name": "SPDR S&P China ETF",                     "category": "China",           "group_name": "Emerging Markets", "region": "Asia"},

    # ── Fixed Income — Government ─────────────────────────────────────────────
    {"symbol": "TLT",  "name": "iShares 20+ Year Treasury Bond ETF",     "category": "Long-Term Gov",   "group_name": "Fixed Income", "region": "US"},
    {"symbol": "IEF",  "name": "iShares 7-10 Year Treasury Bond ETF",    "category": "Mid-Term Gov",    "group_name": "Fixed Income", "region": "US"},
    {"symbol": "SHY",  "name": "iShares 1-3 Year Treasury Bond ETF",     "category": "Short-Term Gov",  "group_name": "Fixed Income", "region": "US"},
    {"symbol": "BIL",  "name": "SPDR Bloomberg 1-3 Month T-Bill ETF",    "category": "T-Bill",          "group_name": "Fixed Income", "region": "US"},
    {"symbol": "GOVT", "name": "iShares US Treasury Bond ETF",           "category": "US Treasury",     "group_name": "Fixed Income", "region": "US"},
    {"symbol": "VGLT", "name": "Vanguard Long-Term Treasury ETF",        "category": "Long-Term Gov",   "group_name": "Fixed Income", "region": "US"},
    {"symbol": "VGSH", "name": "Vanguard Short-Term Treasury ETF",       "category": "Short-Term Gov",  "group_name": "Fixed Income", "region": "US"},
    {"symbol": "TIPS", "name": "iShares TIPS Bond ETF",                  "category": "Inflation-Protected","group_name": "Fixed Income","region": "US"},
    {"symbol": "VTIP", "name": "Vanguard Short-Term Inflation-Protected ETF","category": "Inflation-Protected","group_name": "Fixed Income","region": "US"},

    # ── Fixed Income — Corporate ──────────────────────────────────────────────
    {"symbol": "LQD",  "name": "iShares iBoxx $ Investment Grade Corp Bond ETF","category": "IG Corporate","group_name": "Fixed Income","region": "US"},
    {"symbol": "VCIT", "name": "Vanguard Intermediate-Term Corporate Bond ETF","category": "IG Corporate","group_name": "Fixed Income","region": "US"},
    {"symbol": "VCSH", "name": "Vanguard Short-Term Corporate Bond ETF", "category": "IG Corporate",    "group_name": "Fixed Income", "region": "US"},
    {"symbol": "VCLT", "name": "Vanguard Long-Term Corporate Bond ETF",  "category": "IG Corporate",    "group_name": "Fixed Income", "region": "US"},
    {"symbol": "BND",  "name": "Vanguard Total Bond Market ETF",         "category": "Total Bond",      "group_name": "Fixed Income", "region": "US"},
    {"symbol": "AGG",  "name": "iShares Core US Aggregate Bond ETF",     "category": "Total Bond",      "group_name": "Fixed Income", "region": "US"},

    # ── Fixed Income — High Yield ─────────────────────────────────────────────
    {"symbol": "HYG",  "name": "iShares iBoxx $ High Yield Corporate Bond ETF","category": "High Yield","group_name": "Fixed Income","region": "US"},
    {"symbol": "JNK",  "name": "SPDR Bloomberg High Yield Bond ETF",     "category": "High Yield",      "group_name": "Fixed Income", "region": "US"},
    {"symbol": "FALN", "name": "iShares Fallen Angels USD Bond ETF",     "category": "High Yield",      "group_name": "Fixed Income", "region": "US"},

    # ── Fixed Income — International ──────────────────────────────────────────
    {"symbol": "BNDX", "name": "Vanguard Total International Bond ETF",  "category": "Intl Bond",       "group_name": "Fixed Income", "region": "International"},
    {"symbol": "EMB",  "name": "iShares JP Morgan USD Emerging Markets Bond ETF","category": "EM Bond","group_name": "Fixed Income","region": "Emerging"},

    # ── Commodities ───────────────────────────────────────────────────────────
    {"symbol": "GLD",  "name": "SPDR Gold Shares",                        "category": "Gold",            "group_name": "Commodities", "region": "Global"},
    {"symbol": "IAU",  "name": "iShares Gold Trust",                      "category": "Gold",            "group_name": "Commodities", "region": "Global"},
    {"symbol": "GLDM", "name": "SPDR Gold MiniShares",                    "category": "Gold",            "group_name": "Commodities", "region": "Global"},
    {"symbol": "SLV",  "name": "iShares Silver Trust",                    "category": "Silver",          "group_name": "Commodities", "region": "Global"},
    {"symbol": "PPLT", "name": "Aberdeen Standard Physical Platinum ETF", "category": "Platinum",        "group_name": "Commodities", "region": "Global"},
    {"symbol": "USO",  "name": "United States Oil Fund",                  "category": "Oil",             "group_name": "Commodities", "region": "Global"},
    {"symbol": "UNG",  "name": "United States Natural Gas Fund",          "category": "Natural Gas",     "group_name": "Commodities", "region": "Global"},
    {"symbol": "DBA",  "name": "Invesco DB Agriculture Fund",             "category": "Agriculture",     "group_name": "Commodities", "region": "Global"},
    {"symbol": "PDBC", "name": "Invesco Optimum Yield Diversified Commodity ETF","category": "Diversified Commodity","group_name": "Commodities","region": "Global"},
    {"symbol": "GSG",  "name": "iShares S&P GSCI Commodity-Indexed Trust","category": "Diversified Commodity","group_name": "Commodities","region": "Global"},
    {"symbol": "COMT", "name": "iShares GSCI Commodity Dynamic Roll Strategy ETF","category": "Diversified Commodity","group_name": "Commodities","region": "Global"},

    # ── Real Estate (REITs) ───────────────────────────────────────────────────
    {"symbol": "VNQ",  "name": "Vanguard Real Estate ETF",               "category": "US REIT",         "group_name": "Real Estate", "region": "US"},
    {"symbol": "IYR",  "name": "iShares US Real Estate ETF",             "category": "US REIT",         "group_name": "Real Estate", "region": "US"},
    {"symbol": "SCHH", "name": "Schwab US REIT ETF",                     "category": "US REIT",         "group_name": "Real Estate", "region": "US"},
    {"symbol": "REM",  "name": "iShares Mortgage Real Estate ETF",       "category": "Mortgage REIT",   "group_name": "Real Estate", "region": "US"},
    {"symbol": "VNQI", "name": "Vanguard Global ex-US Real Estate ETF",  "category": "Intl REIT",       "group_name": "Real Estate", "region": "International"},
    {"symbol": "RWX",  "name": "SPDR Dow Jones International Real Estate ETF","category": "Intl REIT","group_name": "Real Estate","region": "International"},

    # ── Technology & Innovation ───────────────────────────────────────────────
    {"symbol": "SOXX", "name": "iShares Semiconductor ETF",              "category": "Semiconductors",  "group_name": "Technology & Innovation", "region": "US"},
    {"symbol": "SMH",  "name": "VanEck Semiconductor ETF",               "category": "Semiconductors",  "group_name": "Technology & Innovation", "region": "US"},
    {"symbol": "HACK", "name": "ETFMG Prime Cyber Security ETF",         "category": "Cybersecurity",   "group_name": "Technology & Innovation", "region": "Global"},
    {"symbol": "BUG",  "name": "Global X Cybersecurity ETF",             "category": "Cybersecurity",   "group_name": "Technology & Innovation", "region": "Global"},
    {"symbol": "IGV",  "name": "iShares Expanded Tech-Software Sector ETF","category": "Software",      "group_name": "Technology & Innovation", "region": "US"},
    {"symbol": "CLOU", "name": "Global X Cloud Computing ETF",           "category": "Cloud Computing", "group_name": "Technology & Innovation", "region": "Global"},
    {"symbol": "AIQ",  "name": "Global X Artificial Intelligence & Technology ETF","category": "AI",   "group_name": "Technology & Innovation", "region": "Global"},
    {"symbol": "BOTZ", "name": "Global X Robotics & Artificial Intelligence ETF","category": "Robotics/AI","group_name": "Technology & Innovation","region": "Global"},
    {"symbol": "ARKK", "name": "ARK Innovation ETF",                     "category": "Disruptive Innovation","group_name": "Technology & Innovation","region": "Global"},
    {"symbol": "ARKW", "name": "ARK Next Generation Internet ETF",       "category": "Internet/Tech",   "group_name": "Technology & Innovation", "region": "Global"},
    {"symbol": "ARKG", "name": "ARK Genomic Revolution ETF",             "category": "Genomics",        "group_name": "Technology & Innovation", "region": "Global"},
    {"symbol": "ARKF", "name": "ARK Fintech Innovation ETF",             "category": "Fintech",         "group_name": "Technology & Innovation", "region": "Global"},

    # ── Clean Energy ─────────────────────────────────────────────────────────
    {"symbol": "ICLN", "name": "iShares Global Clean Energy ETF",        "category": "Clean Energy",    "group_name": "Clean Energy", "region": "Global"},
    {"symbol": "QCLN", "name": "First Trust NASDAQ Clean Edge Green Energy Index Fund","category": "Clean Energy","group_name": "Clean Energy","region": "Global"},
    {"symbol": "CNRG", "name": "SPDR S&P Kensho Clean Power ETF",        "category": "Clean Energy",    "group_name": "Clean Energy", "region": "Global"},
    {"symbol": "TAN",  "name": "Invesco Solar ETF",                      "category": "Solar",           "group_name": "Clean Energy", "region": "Global"},
    {"symbol": "FAN",  "name": "First Trust Global Wind Energy ETF",     "category": "Wind",            "group_name": "Clean Energy", "region": "Global"},
    {"symbol": "LIT",  "name": "Global X Lithium & Battery Tech ETF",    "category": "Battery/EV",      "group_name": "Clean Energy", "region": "Global"},
    {"symbol": "DRIV", "name": "Global X Autonomous & Electric Vehicles ETF","category": "EV",         "group_name": "Clean Energy", "region": "Global"},
    {"symbol": "KARS", "name": "KraneShares Electric Vehicles & Future Mobility ETF","category": "EV", "group_name": "Clean Energy", "region": "Global"},

    # ── Healthcare & Biotech ──────────────────────────────────────────────────
    {"symbol": "IBB",  "name": "iShares Biotechnology ETF",              "category": "Biotech",         "group_name": "Healthcare & Biotech", "region": "US"},
    {"symbol": "XBI",  "name": "SPDR S&P Biotech ETF",                   "category": "Biotech",         "group_name": "Healthcare & Biotech", "region": "US"},
    {"symbol": "BBH",  "name": "VanEck Biotech ETF",                     "category": "Biotech",         "group_name": "Healthcare & Biotech", "region": "US"},
    {"symbol": "IHI",  "name": "iShares US Medical Devices ETF",         "category": "Medical Devices", "group_name": "Healthcare & Biotech", "region": "US"},
    {"symbol": "IHF",  "name": "iShares US Healthcare Providers ETF",    "category": "Healthcare Providers","group_name": "Healthcare & Biotech","region": "US"},
    {"symbol": "GNOM", "name": "Global X Genomics & Biotechnology ETF",  "category": "Genomics",        "group_name": "Healthcare & Biotech", "region": "Global"},

    # ── Dividend ──────────────────────────────────────────────────────────────
    {"symbol": "VYM",  "name": "Vanguard High Dividend Yield ETF",       "category": "High Dividend",   "group_name": "Dividend", "region": "US"},
    {"symbol": "DVY",  "name": "iShares Select Dividend ETF",            "category": "High Dividend",   "group_name": "Dividend", "region": "US"},
    {"symbol": "SDY",  "name": "SPDR S&P Dividend ETF",                  "category": "Dividend Growth", "group_name": "Dividend", "region": "US"},
    {"symbol": "VIG",  "name": "Vanguard Dividend Appreciation ETF",     "category": "Dividend Growth", "group_name": "Dividend", "region": "US"},
    {"symbol": "DGRO", "name": "iShares Core Dividend Growth ETF",       "category": "Dividend Growth", "group_name": "Dividend", "region": "US"},
    {"symbol": "NOBL", "name": "ProShares S&P 500 Dividend Aristocrats ETF","category": "Dividend Aristocrats","group_name": "Dividend","region": "US"},
    {"symbol": "IDV",  "name": "iShares International Select Dividend ETF","category": "Intl Dividend", "group_name": "Dividend", "region": "International"},
    {"symbol": "VYMI", "name": "Vanguard International High Dividend Yield ETF","category": "Intl Dividend","group_name": "Dividend","region": "International"},

    # ── Factor / Smart Beta ───────────────────────────────────────────────────
    {"symbol": "MTUM", "name": "iShares MSCI USA Momentum Factor ETF",   "category": "Momentum",        "group_name": "Factor / Smart Beta", "region": "US"},
    {"symbol": "QUAL", "name": "iShares MSCI USA Quality Factor ETF",    "category": "Quality",         "group_name": "Factor / Smart Beta", "region": "US"},
    {"symbol": "VLUE", "name": "iShares MSCI USA Value Factor ETF",      "category": "Value",           "group_name": "Factor / Smart Beta", "region": "US"},
    {"symbol": "SIZE", "name": "iShares MSCI USA Size Factor ETF",       "category": "Size",            "group_name": "Factor / Smart Beta", "region": "US"},
    {"symbol": "USMV", "name": "iShares MSCI USA Min Vol Factor ETF",    "category": "Low Volatility",  "group_name": "Factor / Smart Beta", "region": "US"},
    {"symbol": "EFAV", "name": "iShares MSCI EAFE Min Vol Factor ETF",   "category": "Low Volatility",  "group_name": "Factor / Smart Beta", "region": "International"},
    {"symbol": "IWF",  "name": "iShares Russell 1000 Growth ETF",        "category": "Growth",          "group_name": "Factor / Smart Beta", "region": "US"},
    {"symbol": "IWD",  "name": "iShares Russell 1000 Value ETF",         "category": "Value",           "group_name": "Factor / Smart Beta", "region": "US"},
    {"symbol": "COWZ", "name": "Pacer US Cash Cows 100 ETF",             "category": "Cash Flow",       "group_name": "Factor / Smart Beta", "region": "US"},

    # ── Multi-Asset ───────────────────────────────────────────────────────────
    {"symbol": "AOR",  "name": "iShares Core Growth Allocation ETF",     "category": "Balanced",        "group_name": "Multi-Asset", "region": "Global"},
    {"symbol": "AOM",  "name": "iShares Core Moderate Allocation ETF",   "category": "Balanced",        "group_name": "Multi-Asset", "region": "Global"},
    {"symbol": "AOA",  "name": "iShares Core Aggressive Allocation ETF", "category": "Aggressive",      "group_name": "Multi-Asset", "region": "Global"},
    {"symbol": "AOK",  "name": "iShares Core Conservative Allocation ETF","category": "Conservative",   "group_name": "Multi-Asset", "region": "Global"},
    {"symbol": "GAL",  "name": "SPDR SSgA Global Allocation ETF",        "category": "Global Allocation","group_name": "Multi-Asset","region": "Global"},

    # ── Leveraged ─────────────────────────────────────────────────────────────
    {"symbol": "TQQQ", "name": "ProShares UltraPro QQQ (3x)",            "category": "3x Leveraged",    "group_name": "Leveraged / Inverse", "region": "US"},
    {"symbol": "UPRO", "name": "ProShares UltraPro S&P 500 (3x)",        "category": "3x Leveraged",    "group_name": "Leveraged / Inverse", "region": "US"},
    {"symbol": "SSO",  "name": "ProShares Ultra S&P 500 (2x)",           "category": "2x Leveraged",    "group_name": "Leveraged / Inverse", "region": "US"},
    {"symbol": "QLD",  "name": "ProShares Ultra QQQ (2x)",               "category": "2x Leveraged",    "group_name": "Leveraged / Inverse", "region": "US"},
    {"symbol": "TMF",  "name": "Direxion Daily 20+ Year Treasury Bull 3x","category": "3x Leveraged",   "group_name": "Leveraged / Inverse", "region": "US"},
    {"symbol": "UVXY", "name": "ProShares Ultra VIX Short-Term Futures ETF","category": "Volatility",   "group_name": "Leveraged / Inverse", "region": "US"},

    # ── Inverse ───────────────────────────────────────────────────────────────
    {"symbol": "SH",   "name": "ProShares Short S&P 500",                "category": "1x Inverse",      "group_name": "Leveraged / Inverse", "region": "US"},
    {"symbol": "SDS",  "name": "ProShares UltraShort S&P 500 (-2x)",     "category": "2x Inverse",      "group_name": "Leveraged / Inverse", "region": "US"},
    {"symbol": "SPXS", "name": "Direxion Daily S&P 500 Bear 3x",         "category": "3x Inverse",      "group_name": "Leveraged / Inverse", "region": "US"},
    {"symbol": "PSQ",  "name": "ProShares Short QQQ (-1x)",              "category": "1x Inverse",      "group_name": "Leveraged / Inverse", "region": "US"},
    {"symbol": "SQQQ", "name": "ProShares UltraPro Short QQQ (-3x)",     "category": "3x Inverse",      "group_name": "Leveraged / Inverse", "region": "US"},
    {"symbol": "TBT",  "name": "ProShares UltraShort 20+ Year Treasury", "category": "2x Inverse",      "group_name": "Leveraged / Inverse", "region": "US"},

    # ── Cryptocurrency / Digital Assets ──────────────────────────────────────
    {"symbol": "BITO", "name": "ProShares Bitcoin Strategy ETF",         "category": "Bitcoin Futures", "group_name": "Crypto", "region": "US"},
    {"symbol": "BTF",  "name": "Valkyrie Bitcoin Strategy ETF",          "category": "Bitcoin Futures", "group_name": "Crypto", "region": "US"},
    {"symbol": "BLOK", "name": "Amplify Transformational Data Sharing ETF","category": "Blockchain",    "group_name": "Crypto", "region": "Global"},
]


def get_groups() -> list[str]:
    """Restituisce l'elenco dei gruppi unici."""
    return sorted({e["group_name"] for e in FULL_ETF_CATALOG})


def get_regions() -> list[str]:
    """Restituisce l'elenco delle regioni uniche."""
    return sorted({e["region"] for e in FULL_ETF_CATALOG if e.get("region")})


def seed_catalog_table(db_path: str) -> None:
    """Inserisce il catalogo nella tabella etf_catalog (ignora duplicati)."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    for e in FULL_ETF_CATALOG:
        conn.execute(
            """INSERT OR IGNORE INTO etf_catalog
               (symbol, name, category, group_name, region, currency)
               VALUES (?,?,?,?,?,?)""",
            (e["symbol"], e["name"], e["category"],
             e["group_name"], e.get("region", ""), e.get("currency", "USD")),
        )
    conn.commit()
    conn.close()
