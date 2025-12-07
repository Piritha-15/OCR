import re
from datetime import datetime


def fix_words(s):
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()


def parse_fields(text):
    data = {}

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    full_lower = text.lower()

    addr1 = None
    addr2 = None
    addr_candidates = []

    for line in lines:
        l = line.strip()
        ll = l.lower()

        # ---------- FIRST NAME (ONLY IF CLEAR LABEL) ----------
        if "first" in ll and "name" in ll:
            value = l.split(":", 1)[-1]
            data["first_name"] = fix_words(value)
            continue

        # ---------- MIDDLE NAME ----------
        if ("middle" in ll and "name" in ll) or ("midde" in ll and "nove" in ll):
            value = l.split(":", 1)[-1]
            data["middle_name"] = fix_words(value)
            continue

        # ---------- LAST NAME ----------
        if "last" in ll and "name" in ll:
            value = re.sub(r"(?i)last\s*name", "", l)
            value = value.replace(":", "")
            value = fix_words(value)

            # Join broken OCR words: "Sum mer" → "Summer"
            parts = value.split()
            if len(parts) == 2:
                value = "".join(parts)

            data["last_name"] = value
            continue

        # ---------- GENDER ----------
        if "gender" in ll or "geen" in ll:
            v = l.split(":", 1)[-1].lower()
            if "female" in v or "fema" in v:
                data["gender"] = "Female"
            elif "male" in v:
                data["gender"] = "Male"
            continue

        # ---------- DOB + AGE ----------
        if ("date" in ll and "birth" in ll) or "dob" in ll:
            m = re.search(r"\d{2}[-/]\d{2}[-/]\d{4}", l)
            if m:
                dob = m.group()
                data["dob"] = dob
                try:
                    d = datetime.strptime(dob, "%d-%m-%Y")
                    today = datetime.today()
                    age = today.year - d.year - (
                        (today.month, today.day) < (d.month, d.day)
                    )
                    data["age"] = age
                except:
                    pass
            continue

        # ---------- PHONE ----------
        if "phone" in ll or "phrowe" in ll:
            m = re.search(r"\d{10}", l)
            if m:
                data["phone"] = m.group()
            continue

        # ---------- EMAIL ----------
        if "email" in ll or "emmett" in ll or "@" in l:
            candidate = l.split(":", 1)[-1]
            candidate = candidate.replace(" ", "")
            candidate = candidate.replace("-", ".")
            candidate = re.sub(r"(?i)cow$", "com", candidate)

            m = re.search(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                candidate
            )
            if m:
                data["email"] = m.group()
            continue

        # ---------- PINCODE ----------
        if "pin" in ll:
            m = re.search(r"\d{6}", l)
            if m:
                data["pincode"] = m.group()
            continue

        # ---------- STATE ----------
        if "state" in ll:
            value = l.split(":", 1)[-1]
            data["state"] = fix_words(value)
            continue

        # ---------- ADDRESS LINE 1 ----------
        if ("address" in ll or "addross" in ll) and (
            "line1" in ll or "line 1" in ll or "linet" in ll
        ):
            addr1 = l.split(":", 1)[-1].strip()
            continue

        # ---------- ADDRESS LINE 2 ----------
        if ("address" in ll or "adobwss" in ll) and (
            "line2" in ll or "line 2" in ll
        ):
            addr2 = l.split(":", 1)[-1].strip()
            continue

        # ---------- GENERIC ADDRESS CANDIDATES (fallback) ----------
        if any(k in ll for k in ["road", "street", "layout", "#", "lasyoud", "hsr"]):
            if not any(bad in ll for bad in ["pin", "state", "phone", "email", "name", "gender", "date", "birth"]):
                addr_candidates.append(l.split(":", 1)[-1].strip())

    # ---------- COMBINE ADDRESS ----------
    addr_parts = []
    if addr1:
        addr_parts.append(addr1)
    if addr2:
        addr_parts.append(addr2)
    for c in addr_candidates:
        if c and c not in addr_parts:
            addr_parts.append(c)

    if addr_parts:
        data["address"] = fix_words(", ".join(addr_parts))

    # ---------- COUNTRY ----------
    data["country"] = "India"

    # ---------- FIRST NAME FALLBACK ----------
    if "first_name" not in data:
        if "middle_name" in data:
            data["first_name"] = data["middle_name"]
        elif "email" in data:
            local = data["email"].split("@")[0]
            local = re.split(r"[._]", local)[0]
            data["first_name"] = local.capitalize()

    return data
