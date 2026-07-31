"""
Generate professional dark-themed PDFs for Shawan Tech Solutions.
Pure Python stdlib — no external dependencies.
"""
import os

# ─── Color palette (R G B as PDF 0-1 strings) ────────────────────────────────
BG    = "0.039 0.059 0.098"   # #0a0f19 – dark navy page bg
CARD  = "0.055 0.078 0.133"   # #0e1422 – card bg
BAR   = "0.024 0.031 0.059"   # #06080f – stats bar
BLUE  = "0.149 0.471 0.961"   # #2678f5 – primary blue
GREEN = "0.118 0.784 0.502"   # #1ec880 – green accent
PURP  = "0.549 0.361 0.961"   # #8c5cf5 – purple accent
WHITE = "1 1 1"
LGRAY = "0.698 0.749 0.824"   # #b2bfd2
MUTED = "0.408 0.478 0.565"   # #687990
DIVID = "0.122 0.153 0.235"   # subtle row divider

def esc(t):
    return t.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

def T(x, y, size, txt, bold=False, color=WHITE, spacing=0):
    fn = "F2" if bold else "F1"
    tc = f"{spacing:.2f} Tc\n" if spacing else ""
    return f"{color} rg\nBT\n/{fn} {size} Tf\n{tc}{x:.1f} {y:.1f} Td\n({esc(txt)}) Tj\nET\n"

def RECT(x, y, w, h, fill=BG, stroke=None, sw=1.0):
    ops = f"{fill} rg\n"
    if stroke:
        ops += f"{stroke} RG\n{sw:.2f} w\n"
        ops += f"{x:.1f} {y:.1f} {w:.1f} {h:.1f} re\nB\n"
    else:
        ops += f"{x:.1f} {y:.1f} {w:.1f} {h:.1f} re\nf\n"
    return ops

def LINE(x1, y1, x2, y2, color=BLUE, w=1.5):
    return f"{color} RG\n{w:.2f} w\n{x1:.1f} {y1:.1f} m\n{x2:.1f} {y2:.1f} l\nS\n"

def circle_path(cx, cy, r):
    k = 0.5523 * r
    return (f"{cx+r:.2f} {cy:.2f} m "
            f"{cx+r:.2f} {cy+k:.2f} {cx+k:.2f} {cy+r:.2f} {cx:.2f} {cy+r:.2f} c "
            f"{cx-k:.2f} {cy+r:.2f} {cx-r:.2f} {cy+k:.2f} {cx-r:.2f} {cy:.2f} c "
            f"{cx-r:.2f} {cy-k:.2f} {cx-k:.2f} {cy-r:.2f} {cx:.2f} {cy-r:.2f} c "
            f"{cx+k:.2f} {cy-r:.2f} {cx+r:.2f} {cy-k:.2f} {cx+r:.2f} {cy:.2f} c h ")

def CIRCLE(cx, cy, r, fill=None, stroke=None, sw=2.0):
    ops = ""
    if fill:   ops += f"{fill} rg\n"
    if stroke: ops += f"{stroke} RG\n{sw:.2f} w\n"
    ops += circle_path(cx, cy, r)
    if fill and stroke: ops += "B\n"
    elif fill:          ops += "f\n"
    elif stroke:        ops += "S\n"
    return ops

def rrect_path(x, y, w, h, r=4):
    k = 0.5523 * r
    return (f"{x+r:.1f} {y:.1f} m {x+w-r:.1f} {y:.1f} l "
            f"{x+w-r:.1f} {y:.1f} {x+w:.1f} {y:.1f} {x+w:.1f} {y+r:.1f} c "
            f"{x+w:.1f} {y+h-r:.1f} l "
            f"{x+w:.1f} {y+h-r:.1f} {x+w:.1f} {y+h:.1f} {x+w-r:.1f} {y+h:.1f} c "
            f"{x+r:.1f} {y+h:.1f} l "
            f"{x+r:.1f} {y+h:.1f} {x:.1f} {y+h:.1f} {x:.1f} {y+h-r:.1f} c "
            f"{x:.1f} {y+r:.1f} l {x:.1f} {y+r:.1f} {x:.1f} {y:.1f} {x+r:.1f} {y:.1f} c h ")

def PILL(x, y, w, h, txt, accent=BLUE, r=4):
    ops = f"{BG} rg\n{accent} RG\n0.8 w\n{rrect_path(x, y, w, h, r)}B\n"
    ops += T(x + 9, y + h/2 - 3.5, 7.5, txt, color=accent)
    return ops

def STAT(x, y, number, label, accent=BLUE):
    ops = T(x, y + 28, 30, number, bold=True, color=accent)
    ops += T(x, y + 8,  8.5, label, color=LGRAY)
    return ops

def BULLET(x, y, title, desc, accent=BLUE):
    ops  = RECT(x, y + 5, 4, 10, accent)
    ops += T(x + 12, y + 4, 10.5, title, bold=True, color=WHITE)
    ops += T(x + 12, y - 10, 8.5, desc, color=LGRAY)
    return ops

def page_bg(accent=BLUE):
    ops  = RECT(0, 0, 595, 842, BG)
    ops += RECT(0, 0, 6, 842, accent)
    return ops

def inner_header(label, page_info="", accent=BLUE):
    ops  = page_bg(accent)
    ops += RECT(0, 806, 595, 36, CARD)
    ops += T(72, 816, 7.5, label, bold=True, color=accent, spacing=0.5)
    if page_info:
        ops += T(490, 816, 7, page_info, color=MUTED)
    ops += LINE(72, 804, 523, 804, MUTED, 0.4)
    return ops

def row_divider(x, y, w=451):
    return LINE(x, y, x + w, y, DIVID, 0.4)

def cover_deco(accent=BLUE):
    """Logo circle + 3 decorative circles."""
    ops  = CIRCLE(130, 733, 47, fill=CARD, stroke=accent, sw=2.0)
    ops += CIRCLE(149, 745, 12, fill=accent)
    ops += T(110, 726, 17, "ST", bold=True, color=WHITE)
    ops += CIRCLE(455, 744, 43, fill="0.055 0.075 0.125", stroke=accent, sw=1.5)
    ops += CIRCLE(498, 759, 43, fill=CARD,                stroke=accent, sw=1.5)
    ops += CIRCLE(477, 722, 38, fill="0.059 0.082 0.137", stroke=accent, sw=1.5)
    return ops

def cover_stats(items, accent=BLUE):
    """4-column stats bar at page bottom."""
    ops  = RECT(0, 0, 595, 128, BAR)
    ops += LINE(0, 128, 595, 128, DIVID, 0.5)
    cw = 595 / 4
    for i, (num, lbl) in enumerate(items):
        ops += STAT(28 + i * cw, 50, num, lbl, accent)
        if i < 3:
            ops += LINE(28 + (i+1)*cw - 6, 58, 28 + (i+1)*cw - 6, 110, DIVID, 0.4)
    return ops


# ═══════════════════════════════════════════════════════════════════
#  COMPANY PROFILE
# ═══════════════════════════════════════════════════════════════════

def cp_cover():
    ops  = page_bg(BLUE)
    ops += cover_deco(BLUE)
    # Subtle grid dots decoration
    for gx in range(350, 560, 22):
        for gy in range(155, 370, 22):
            ops += CIRCLE(gx, gy, 1.2, fill="0.149 0.471 0.961")
    # Content block
    ops += T(72, 648, 8,  "COMPANY PROFILE", bold=True, color=BLUE, spacing=1.8)
    ops += T(72, 572, 54, "Shawan Tech",     bold=True, color=WHITE)
    ops += T(72, 512, 50, "Solutions",                  color=LGRAY)
    ops += T(72, 470, 10.5, "Enterprise IT Infrastructure, Cloud, Cyber Security", color=MUTED)
    ops += T(72, 454, 10.5, "& Data Recovery Solutions",                           color=MUTED)
    ops += LINE(72, 435, 523, 435, BLUE, 1.5)
    bx = 72
    for lbl, w in [("ISO Certified",83),("24/7 Support",75),("AMC Services",80),("Chennai Based",84)]:
        ops += PILL(bx, 408, w, 22, lbl, BLUE)
        bx += w + 8
    ops += cover_stats([("150+","Projects"),("100+","Clients"),("6+","Years"),("24x7","Uptime")], BLUE)
    return ops

def cp_page2():
    ops  = inner_header("COMPANY PROFILE  /  OUR SERVICES & INDUSTRIES", "Page 2 of 3", BLUE)
    y = 758
    ops += T(72, y, 16, "Core Services", bold=True, color=WHITE)
    ops += LINE(72, y - 8, 523, y - 8, BLUE, 0.8)
    y -= 36
    services = [
        ("Enterprise Networking",   "LAN/WAN design, Wi-Fi 6, VPN gateways, structured cabling, managed switches."),
        ("Cloud Infrastructure",    "Microsoft 365, Azure migration, hybrid cloud, Google Workspace, cloud backup."),
        ("Cybersecurity",           "Fortinet / Sophos / Cisco NGFW, endpoint protection, vulnerability assessments."),
        ("Data Recovery",           "Forensic HDD/SSD/RAID recovery. 92%+ success rate. Emergency 24x7 hotline."),
        ("AMC Support",             "3-tier SLA plans (Basic, Standard, Enterprise). On-site + remote coverage."),
        ("Hardware Sales & Rental", "Refurbished laptops, desktops, printers, workstations and networking gear."),
        ("Genuine Spare Parts",     "OEM-sourced RAM, SSDs, batteries, keyboards and peripherals."),
    ]
    for title, desc in services:
        ops += BULLET(72, y, title, desc, BLUE)
        y -= 48
    y -= 14
    ops += T(72, y, 16, "Industries We Serve", bold=True, color=WHITE)
    ops += LINE(72, y - 8, 523, y - 8, BLUE, 0.8)
    y -= 30
    left  = ["Healthcare & Hospitals","Education & Universities","Manufacturing & Logistics","Financial Services"]
    right = ["Retail & Hospitality","Government Agencies","SMEs & Startups","Legal & Consulting Firms"]
    for j in range(4):
        ops += RECT(72,  y - j*22 + 6, 4, 8, BLUE)
        ops += T(82,  y - j*22, 9, left[j],  color=LGRAY)
        ops += RECT(310, y - j*22 + 6, 4, 8, BLUE)
        ops += T(320, y - j*22, 9, right[j], color=LGRAY)
    return ops

def cp_page3():
    ops  = inner_header("COMPANY PROFILE  /  WHY US & CONTACT", "Page 3 of 3", BLUE)
    y = 758
    ops += T(72, y, 16, "Why Choose Shawan Tech?", bold=True, color=WHITE)
    ops += LINE(72, y - 8, 523, y - 8, BLUE, 0.8)
    y -= 36
    for title, desc in [
        ("ISO-Aligned Processes",   "Workflows conforming to ISO/IEC 27001 and ITIL service management frameworks."),
        ("Certified Engineers",     "CCNA, CompTIA Network+, CEH, and Microsoft Azure certified engineering team."),
        ("24x7 Emergency Support",  "Round-the-clock support desk for critical incidents, data loss and outages."),
        ("Transparent Pricing",     "Fixed-fee AMC contracts. Quote-based projects. Zero hidden charges guaranteed."),
        ("Quality-Assured Hardware","47-point QC inspection on every refurbished unit before dispatch to client."),
    ]:
        ops += BULLET(72, y, title, desc, BLUE)
        y -= 50
    y -= 16
    ops += T(72, y, 13, "Technology Partners", bold=True, color=WHITE)
    ops += LINE(72, y - 7, 523, y - 7, BLUE, 0.8)
    y -= 26
    ops += T(72, y, 9, "Cisco  |  Fortinet  |  HP  |  Dell  |  Lenovo  |  Microsoft  |  Sophos  |  Seagate  |  WD  |  Kingston", color=LGRAY)
    y -= 44
    ops += T(72, y, 13, "Get In Touch", bold=True, color=WHITE)
    ops += LINE(72, y - 7, 523, y - 7, BLUE, 0.8)
    y -= 28
    for lbl, val in [("Email","shawan@shawanreddy.com"),("Phone","+91 97912 71479"),
                     ("Website","karthik.shawanreddy.com")]:
        ops += RECT(72, y + 3, 4, 10, BLUE)
        ops += T(82,  y, 9.5, f"{lbl}:", bold=True, color=MUTED)
        ops += T(82 + 80, y, 9.5, val, color=WHITE)
        y -= 24
    y -= 18
    bw, bh = 451, 62
    ops += RECT(72, y - 40, bw, bh, CARD, stroke=BLUE, sw=0.5)
    ops += T(92, y + 2,  10.5, "Schedule a FREE IT Infrastructure Assessment", bold=True, color=WHITE)
    ops += T(92, y - 14, 9,    "Contact us at shawan@shawanreddy.com   |   +91 97912 71479", color=LGRAY)
    return ops


# ═══════════════════════════════════════════════════════════════════
#  AMC SERVICE SHEET
# ═══════════════════════════════════════════════════════════════════

def amc_cover():
    ops  = page_bg(GREEN)
    ops += cover_deco(GREEN)
    for gx in range(350, 560, 22):
        for gy in range(155, 370, 22):
            ops += CIRCLE(gx, gy, 1.2, fill=GREEN)
    ops += T(72, 648, 8,  "SERVICE DOCUMENTATION", bold=True, color=GREEN, spacing=1.8)
    ops += T(72, 572, 46, "Annual Maintenance",    bold=True, color=WHITE)
    ops += T(72, 520, 46, "Contract Plans",                   color=LGRAY)
    ops += T(72, 474, 10.5, "Predictable IT maintenance costs. Guaranteed SLA response times.", color=MUTED)
    ops += T(72, 458, 10.5, "Certified engineers. On-site support. Hardware coverage.",         color=MUTED)
    ops += LINE(72, 438, 523, 438, GREEN, 1.5)
    bx = 72
    for lbl, w in [("Basic Plan",72),("Standard Plan",86),("Enterprise Plan",95),("24x7 SLA",66)]:
        ops += PILL(bx, 410, w, 22, lbl, GREEN)
        bx += w + 8
    ops += cover_stats([("3","Tier Plans"),("4h","Max SLA"),("365","Days Cover"),("100%","Hardware")], GREEN)
    return ops

def amc_page2():
    ops  = inner_header("ANNUAL MAINTENANCE CONTRACT  /  PLAN DETAILS", "Page 2 of 2", GREEN)
    # 3 tier cards
    tiers = [
        ("BASIC",      "Rs. 2,999/mo",  "Next Business Day",   "2 visits / quarter",   "Labour only",          BLUE),
        ("STANDARD",   "Rs. 5,999/mo",  "4-Hour SLA",          "Monthly + emergency",  "Parts at cost",        GREEN),
        ("ENTERPRISE", "Rs. 12,999/mo", "2-Hour SLA  24x7",    "Dedicated engineer",   "All parts covered",    PURP),
    ]
    tw, th = 158, 192
    for i, (name, price, sla, visits, hw, col) in enumerate(tiers):
        bx = 50 + i * (tw + 10)
        by = 610
        ops += RECT(bx, by, tw, th, CARD, stroke=col, sw=1.2)
        ops += T(bx + 10, by + th - 24, 9, name, bold=True, color=col, spacing=0.8)
        ops += LINE(bx, by + th - 32, bx + tw, by + th - 32, col, 0.5)
        ops += T(bx + 10, by + th - 52, 13, price, bold=True, color=WHITE)
        ops += T(bx + 10, by + th - 74, 7.5, "Response SLA:", bold=True, color=MUTED)
        ops += T(bx + 10, by + th - 88, 8.5, sla, color=WHITE)
        ops += T(bx + 10, by + th - 108, 7.5, "On-site visits:", bold=True, color=MUTED)
        ops += T(bx + 10, by + th - 122, 8.5, visits, color=WHITE)
        ops += T(bx + 10, by + th - 142, 7.5, "Hardware:", bold=True, color=MUTED)
        ops += T(bx + 10, by + th - 156, 8.5, hw, color=WHITE)
        # coloured dot
        ops += CIRCLE(bx + tw - 14, by + th - 18, 6, fill=col)
    y = 586
    ops += T(72, y, 13, "What's Covered", bold=True, color=WHITE)
    ops += LINE(72, y - 7, 523, y - 7, GREEN, 0.8)
    y -= 28
    for item in [
        "Hardware maintenance: desktops, laptops, servers, printers, UPS, CCTV, access control",
        "Software support: OS, antivirus patching, MS 365 admin, ERP / CRM assistance",
        "Network: router/switch config, firewall rule management, VPN monitoring, Wi-Fi tuning",
        "Data backup configuration, cloud integration monitoring and restore drills",
        "Cybersecurity: quarterly vulnerability scan (Standard & Enterprise tiers)",
        "Data recovery assistance at discounted rates for all active AMC clients",
    ]:
        ops += RECT(72, y + 5, 4, 8, GREEN)
        ops += T(82, y, 9, item, color=LGRAY)
        y -= 22
    y -= 24
    bw, bh = 451, 62
    ops += RECT(72, y - 40, bw, bh, CARD, stroke=GREEN, sw=0.5)
    ops += T(92, y + 2,  10.5, "Enrol Today — Contact Us", bold=True, color=WHITE)
    ops += T(92, y - 14, 9,    "shawan@shawanreddy.com   |   +91 97912 71479   |   karthik.shawanreddy.com", color=LGRAY)
    return ops


# ═══════════════════════════════════════════════════════════════════
#  PRODUCT CATALOG
# ═══════════════════════════════════════════════════════════════════

def cat_cover():
    ops  = page_bg(PURP)
    ops += cover_deco(PURP)
    for gx in range(350, 560, 22):
        for gy in range(155, 370, 22):
            ops += CIRCLE(gx, gy, 1.2, fill=PURP)
    ops += T(72, 648, 8,  "PRODUCT CATALOG", bold=True, color=PURP, spacing=1.8)
    ops += T(72, 572, 48, "Hardware, Rentals", bold=True, color=WHITE)
    ops += T(72, 518, 48, "& IT Services",               color=LGRAY)
    ops += T(72, 472, 10.5, "Refurbished laptops, desktops, printer rentals, networking gear,", color=MUTED)
    ops += T(72, 456, 10.5, "genuine spare parts and managed IT services with clear pricing.",   color=MUTED)
    ops += LINE(72, 437, 523, 437, PURP, 1.5)
    bx = 72
    for lbl, w in [("Laptops & Desktops",115),("Printer Rentals",93),("Networking",82),("Spare Parts",80)]:
        ops += PILL(bx, 410, w, 22, lbl, PURP)
        bx += w + 8
    ops += cover_stats([("200+","Products"),("3mo","Warranty"),("47pt","QC Check"),("24x7","Support")], PURP)
    return ops

def cat_page2():
    ops  = inner_header("PRODUCT CATALOG  /  LAPTOPS & PRINTER RENTALS", "Page 2 of 3", PURP)
    y = 758
    ops += T(72, y, 14, "Refurbished Laptops", bold=True, color=WHITE)
    ops += LINE(72, y - 8, 523, y - 8, PURP, 0.8)
    y -= 32
    for model, spec, price in [
        ("Dell Latitude E5470",  "Core i5-6300U  |  8 GB RAM  |  256 GB SSD  |  14\" FHD  |  Win 10 Pro  |  Grade A",    "Rs. 18,500   Rental: Rs. 1,200 / month"),
        ("HP EliteBook 840 G3",  "Core i5-6300U  |  8 GB RAM  |  512 GB SSD  |  14\" FHD  |  Win 11 Pro  |  Grade A+",   "Rs. 22,000   Rental: Rs. 1,500 / month"),
        ("Lenovo ThinkPad T470", "Core i7-7600U  |  16 GB RAM  |  512 GB SSD  |  14\" FHD  |  Win 11 Pro  |  Grade A",   "Rs. 28,000   Rental: Rs. 1,800 / month"),
        ("HP ProDesk 600 G3",    "Core i7-7700  |  16 GB RAM  |  512 GB SSD  |  Desktop  |  Win 11 Pro  |  Grade A",      "Rs. 21,000"),
        ("Dell OptiPlex 7050",   "Core i5-7500  |  8 GB RAM  |  256 GB SSD  |  SFF  |  Win 10 Pro  |  Grade A",           "Rs. 14,500"),
    ]:
        ops += T(72,  y,      11, model, bold=True, color=WHITE)
        ops += T(72,  y - 14, 8.5, spec,  color=LGRAY)
        ops += T(72,  y - 26, 9,   price, bold=True, color=PURP)
        ops += row_divider(72, y - 36)
        y -= 54
    y -= 8
    ops += T(72, y, 14, "Printer Rentals", bold=True, color=WHITE)
    ops += LINE(72, y - 8, 523, y - 8, PURP, 0.8)
    y -= 32
    for model, spec, price in [
        ("HP LaserJet Pro M428fdw",      "Print / Copy / Scan / Fax  |  35 ppm  |  Duplex  |  Wi-Fi  |  A4",       "Rs. 1,800/mo  (min 12 months, toner included)"),
        ("Canon imageRUNNER 2206N",      "Print / Copy / Scan  |  22 ppm  |  Duplex  |  Network  |  A3 capable",   "Rs. 2,200/mo  (min 12 months, toner included)"),
        ("Xerox WorkCentre 6515 Colour", "Colour Laser  |  Print/Copy/Scan/Fax  |  35 ppm  |  Wi-Fi  |  A4",       "Rs. 3,500/mo  (min 12 months, toner included)"),
    ]:
        ops += T(72, y,      11, model, bold=True, color=WHITE)
        ops += T(72, y - 14, 8.5, spec,  color=LGRAY)
        ops += T(72, y - 26, 9,   price, bold=True, color=PURP)
        ops += row_divider(72, y - 36)
        y -= 54
    return ops

def cat_page3():
    ops  = inner_header("PRODUCT CATALOG  /  NETWORKING, SPARE PARTS & SERVICES", "Page 3 of 3", PURP)
    y = 758
    ops += T(72, y, 14, "Networking Equipment", bold=True, color=WHITE)
    ops += LINE(72, y - 8, 523, y - 8, PURP, 0.8)
    y -= 32
    for model, spec, price in [
        ("Cisco 2960-X 24-Port PoE Switch",      "24x GbE PoE+  |  4x SFP  |  IOS  |  Refurbished Grade A",                  "Rs. 32,000"),
        ("Fortinet FortiGate 60F NGFW",           "10 Gbps throughput  |  SSL inspection  |  UTM  |  New unit",                "Rs. 45,000  (licensing separate)"),
        ("TP-Link EAP670 Wi-Fi 6 Access Point",  "AX3000  |  2.4 + 5 GHz  |  PoE  |  Omada SDN managed  |  New unit",        "Rs. 8,500 per unit"),
        ("Ubiquiti UniFi US-24-250W PoE Switch", "24x GbE PoE+  |  250 W budget  |  2x SFP  |  Refurbished Grade A",         "Rs. 28,000"),
    ]:
        ops += T(72, y,      11, model, bold=True, color=WHITE)
        ops += T(72, y - 14, 8.5, spec,  color=LGRAY)
        ops += T(72, y - 26, 9,   price, bold=True, color=PURP)
        ops += row_divider(72, y - 36)
        y -= 54
    y -= 8
    ops += T(72, y, 14, "IT Services & Spare Parts", bold=True, color=WHITE)
    ops += LINE(72, y - 8, 523, y - 8, PURP, 0.8)
    y -= 28
    left_col  = [("OS Reinstall","Rs. 500"),("Virus Removal","Rs. 600"),("RAM Upgrade (labour)","Rs. 300"),
                 ("SSD Upgrade (labour)","Rs. 350"),("Motherboard Diagnosis","Rs. 800"),("Network Point Install","Rs. 1,200")]
    right_col = [("256 GB SATA SSD","Rs. 2,800"),("512 GB SATA SSD","Rs. 4,500"),("8 GB DDR4 SODIMM","Rs. 2,200"),
                 ("16 GB DDR4 SODIMM","Rs. 4,000"),("Laptop Battery","Rs. 1,800+"),("AC Adapter / Brick","Rs. 700+")]
    for j, ((ls, lp), (rs, rp)) in enumerate(zip(left_col, right_col)):
        ry = y - j * 22
        ops += RECT(72,  ry + 4, 3, 8, PURP)
        ops += T(80,  ry, 8.5, ls, color=LGRAY)
        ops += T(230, ry, 8.5, lp, bold=True, color=WHITE)
        ops += RECT(310, ry + 4, 3, 8, PURP)
        ops += T(318, ry, 8.5, rs, color=LGRAY)
        ops += T(445, ry, 8.5, rp, bold=True, color=WHITE)
    y -= len(left_col) * 22 + 28
    ops += T(72, y, 10, "Data Recovery:", bold=True, color=WHITE)
    ops += T(72, y - 14, 9, "HDD / SSD Logical: Rs. 2,000-8,000   RAID Array: Rs. 12,000-40,000   USB / Flash: Rs. 1,500-5,000", color=LGRAY)
    y -= 54
    bw, bh = 451, 62
    ops += RECT(72, y - 40, bw, bh, CARD, stroke=PURP, sw=0.5)
    ops += T(92, y + 2,  10.5, "Place an Order / Request a Quote", bold=True, color=WHITE)
    ops += T(92, y - 14, 9,    "shawan@shawanreddy.com   |   +91 97912 71479   |   karthik.shawanreddy.com", color=LGRAY)
    return ops


# ═══════════════════════════════════════════════════════════════════
#  PDF FILE BUILDER
# ═══════════════════════════════════════════════════════════════════

def build_pdf(filename, page_streams, W=595, H=842):
    np = len(page_streams)
    font_reg  = 3 + 2 * np
    font_bold = 4 + 2 * np
    page_nums = list(range(3, 3 + np))
    cont_nums = list(range(3 + np, 3 + 2 * np))

    body = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
    parts, offsets = [body], {}
    pos = len(body)

    def wobj(num, raw):
        nonlocal pos
        chunk = f"{num} 0 obj\n".encode() + raw + b"\nendobj\n"
        offsets[num] = pos
        parts.append(chunk)
        pos += len(chunk)

    wobj(1, b"<< /Type /Catalog /Pages 2 0 R >>")
    kids = " ".join(f"{n} 0 R" for n in page_nums)
    wobj(2, f"<< /Type /Pages /Kids [{kids}] /Count {np} >>".encode())

    for pn, cn, stream in zip(page_nums, cont_nums, page_streams):
        sb = stream.encode("latin-1", errors="replace")
        wobj(pn, (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {W} {H}] "
            f"/Contents {cn} 0 R "
            f"/Resources << /Font << /F1 {font_reg} 0 R /F2 {font_bold} 0 R >> >> >>"
        ).encode())
        wobj(cn, f"<< /Length {len(sb)} >>\nstream\n".encode() + sb + b"\nendstream")

    wobj(font_reg,  b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    wobj(font_bold, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")

    total = font_bold + 1
    xref_pos = pos
    parts.append(f"xref\n0 {total}\n0000000000 65535 f \n".encode())
    for i in range(1, total):
        parts.append(f"{offsets.get(i, 0):010d} 00000 n \n".encode())
    parts.append(f"trailer\n<< /Size {total} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode())

    with open(filename, "wb") as f:
        for p in parts:
            f.write(p)
    size = os.path.getsize(filename)
    print(f"  Created: {filename}  ({size:,} bytes)")


# ─── Generate ────────────────────────────────────────────────────
os.makedirs("downloads", exist_ok=True)
print("Generating professional PDFs...")

build_pdf("downloads/Shawan-Tech-Company-Profile.pdf", [cp_cover(), cp_page2(), cp_page3()])
build_pdf("downloads/Shawan-Tech-AMC-Service-Sheet.pdf", [amc_cover(), amc_page2()])
build_pdf("downloads/Shawan-Tech-Product-Catalog.pdf",  [cat_cover(), cat_page2(), cat_page3()])

print("Done.")
