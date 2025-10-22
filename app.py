# Streamlit Risk Questionnaire (Final — clean ReportLab version, no pyplot)
# ------------------------------------------------------------------------
import streamlit as st
from dataclasses import dataclass
from typing import List
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak



st.set_page_config(page_title="Risk Questionnaire", page_icon="📊", layout="centered")
# ---- Sidebar progress placeholders (single instance) ----
st.sidebar.markdown("### 📊 Progress")
_progress_slot = st.sidebar.empty()     # progress bar lives here
_caption_slot  = st.sidebar.empty()     # caption lives here


# --- Streamlit Styling ----------------------------------------------------------
st.markdown("""
<style>
.result-card {
    background-color: #F7F9FB;
    border-radius: 12px;
    padding: 22px 24px;
    border: 1px solid #E0E7EF;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}
.overall-card {
    background-color: #F9FAFB;
    border-radius: 12px;
    padding: 22px 26px;
    border: 1px solid #E3E9EE;
    box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    margin-top: 25px;
    margin-bottom: 25px;
}
.teal { color: #2B8CA3; font-weight:600; }
.muted { color:#5A6B7A; font-size:0.92rem; }
</style>
""", unsafe_allow_html=True)

# --- Data Models ----------------------------------------------------------------
@dataclass
class Question:
    prompt: str
    options: List[str]

@dataclass
class Section:
    title: str
    questions: List[Question]

def option_score(idx: int) -> int:
    return 5 - idx

# --- Questionnaire definitions -------------------------------------------------
risk_tolerance = Section(
    title="Risk Tolerance",
    questions=[
        Question("How do you feel when thinking about taking financial risks?", [
            "Thrilled — I enjoy taking risks for higher rewards",
            "Excited — I’m open to taking risks",
            "Neutral — I can accept risks but don’t seek them",
            "Uneasy — I’m cautious about taking risks",
            "Afraid — I strongly avoid financial risks",        
        ]),
        Question("Imagine there’s a sudden global market crash caused by an unexpected event that experts don’t yet understand. Headlines are panicking, your portfolio has fallen 20% in just a few weeks, and news outlets are warning of more uncertainty. How would you most likely respond?", [
            "Invest more",
            "Hold steady and wait for markets to recover",
            "Do nothing immediately, but watch closely",
            "Sell part of my investments",
            "Sell most or all of my investments",            
        ]), 
        Question("You’re given an unexpected R50 000 bonus. You can either keep it safely or take a chance at earning more. Which option sounds most like you?", [
            "Risk it all for a 10 % chance to make ten times your money.",
            "Take a 25 % chance to triple it, or lose it all.",
            "Take a 50 % chance to double it, or lose it all.",
            "50 % chance of getting R75 000, or 50 % chance of getting R25 000.",
            "Keep the full R50 000 — guaranteed.",
        ]),
        Question("A close friend is launching a new renewable-energy business. They believe it could return 5–10× your investment within five years, but there’s a good chance you could lose everything. If you could afford it, how much would you realistically invest?", [
            "A large stake — I’d put in whatever it takes if the upside looks exciting.",
            "A significant amount — up to six months’ income.",
            "A moderate amount — two to three months’ income.",
            "A small amount — maybe one month’s income.",
            "Nothing — I wouldn’t risk my capital on something so uncertain.",
        ]),      
        Question("How much risk are you willing to take with your finances right now?", [
            "A lot — I want aggressive growth",
            "A fair amount — I’m comfortable with moderate–high risk",
            "A balanced amount — I want moderate risk",
            "A little — I prefer low risk",
            "None — I want safety and stability",
        ]),
        Question("Which investment option appeals to you most?", [
            "Very high risk / very high return potential",
            "High risk / high return potential",
            "Moderate risk / moderate return potential",
            "Low risk / low return potential",
            "No risk / low but guaranteed return",
        ]),
        Question("When you see alarming financial news or market headlines that could affect your portfolio, how do you typically react?", [
            "I ignore most of it — short-term noise doesn’t bother me",
            "I read it, but rarely take any action",
            "I monitor my investments more closely for a while",
            "I feel anxious and consider adjusting my portfolio",
            "I often make quick changes or contact my advisor immediately",
        
        ]),
        Question("If your investments moved up or down sharply from week to week, how would that affect you?", [
            "I’d see it as normal and ignore short-term swings",
            "I’d stay calm but stay aware of the movements",
            "I’d check more often and feel a little uneasy",
            "I’d feel stressed and consider changing my investments",
            "I’d lose sleep or want to exit volatile investments entirely",
        ]),
    ]
)

risk_capacity = Section(
    title="Risk Capacity",
    questions=[
        Question("How stable and predictable is your main source of income?", [
            "Very stable and highly predictable",
            "Mostly stable with minor uncertainty",
            "Moderately stable, some ups and downs",
            "Unstable, often fluctuates",
            "Very unstable and unpredictable",
        ]),
        Question("How does your income compare to your regular expenses?", [
            "Much higher — I have a large surplus each month",
            "Higher — I usually save comfortably",
            "About equal — I break even most months",
            "Lower — I sometimes struggle to cover expenses",
            "Much lower — I frequently rely on debt or savings",
        ]),
        Question("Thinking about your family and future, which of the following best describes your situation regarding financial dependents and potential inheritance?", [
            "I have no dependents and expect a significant inheritance or financial support later in life",
            "I have few or no dependents and expect a moderate inheritance in future",
            "I have few or no dependents, and any inheritance I might receive is uncertain",
            "I have some dependents and don’t expect much inheritance support",
            "I have several people who rely on me financially, and I don’t expect any inheritance",
        ]),
        Question("Excluding your home loan or car finance, how would you describe your current debt situation?", [
            "I’m completely debt-free",
            "I have no debt, though I sometimes use a credit card and pay it off immediately",
            "I have manageable debts that I usually pay off by the end of the month",
            "I have debts that sometimes feel difficult to manage or cause financial pressure",
            "I have significant debts that are difficult to manage",            
        ]),
        Question("How many months of living expenses could you cover using your savings and other easily accessible liquid assets?", [
            "More than 12 months",
            "7–12 months",
            "4–6 months",
            "1–3 months",
            "Less than 1 month / none",
        ]),
        Question("If you were to experience a major financial setback, how confident are you in your ability to recover through future income or resources?", [
            "Very confident — I could recover quickly through income or other assets",
            "Fairly confident — I could recover over time with some adjustments",
            "Somewhat confident — recovery would take time and careful planning",
            "Not very confident — recovery would be difficult",
            "Not confident at all — it would be extremely hard to recover financially",
        ]),
        Question("How likely are you to face major expenses or financial obligations in the next five years (such as education costs, medical costs, or familial changes)?", [
            "Very unlikely — no large expenses expected",
            "Somewhat unlikely — small chance of moderate expenses",
            "Uncertain — depends on future circumstances",
            "Somewhat likely — a few large expenses expected",
            "Very likely — significant expenses are definite or planned",
        ]),
        Question("If your income were to decrease or investment returns were lower for a period of time, how easily could you reduce your expenses to adjust?", [
            "I could easily scale down my lifestyle with minimal impact",
            "I could comfortably reduce expenses for a while if necessary",
            "I could reduce some costs with moderate effort",
            "It would be challenging — I could cut back a little, but not much",
            "It would be very difficult — my expenses are largely fixed",
        ]),            
    ]    
)    

# --- Scoring --------------------------------------------------------------------
def interpret_tolerance(score):
    if 8 <= score <= 13:
        return "Conservative", "Prefers safety and capital preservation above all."
    elif 14 <= score <= 20:
        return "Moderately Conservative", "Comfortable with some volatility but prioritizes capital protection."
    elif 21 <= score <= 27:
        return "Moderate", "Seeks a balance between growth and stability."
    elif 28 <= score <= 34:
        return "Moderately Aggressive", "Willing to accept meaningful risk for higher potential growth."
    else:  # 35–40
        return "Aggressive", "Comfortable with high volatility for maximum long-term returns."

def interpret_capacity(score):
    if 8 <= score <= 13:
        return "Conservative", "Low flexibility or shorter-term horizon — prefers minimal risk."
    elif 14 <= score <= 20:
        return "Moderately Conservative", "Stable finances but cautious toward uncertainty."
    elif 21 <= score <= 27:
        return "Moderate", "Average stability and flexibility — can accept some drawdowns."
    elif 28 <= score <= 34:
        return "Moderately Aggressive", "Strong financial stability and capacity for risk."
    else:  # 35–40
        return "Aggressive", "High surplus, strong resources, and long horizon — well suited for higher risk."


def overall_message(tol, cap):
    diff = abs(tol - cap)
    if diff < 6:
        return "Your tolerance and capacity are broadly aligned — your overall position looks appropriate."
    elif tol > cap:
        return "Your risk tolerance is higher than your financial capacity. Please discuss this with your advisor."
    else:
        return "Your financial capacity allows more risk than you currently feel comfortable taking. Review your goals."

def combine_label(tol_level, cap_level):
    order = ["Conservative", "Moderately Conservative", "Moderate", "Moderately Aggressive", "Aggressive"]
    t = next((o for o in order if tol_level.startswith(o)), "Moderate")
    c = next((o for o in order if cap_level.startswith(o)), "Moderate")
    # Return the lower (more conservative) of the two
    return order[min(order.index(t), order.index(c))]

# --- PDF Generator --------------------------------------------------------------
def generate_pdf(tol_total, tol_level, tol_desc, cap_total, cap_level, cap_desc,
                 msg, overall_label, tol_answers, cap_answers, client_name, client_email):
    buffer = BytesIO()
    dark_blue = colors.HexColor("#0E4C74")
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        title="Risk Profile Report",
        leftMargin=18*mm,
        rightMargin=18*mm,
        topMargin=18*mm,
        bottomMargin=18*mm,
    )
    normal = ParagraphStyle("normal", fontSize=10.5, leading=14)
    h2 = ParagraphStyle("h2", fontSize=13, textColor=dark_blue, spaceBefore=12, spaceAfter=8, alignment=1)
    title = ParagraphStyle("title", fontSize=18, alignment=1, textColor=dark_blue, spaceAfter=10)

    elements = [
        Paragraph(f"Client Risk Profile Report: {client_name}", title),
        Spacer(1, 20),
    ]


    # --- Summary table
    data = [
        ["Category", "Score (0–40)", "Level", "Description"],
        [
            "Risk Tolerance",
            f"{tol_total}/40",
            Paragraph(tol_level, normal),
            Paragraph(tol_desc, normal),
        ],
        [
            "Risk Capacity",
            f"{cap_total}/40",
            Paragraph(cap_level, normal),
            Paragraph(cap_desc, normal),
        ],
    ]

    t = Table(data, colWidths=[85, 85, 95, 190])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), dark_blue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),     # center header text
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),   # vertical alignment for wrapped text
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))
    elements.append(t)

    # Space below the summary table
    elements.append(Spacer(1, 14))

    # Show the explanatory message as a full-width, styled box
    msg_table = Table([[Paragraph(msg, normal)]], colWidths=[455])
    msg_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(msg_table)

    # Space above the Risk & Return section
    elements.append(Spacer(1, 18))

    # --- Risk & Return Profiles
    elements.append(Paragraph("Risk & Return Profiles", h2))

    profiles = [
        ("Conservative", 9.9, 5.6),
        ("Mod. Conservative", 10.5, 6.8),
        ("Moderate", 11.0, 8.4),
        ("Mod. Aggressive", 11.6, 10.3),
        ("Aggressive", 12.1, 12.2),
    ]

    pdata = [["Profile", "Hist Average Return", "Hist Annual Volatility"]]
    for p in profiles:
        pdata.append([p[0], f"{p[1]}%", f"{p[2]}%"])

    tp = Table(pdata, colWidths=[140, 120, 120])
    tp.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), dark_blue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),    # center header titles
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),   # center numeric data
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))
    elements.append(tp)

    # --- Box & Whisker chart (centered & well spaced)
    chart_path = "box_whisker_summary.png"
    img = Image(chart_path, width=420, height=220)

    # Center the image more precisely under the table (slightly wider frame)
    img_table = Table([[img]], colWidths=[440])
    img_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
    ]))
    elements.append(img_table)


    # gentle space below the chart before the next section
    elements.append(Spacer(1, 35))

    # --- Answers (boxed layout)
    elements.append(PageBreak())
    elements.append(Paragraph("Risk Tolerance", h2))
    for i, (q, a) in enumerate(tol_answers, 1):
        qa_table = Table(
            [[Paragraph(f"<b>Q{i}.</b> {q}", normal)],
             [Paragraph(f"<i>Answer:</i> {a}", normal)]],
            colWidths=[450]
        )
        qa_table.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.75, colors.grey),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(qa_table)
        elements.append(Spacer(1, 6))

    elements.append(PageBreak())
    elements.append(Paragraph("Risk Capacity", h2))
    for i, (q, a) in enumerate(cap_answers, 1):
        qa_table = Table(
            [[Paragraph(f"<b>Q{i}.</b> {q}", normal)],
             [Paragraph(f"<i>Answer:</i> {a}", normal)]],
            colWidths=[450]
        )
        qa_table.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.75, colors.grey),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(qa_table)
        elements.append(Spacer(1, 6))

    # --- Notes Section (smaller text, bottom of final page) -------------------------
    elements.append(PageBreak())
    elements.append(Spacer(1, 420))
    small = ParagraphStyle("small", fontSize=8.5, leading=11, alignment=1)
    elements.append(Paragraph(
        "<b>Notes:</b> Each risk profile reflects a different blend of local and global equities "
        "versus local bonds: Conservative (20% local equity, 10% global equity, 70% local bonds); "
        "Mod. Conservative (30%/15%/55%); Moderate (40%/20%/40%); "
        "Mod. Aggressive (50%/25%/25%); Aggressive (60%/30%/10%). "
        "Results are based on 20 years of daily data using rolling one-year periods.",
        small
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

    elements.append(Spacer(1, 16))
                     
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()





# --- Streamlit Flow -------------------------------------------------------------
def render_section(section, key_prefix):
    scores, answers = [], []
    for i, q in enumerate(section.questions):
        st.markdown(f"**Q{i+1}. {q.prompt}**")
        choice = st.radio("", q.options, index=None, key=f"{key_prefix}_{i}")
        scores.append(None if choice is None else option_score(q.options.index(choice)))
        answers.append((q.prompt, choice if choice else "—"))
    return scores, answers

def all_answered(scores): return all(s is not None for s in scores)

def result_card(title, score, level, desc):
    st.markdown(f"""
    <div class='result-card'>
      <span class='teal'>{title}</span><br>
      <span class='muted'>Score:</span> <b>{score}/40</b><br>
      <span class='muted'>Level:</span> {level}<br><br>
      <span class='muted'>{desc}</span>
    </div>
    """, unsafe_allow_html=True)

# --- Sidebar progress tracker ---------------------------------------------------
def render_progress_sidebar():
    tol_count = sum(
        1 for i in range(len(risk_tolerance.questions))
        if st.session_state.get(f"tol_{i}") is not None
    )
    cap_count = sum(
        1 for i in range(len(risk_capacity.questions))
        if st.session_state.get(f"cap_{i}") is not None
    )
    total_questions = len(risk_tolerance.questions) + len(risk_capacity.questions)
    answered = tol_count + cap_count
    progress = int((answered / total_questions) * 100)

    _progress_slot.progress(progress)
    _caption_slot.caption(f"{answered} of {total_questions} questions answered ({progress}%)")


# --- Streamlit Flow -------------------------------------------------------------
st.title("📊 Risk Questionnaire")
st.header("Client Information")
client_name = st.text_input("Full Name")
client_email = st.text_input("Email Address")

# Prevent moving forward without details
if not client_name or not client_email:
    st.warning("Please enter your name and email before starting the questionnaire.")
    st.stop()

render_progress_sidebar()  # initial bar

st.header("Risk Tolerance Questionnaire")
tol_scores, tol_answers = render_section(risk_tolerance, "tol")
render_progress_sidebar()  # updates while answering

if all_answered(tol_scores):
    tol_total = sum(tol_scores)
    tol_level, tol_desc = interpret_tolerance(tol_total)
    result_card("Risk Tolerance", tol_total, tol_level, tol_desc)
    st.divider()

    st.header("Risk Capacity Questionnaire")
    cap_scores, cap_answers = render_section(risk_capacity, "cap")
    render_progress_sidebar()  # updates while answering

    if all_answered(cap_scores):
        cap_total = sum(cap_scores)
        cap_level, cap_desc = interpret_capacity(cap_total)
        result_card("Risk Capacity", cap_total, cap_level, cap_desc)

        message = overall_message(tol_total, cap_total)
        overall_label = combine_label(tol_level, cap_level)
        st.markdown(
            f"<div class='overall-card'><b>Overall Risk Position</b><br>"
            f"<span class='muted'>{message}</span></div>",
            unsafe_allow_html=True
        )

        pdf = generate_pdf(
            tol_total, tol_level, tol_desc,
            cap_total, cap_level, cap_desc,
            message, overall_label,
            tol_answers, cap_answers,
            client_name, client_email
        )

        st.download_button("📄 Download PDF Report", pdf, "Risk_Profile_Report.pdf", mime="application/pdf")
    else:
        st.info("Please complete all Risk Capacity questions to generate your PDF report.")
else:
    st.info("Please complete all Risk Tolerance questions to proceed to Risk Capacity.")
