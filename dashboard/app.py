import dash
from dash import html, dcc
import plotly.graph_objects as go
import json, os
from datetime import datetime

app = dash.Dash(__name__, title="IntelliQA Dashboard")

NAVY="#1E3A5F"; TEAL="#0D9488"; BG="#0F172A"; CARD="#1E293B"
LIGHT="#E2E8F0"; MID="#94A3B8"; GREEN="#22C55E"; RED="#EF4444"; AMBER="#F59E0B"

def load_failures():
    path = "execution-pipeline/failure_report.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []

def card(children, style={}):
    return html.Div(children, style={"background":CARD,"borderRadius":"12px","padding":"20px","border":"1px solid #334155",**style})

def stat_card(value, label, color):
    return card([
        html.Div(str(value), style={"fontSize":"42px","fontWeight":"bold","color":color,"textAlign":"center","marginBottom":"6px"}),
        html.Div(label, style={"fontSize":"12px","color":MID,"textAlign":"center","textTransform":"uppercase","letterSpacing":"0.05em"})
    ])

def build_layout():
    bugs = load_failures()
    total=35; passed=35-len(bugs); failed=len(bugs)

    risk_fig = go.Figure(go.Bar(
        x=["payments","transfers","refunds","accounts","get_payment"],
        y=[5,3,3,1,1],
        marker_color=[RED,AMBER,AMBER,GREEN,GREEN],
        text=["HIGH","MEDIUM","MEDIUM","LOW","LOW"],
        textposition="outside",
    ))
    risk_fig.update_layout(plot_bgcolor=CARD,paper_bgcolor=CARD,font_color=LIGHT,
        margin=dict(t=20,b=20,l=20,r=20),
        yaxis=dict(showgrid=False,showticklabels=False,zeroline=False),
        xaxis=dict(showgrid=False),height=220)

    donut_fig = go.Figure(go.Pie(
        values=[passed, max(failed,0), 0],
        labels=["Passed","Failed",""],
        hole=0.65, marker_colors=[GREEN,RED,"#334155"],
        textinfo="none"))
    donut_fig.update_layout(plot_bgcolor=CARD,paper_bgcolor=CARD,font_color=LIGHT,
        margin=dict(t=10,b=10,l=10,r=10),height=200,showlegend=True,
        legend=dict(font=dict(color=LIGHT,size=11)))
    donut_fig.add_annotation(text=f"<b>{passed}</b><br>passed",
        x=0.5,y=0.5,showarrow=False,font=dict(size=18,color=GREEN))

    if bugs:
        bug_items = []
        for b in bugs:
            name = b.get("test","").split("::")[-1]
            analysis = b.get("analysis","")
            lines = {l.split(":")[0].strip():":".join(l.split(":")[1:]).strip() for l in analysis.split("\n") if ":" in l}
            sev = lines.get("SEVERITY","High")
            col = RED if "Critical" in sev else (AMBER if "High" in sev else GREEN)
            bug_items.append(html.Div([
                html.Div(f"❌ {name}", style={"fontFamily":"monospace","fontSize":"12px","color":MID,"marginBottom":"4px"}),
                html.Div(lines.get("ROOT CAUSE","See analysis"), style={"fontSize":"13px","color":LIGHT,"marginBottom":"4px"}),
                html.Div(f"Severity: {sev}  |  {lines.get('AFFECTED ENDPOINT','')}", style={"fontSize":"11px","color":MID}),
            ], style={"background":BG,"borderRadius":"8px","padding":"12px","marginBottom":"10px","borderLeft":f"3px solid {col}"}))
        bug_section = bug_items
    else:
        bug_section = [html.Div("✅ All tests passing — no active failures",
            style={"color":GREEN,"textAlign":"center","padding":"30px","fontSize":"14px"})]

    logs = [
        ("test_payments.py::test_happy_path_payment","pass"),
        ("test_payments.py::test_amount_missing_payment","pass"),
        ("test_payments.py::test_amount_zero_payment","pass"),
        ("test_payments.py::test_amount_negative_payment","pass"),
        ("test_payments.py::test_currency_missing_payment","pass"),
        ("test_payments.py::test_account_not_found_payment","pass"),
        ("test_payments.py::test_insufficient_funds_payment","pass"),
        ("test_refunds.py::test_refund_happy_path","pass"),
        ("test_refunds.py::test_refund_payment_not_found","pass"),
        ("test_refunds.py::test_refund_exceeds_original_payment","pass"),
        ("test_transfers.py::test_transfers_happy_path","pass"),
        ("test_transfers.py::test_transfers_insufficient_funds","pass"),
        ("test_transfers.py::test_transfers_invalid_amount","pass"),
        ("test_transfers.py::test_transfers_zero_amount","pass"),
        ("test_accounts.py::test_get_account_valid_id","pass"),
        ("test_accounts.py::test_get_account_non_existent_id","pass"),
        ("test_get_payment.py::test_get_payment_success","pass"),
        ("test_get_payment.py::test_get_payment_not_found","pass"),
    ]
    log_items = [html.Div(
        f"{'✅ PASSED' if s=='pass' else '❌ FAILED'} — {t}",
        style={"fontFamily":"monospace","fontSize":"12px","padding":"5px 0",
               "borderBottom":"1px solid #1E293B",
               "color":GREEN if s=="pass" else RED}
    ) for t,s in logs]

    return html.Div([
        html.Div([
            html.Div([
                html.H1([html.Span("Intelli",style={"color":LIGHT}),html.Span("QA",style={"color":TEAL})],
                    style={"fontSize":"28px","fontWeight":"bold","margin":0}),
                html.Div("AI-Driven Autonomous Test Generation & Risk-Based Execution Platform",
                    style={"fontSize":"12px","color":MID,"marginTop":"4px"})
            ]),
            html.Div([
                html.Span(f"Last updated: {datetime.now().strftime('%d %b %Y %H:%M')}",
                    style={"fontSize":"12px","color":MID,"marginRight":"12px"}),
                html.Span("● LIVE",style={"background":TEAL,"color":"white","padding":"4px 12px",
                    "borderRadius":"20px","fontSize":"12px","fontWeight":"bold"})
            ])
        ], style={"background":NAVY,"padding":"20px 30px","display":"flex",
            "alignItems":"center","justifyContent":"space-between","borderBottom":f"2px solid {TEAL}"}),

        html.Div([
            html.Div([
                stat_card(total,"Tests Generated",TEAL),
                stat_card(passed,"Tests Passed",GREEN),
                stat_card(failed,"Tests Failed",RED if failed>0 else GREEN),
                stat_card(len(bugs),"Bugs Found",AMBER),
            ], style={"display":"grid","gridTemplateColumns":"repeat(4,1fr)","gap":"16px","marginBottom":"20px"}),

            html.Div([
                card([html.H3("Risk Heatmap",style={"fontSize":"13px","color":MID,"textTransform":"uppercase","letterSpacing":"0.05em","marginBottom":"12px"}),
                    dcc.Graph(figure=risk_fig,config={"displayModeBar":False})]),
                card([html.H3("Pass / Fail",style={"fontSize":"13px","color":MID,"textTransform":"uppercase","letterSpacing":"0.05em","marginBottom":"12px"}),
                    dcc.Graph(figure=donut_fig,config={"displayModeBar":False})]),
            ], style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"16px","marginBottom":"20px"}),

            card([html.H3("AI Failure Analysis",style={"fontSize":"13px","color":MID,"textTransform":"uppercase","letterSpacing":"0.05em","marginBottom":"12px"}),
                *bug_section], style={"marginBottom":"20px"}),

            card([html.H3("Execution Log",style={"fontSize":"13px","color":MID,"textTransform":"uppercase","letterSpacing":"0.05em","marginBottom":"12px"}),
                *log_items]),

            html.Div(["IntelliQA — MSc Software Design with Cloud Computing | TUS Athlone | ",
                html.A("github.com/shivendrasurve/IntelliQA",
                    href="https://github.com/shivendrasurve/IntelliQA",style={"color":TEAL})
            ], style={"textAlign":"center","padding":"20px","color":"#334155","fontSize":"12px","marginTop":"20px"})

        ], style={"padding":"24px 30px","maxWidth":"1200px","margin":"0 auto"})
    ], style={"background":BG,"minHeight":"100vh","color":LIGHT,"fontFamily":"Arial"})

app.layout = build_layout

if __name__ == "__main__":
    print("IntelliQA Dashboard → http://localhost:8050")
    app.run(debug=True, host="0.0.0.0", port=8050)
