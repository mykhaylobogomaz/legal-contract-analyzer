"""
risk_patterns.py
================
Centralised library of toxic / high-risk clause patterns.
Each entry is a dict with:
    - pattern   : str  – keyword or short phrase (lower-case, regex-safe)
    - category  : str  – human-readable risk category
    - severity  : str  – "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
    - explanation: str – plain-language explanation shown to the user
    - recommendation: str – what the lawyer / client should do

Add new patterns here without touching any other file.
"""

RISK_PATTERNS = [
    # ── FINANCIAL TRAPS ──────────────────────────────────────────────────────
    {
        "pattern": "sole discretion",
        "category": "Unilateral Decision Power",
        "severity": "CRITICAL",
        "explanation": (
            "The counterparty can make key decisions (price changes, "
            "fee adjustments, termination) without your consent or any "
            "objective standard."
        ),
        "recommendation": (
            "Replace with 'mutual agreement' or add a specific, objective "
            "criteria that must be met before this power is exercised."
        ),
    },
    {
        "pattern": "at any time without notice",
        "category": "Unilateral Modification",
        "severity": "CRITICAL",
        "explanation": (
            "The other party can change contract terms, pricing, or "
            "obligations instantly with zero warning to you."
        ),
        "recommendation": (
            "Negotiate a mandatory written notice period (30–90 days) "
            "and a right to exit if changes are material."
        ),
    },
    {
        "pattern": "royalty fee",
        "category": "Ongoing Financial Obligation",
        "severity": "HIGH",
        "explanation": (
            "Royalty fees are recurring charges that continue for the "
            "life of the agreement. Ensure the rate, base, and cap are "
            "explicitly defined."
        ),
        "recommendation": (
            "Verify the fee base (gross vs net revenue), the exact "
            "percentage, any caps, and audit rights to verify calculations."
        ),
    },
    {
        "pattern": "marketing fund",
        "category": "Compulsory Contribution",
        "severity": "HIGH",
        "explanation": (
            "Mandatory marketing fund contributions can be open-ended. "
            "You may have no control over how the money is spent."
        ),
        "recommendation": (
            "Demand a defined spending policy, regular reporting, "
            "and an advisory committee with franchisee representation."
        ),
    },
    {
        "pattern": "non-refundable",
        "category": "Financial Risk",
        "severity": "HIGH",
        "explanation": (
            "Fees or deposits marked non-refundable cannot be recovered "
            "if the deal falls through or the contract is terminated."
        ),
        "recommendation": (
            "Seek partial refund provisions tied to specific milestones "
            "or the counterparty's breach."
        ),
    },
    {
        "pattern": "indemnif",
        "category": "Indemnification",
        "severity": "HIGH",
        "explanation": (
            "Broad indemnification clauses can make you financially "
            "responsible for losses, legal costs, and damages far beyond "
            "what you directly caused."
        ),
        "recommendation": (
            "Limit indemnification to your own gross negligence or "
            "wilful misconduct, and cap the total exposure."
        ),
    },
    {
        "pattern": "liquidated damages",
        "category": "Pre-Set Penalties",
        "severity": "HIGH",
        "explanation": (
            "Pre-agreed penalties can be imposed without proving actual "
            "harm. Verify these amounts are proportionate and reasonable."
        ),
        "recommendation": (
            "Ensure the amounts reflect genuine pre-estimates of loss, "
            "not a disguised penalty which may be unenforceable."
        ),
    },

    # ── CONTROL & AUTONOMY ────────────────────────────────────────────────────
    {
        "pattern": "non-compete",
        "category": "Restraint of Trade",
        "severity": "CRITICAL",
        "explanation": (
            "Non-compete clauses restrict your ability to work in your "
            "industry after the contract ends. Broad clauses can be "
            "commercially crippling."
        ),
        "recommendation": (
            "Negotiate geographic scope, duration (max 12–24 months), "
            "and activity scope. Check local enforceability."
        ),
    },
    {
        "pattern": "exclusive territory",
        "category": "Territory Rights",
        "severity": "MEDIUM",
        "explanation": (
            "Exclusivity clauses must be precisely defined. Vague territory "
            "descriptions can be exploited to allow encroachment."
        ),
        "recommendation": (
            "Define territory by postcode, map exhibit, or population "
            "radius. Include protection against online sales encroachment."
        ),
    },
    {
        "pattern": "right of first refusal",
        "category": "Exit Restriction",
        "severity": "MEDIUM",
        "explanation": (
            "This clause can delay or devalue your ability to sell your "
            "business interest by giving the other party priority purchase "
            "rights."
        ),
        "recommendation": (
            "Set a strict time window (e.g. 30 days) for the right to be "
            "exercised, after which you are free to sell to any third party."
        ),
    },
    {
        "pattern": "assign",
        "category": "Assignment Rights",
        "severity": "MEDIUM",
        "explanation": (
            "Assignment clauses control whether you can transfer the "
            "contract. One-sided restrictions (only the counterparty may "
            "assign) create imbalance."
        ),
        "recommendation": (
            "Ensure assignment rights are mutual or, if restricted, "
            "approval cannot be unreasonably withheld."
        ),
    },

    # ── TERMINATION TRAPS ─────────────────────────────────────────────────────
    {
        "pattern": "terminate immediately",
        "category": "Instant Termination",
        "severity": "CRITICAL",
        "explanation": (
            "Immediate termination without a cure period can destroy your "
            "business overnight based on minor or disputed breaches."
        ),
        "recommendation": (
            "Require a written notice of breach and a reasonable cure "
            "period (14–30 days) before termination takes effect."
        ),
    },
    {
        "pattern": "without cause",
        "category": "Arbitrary Termination",
        "severity": "CRITICAL",
        "explanation": (
            "'Without cause' termination allows the counterparty to end "
            "the agreement for any reason — or no reason at all."
        ),
        "recommendation": (
            "Remove or limit 'without cause' termination rights. If "
            "retained, require substantial compensation to offset your losses."
        ),
    },
    {
        "pattern": "automatic renewal",
        "category": "Lock-In Risk",
        "severity": "HIGH",
        "explanation": (
            "Auto-renewal clauses can lock you into a new term with "
            "unfavourable conditions if you miss the opt-out deadline."
        ),
        "recommendation": (
            "Set calendar reminders 90 days before the opt-out window. "
            "Negotiate a longer notice window and written confirmation."
        ),
    },
    {
        "pattern": "cure period",
        "category": "Breach Remedy Window",
        "severity": "MEDIUM",
        "explanation": (
            "The presence or absence of a cure period determines how much "
            "time you have to fix a breach before facing termination."
        ),
        "recommendation": (
            "Ensure the cure period is at least 14–30 days for all "
            "material breaches, with written notice requirements."
        ),
    },

    # ── INTELLECTUAL PROPERTY ─────────────────────────────────────────────────
    {
        "pattern": "intellectual property",
        "category": "IP Rights",
        "severity": "HIGH",
        "explanation": (
            "IP clauses define who owns innovations, branding, data, "
            "and know-how created during the relationship. "
            "Blanket assignment of your IP is extremely risky."
        ),
        "recommendation": (
            "Carve out pre-existing IP. Ensure ownership of any "
            "independently developed IP remains with you."
        ),
    },
    {
        "pattern": "confidential",
        "category": "Confidentiality",
        "severity": "MEDIUM",
        "explanation": (
            "Overly broad confidentiality clauses can prevent you from "
            "seeking legal advice, disclosing breaches, or even mentioning "
            "the contract's existence."
        ),
        "recommendation": (
            "Carve out disclosures required by law, regulatory bodies, "
            "legal advisers, and lenders."
        ),
    },

    # ── DISPUTE RESOLUTION ────────────────────────────────────────────────────
    {
        "pattern": "arbitration",
        "category": "Dispute Resolution",
        "severity": "MEDIUM",
        "explanation": (
            "Mandatory arbitration waives your right to a jury trial "
            "and can limit discovery. Arbitration favours repeat players "
            "(usually the franchisor)."
        ),
        "recommendation": (
            "Check the arbitration venue, governing rules, and seat. "
            "Negotiate the right to seek emergency court injunctions."
        ),
    },
    {
        "pattern": "governing law",
        "category": "Jurisdiction",
        "severity": "MEDIUM",
        "explanation": (
            "A distant governing law or jurisdiction forces you to litigate "
            "far from home under unfamiliar rules — raising your costs "
            "dramatically."
        ),
        "recommendation": (
            "Negotiate for your local jurisdiction or, at minimum, "
            "the jurisdiction where you primarily operate."
        ),
    },
    {
        "pattern": "class action waiver",
        "category": "Legal Rights Waiver",
        "severity": "HIGH",
        "explanation": (
            "This clause prevents you from joining a class action lawsuit, "
            "isolating you and making it economically unviable to pursue "
            "small individual claims."
        ),
        "recommendation": (
            "Contest class action waivers, particularly for consumer "
            "or franchise agreements; enforceability varies by jurisdiction."
        ),
    },

    # ── MISCELLANEOUS HIGH-RISK ───────────────────────────────────────────────
    {
        "pattern": "as is",
        "category": "Warranty Disclaimer",
        "severity": "HIGH",
        "explanation": (
            "'As is' language strips all warranties — you accept the asset "
            "or system in whatever condition it exists, with no recourse "
            "for hidden defects."
        ),
        "recommendation": (
            "Conduct thorough due diligence before signing. "
            "Negotiate specific warranties for material representations."
        ),
    },
    {
        "pattern": "force majeure",
        "category": "Force Majeure",
        "severity": "MEDIUM",
        "explanation": (
            "Force majeure clauses excuse performance during unforeseen "
            "events. One-sided or overly broad definitions can excuse "
            "the counterparty while you remain bound."
        ),
        "recommendation": (
            "Ensure force majeure is mutual, narrowly defined, "
            "and includes a termination right if the event exceeds "
            "a set duration (e.g. 90 days)."
        ),
    },
    {
        "pattern": "entire agreement",
        "category": "Prior Representations",
        "severity": "LOW",
        "explanation": (
            "This clause voids all pre-contractual promises and "
            "representations not captured in the written agreement. "
            "Verbal assurances from sales meetings are legally erased."
        ),
        "recommendation": (
            "Ensure every material representation made during negotiations "
            "is captured in writing within the contract or a schedule."
        ),
    },
    {
        "pattern": "waiver",
        "category": "Rights Waiver",
        "severity": "LOW",
        "explanation": (
            "Waiver clauses can erode your rights over time if you fail "
            "to enforce them consistently."
        ),
        "recommendation": (
            "Include a 'non-waiver' clause stating that failure to enforce "
            "a right does not constitute a permanent waiver of that right."
        ),
    },
]

SEVERITY_COLORS = {
    "CRITICAL": "#e74c3c",
    "HIGH":     "#e67e22",
    "MEDIUM":   "#f1c40f",
    "LOW":      "#3498db",
}

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
