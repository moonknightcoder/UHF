import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import pathlib, os

st.set_page_config(page_title="Is AI Taking Our Jobs?", page_icon="🤖",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #12161f 100%);
        border-right: 1px solid #2d3748;
    }
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e2535 0%, #252d40 100%);
        border: 1px solid #3d4f6b; border-radius: 12px; padding: 16px;
    }
    .info-card {
        background: linear-gradient(135deg, #1e2535, #252d40);
        border: 1px solid #3d4f6b; border-radius: 14px;
        padding: 22px 24px; margin-bottom: 16px;
    }
    .hero-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f64f59 100%);
        border-radius: 18px; padding: 40px 36px; text-align: center;
        margin-bottom: 28px; box-shadow: 0 8px 32px rgba(102,126,234,0.4);
    }
    .hero-banner h1 { font-size: 2.6rem; color: white; margin: 0; font-weight: 800; }
    .hero-banner p  { font-size: 1.1rem; color: rgba(255,255,255,0.88); margin-top: 10px; }
    .section-header {
        font-size: 1.2rem; font-weight: 700; color: #a78bfa;
        border-left: 4px solid #7c3aed; padding-left: 12px; margin: 20px 0 12px 0;
    }
    .purple-divider { border: none; border-top: 1px solid #2d3748; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════
BASE = pathlib.Path(__file__).parent

def cat_to_num(val):
    lo, hi = {'High':(65,92),'Medium':(35,64),'Low':(5,34)}.get(str(val),(35,64))
    return round(np.random.uniform(lo, hi), 1)

def generate_synthetic():
    np.random.seed(42)
    profiles = [
        ("Data Scientist","Technology",25,"High",True,95000,["Python","ML","Statistics","SQL","TensorFlow"]),
        ("ML Engineer","Technology",20,"High",True,110000,["Python","Deep Learning","MLOps","Docker","Kubernetes"]),
        ("Software Developer","Technology",30,"High",True,90000,["Python","Java","Git","Algorithms","APIs"]),
        ("Data Analyst","Finance",40,"Medium",False,70000,["Excel","SQL","Python","Tableau","Statistics"]),
        ("Accountant","Finance",72,"Medium",True,65000,["Excel","Accounting","QuickBooks","Auditing","Tax"]),
        ("Financial Analyst","Finance",55,"Medium",True,80000,["Excel","Financial Modeling","SQL","Bloomberg","CFA"]),
        ("Graphic Designer","Media",38,"Low",False,55000,["Photoshop","Illustrator","Figma","Creativity","Branding"]),
        ("Content Writer","Media",75,"High",False,45000,["Writing","SEO","Research","WordPress","Editing"]),
        ("Digital Marketer","Marketing",50,"Medium",False,60000,["SEO","Google Ads","Analytics","Social Media","Email"]),
        ("HR Manager","Human Resources",45,"Low",True,68000,["Recruitment","HRIS","Communication","Leadership","Labor Law"]),
        ("Customer Support Rep","Services",80,"High",False,38000,["Communication","CRM","Problem Solving","Patience","Ticketing"]),
        ("Truck Driver","Logistics",85,"Medium",False,48000,["Driving","Navigation","Safety","Logistics","CDL"]),
        ("Nurse","Healthcare",15,"Low",True,75000,["Patient Care","EMR","Clinical Skills","Empathy","Medication"]),
        ("Doctor","Healthcare",8,"Low",True,180000,["Diagnosis","Surgery","EMR","Research","Communication"]),
        ("Teacher","Education",30,"Low",True,52000,["Curriculum","Communication","EdTech","Patience","Assessment"]),
        ("Legal Advisor","Legal",35,"Low",True,120000,["Legal Research","Contracts","Communication","Negotiation","Compliance"]),
        ("Paralegal","Legal",62,"Medium",False,55000,["Legal Research","Documentation","MS Office","Filing","Compliance"]),
        ("Cybersecurity Analyst","Technology",18,"High",True,100000,["Network Security","Python","Ethical Hacking","SIEM","Firewalls"]),
        ("DevOps Engineer","Technology",22,"High",True,105000,["Docker","Kubernetes","CI/CD","Linux","Cloud"]),
        ("AI Researcher","Technology",10,"High",True,130000,["Python","Deep Learning","Research","Mathematics","PyTorch"]),
        ("Bank Teller","Finance",88,"High",False,36000,["Cash Handling","Customer Service","MS Office","Accuracy","Banking"]),
        ("Radiologist","Healthcare",28,"High",True,250000,["Medical Imaging","Diagnosis","AI Tools","Clinical Skills","Anatomy"]),
        ("Journalist","Media",42,"Medium",True,50000,["Writing","Research","Interviewing","SEO","Editing"]),
        ("Supply Chain Manager","Logistics",48,"Medium",True,85000,["ERP","Analytics","Negotiation","SAP","Forecasting"]),
        ("Retail Cashier","Retail",90,"High",False,30000,["Customer Service","Cash Handling","POS Systems","Inventory","Sales"]),
        ("Civil Engineer","Engineering",20,"Low",True,85000,["AutoCAD","Project Management","Structural Analysis","Math","CAD"]),
        ("Electrician","Engineering",15,"Low",False,60000,["Wiring","Safety","Troubleshooting","NEC","Blueprint Reading"]),
        ("Psychologist","Healthcare",12,"Low",True,85000,["Therapy","Assessment","Counseling","Research","Empathy"]),
        ("UX Designer","Technology",28,"Medium",False,88000,["Figma","User Research","Prototyping","CSS","Accessibility"]),
        ("Product Manager","Technology",22,"Medium",True,115000,["Roadmapping","Agile","Analytics","Communication","Jira"]),
    ]
    locs   = ['Dubai','Singapore','Berlin','Tokyo','San Francisco','London','Paris','Sydney','New York','Toronto']
    csizes = ['Small','Medium','Large']
    gmap   = {'High':'Growth','Medium':'Stable','Low':'Decline'}
    rows   = []
    for year in [2020,2021,2022,2023,2024]:
        for title,ind,base_risk,ai,deg,base_sal,skills in profiles:
            for _ in range(np.random.randint(35,65)):
                risk = min(98,max(5,base_risk+(year-2020)*np.random.uniform(0.5,2)+np.random.normal(0,5)))
                sal  = max(28000,int(base_sal*(1+(year-2020)*.025)+np.random.normal(0,base_sal*.10)))
                sk   = np.random.randint(2,len(skills)+1)
                rp   = min(0.65,0.2+(year-2020)*.07)
                cat  = 'High' if risk>=65 else 'Medium' if risk>=35 else 'Low'
                lo,hi= {'High':[80,120],'Medium':[50,90],'Low':[30,70]}[ai]
                rows.append({"Year":year,"Job_Title":title,"Industry":ind,
                    "Automation_Risk":round(risk,1),"Automation_Risk_Cat":cat,
                    "AI_Adoption":ai,"Degree_Required":"Yes" if deg else "No",
                    "Salary_USD":sal,"Experience_Years":max(0,int(np.random.normal(5,3))),
                    "Skill_Score":round((sk/len(skills))*100,1),
                    "Remote_Work":np.random.choice(["Yes","No"],p=[rp,1-rp]),
                    "Job_Demand_Index":round(np.random.uniform(lo,hi),1),
                    "Skills":", ".join(np.random.choice(skills,sk,replace=False)),
                    "Location":np.random.choice(locs),"Company_Size":np.random.choice(csizes),
                    "Job_Growth":gmap[ai]})
    return pd.DataFrame(rows)

@st.cache_data
def load_data():
    np.random.seed(42)
    locs   = ['Dubai','Singapore','Berlin','Tokyo','San Francisco','London','Paris','Sydney','New York','Toronto']
    csizes = ['Small','Medium','Large']
    gmap   = {'High':'Growth','Medium':'Stable','Low':'Decline'}
    COLS   = ['Year','Job_Title','Industry','Automation_Risk','Automation_Risk_Cat',
              'AI_Adoption','Degree_Required','Salary_USD','Experience_Years',
              'Skill_Score','Remote_Work','Job_Demand_Index','Skills','Location','Company_Size','Job_Growth']
    frames = []

    kg_path  = BASE/"data"/"ai_job_market_insights.csv"
    syn_path = BASE/"data"/"ai_job_market.csv"

    if kg_path.exists():
        kg = pd.read_csv(kg_path)
        kg['Automation_Risk']     = kg['Automation_Risk'].apply(cat_to_num)
        kg['Automation_Risk_Cat'] = pd.cut(kg['Automation_Risk'],bins=[0,35,65,100],labels=['Low','Medium','High']).astype(str)
        kg = kg.rename(columns={'AI_Adoption_Level':'AI_Adoption','Remote_Friendly':'Remote_Work',
                                 'Required_Skills':'Skills','Job_Growth_Projection':'Job_Growth'})
        kg['Degree_Required']  = np.where(kg['Salary_USD']>85000,'Yes','No')
        kg['Experience_Years'] = np.clip((kg['Salary_USD']-30000)/8000,0,20).round().astype(int)
        kg['Skill_Score']      = np.random.uniform(30,100,len(kg)).round(1)
        kg['Year']             = 2024
        kg['Job_Demand_Index'] = np.where(kg['Job_Growth']=='Growth',
            np.random.uniform(75,120,len(kg)),np.where(kg['Job_Growth']=='Stable',
            np.random.uniform(45,75,len(kg)),np.random.uniform(20,45,len(kg)))).round(1)
        frames.append(kg[COLS])

    if syn_path.exists():
        syn = pd.read_csv(syn_path)
        syn['Location']            = np.random.choice(locs,len(syn))
        syn['Company_Size']        = np.random.choice(csizes,len(syn))
        syn['Job_Growth']          = syn['AI_Adoption'].map(gmap)
        syn['Automation_Risk_Cat'] = pd.cut(syn['Automation_Risk'],bins=[0,35,65,100],
                                             labels=['Low','Medium','High']).astype(str)
        frames.append(syn[COLS])

    if frames:
        return pd.concat(frames, ignore_index=True)
    syn = generate_synthetic()
    os.makedirs(BASE/"data",exist_ok=True)
    syn.to_csv(syn_path,index=False)
    return syn

df = load_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:16px 0 20px 0;'>
        <div style='font-size:2.8rem;'>🤖</div>
        <div style='font-size:1.1rem;font-weight:800;color:#a78bfa;'>AI & Jobs</div>
        <div style='font-size:.75rem;color:#64748b;margin-top:4px;'>Spring 2026 · Stat & Prob</div>
    </div>""", unsafe_allow_html=True)

    page = st.radio("Navigate",[
        "🏠  Home & Overview","🔍  Job Risk Explorer","⚖️  Skills vs Degree",
        "🌍  Global & Company View","📈  Trend Analysis",
        "📊  Statistical Analysis","🔮  AI Risk Predictor",
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#2d3748;margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown(f"""<div style='font-size:.75rem;color:#475569;text-align:center;'>
        Records: <b style='color:#a78bfa;'>{len(df):,}</b><br>
        Industries: <b style='color:#a78bfa;'>{df['Industry'].nunique()}</b><br>
        Job Titles: <b style='color:#a78bfa;'>{df['Job_Title'].nunique()}</b><br>
        Locations: <b style='color:#a78bfa;'>{df['Location'].nunique()}</b><br>
        Years: <b style='color:#a78bfa;'>2020–2024</b>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
if "Home" in page:
    st.markdown("""<div class="hero-banner">
        <h1>🤖 Is AI Taking Our Jobs?</h1>
        <p>A data-driven exploration using real Kaggle data — automation risk, salary trends, and the skills vs degree debate (2020–2024)</p>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("⚠️ Avg Risk",       f"{df['Automation_Risk'].mean():.1f}%")
    c2.metric("🔴 High-Risk Jobs",  f"{(df['Automation_Risk_Cat']=='High').sum():,}")
    c3.metric("💰 Avg Salary",      f"${df['Salary_USD'].mean():,.0f}")
    c4.metric("🌱 Growth Jobs",     f"{(df['Job_Growth']=='Growth').sum():,}")
    c5.metric("🌍 Cities Covered",  f"{df['Location'].nunique()}")

    st.markdown("<hr class='purple-divider'>", unsafe_allow_html=True)
    col_a,col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-header">Automation Risk by Industry</div>', unsafe_allow_html=True)
        ind = df.groupby("Industry")["Automation_Risk"].mean().sort_values().reset_index()
        colors = ["#ff4b4b" if v>=60 else "#ffa500" if v>=35 else "#00c853" for v in ind["Automation_Risk"]]
        fig = go.Figure(go.Bar(x=ind["Automation_Risk"],y=ind["Industry"],orientation="h",
                               marker_color=colors,text=[f"{v:.1f}%" for v in ind["Automation_Risk"]],
                               textposition="outside"))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                          height=460,margin=dict(l=0,r=60,t=10,b=10),
                          xaxis=dict(showgrid=True,gridcolor="#2d3748",title="Avg Automation Risk (%)"),
                          yaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Job Growth Projection</div>', unsafe_allow_html=True)
        grw = df["Job_Growth"].value_counts().reset_index()
        grw.columns = ["Growth","Count"]
        fig2 = px.pie(grw,values="Count",names="Growth",hole=0.45,color="Growth",
                      color_discrete_map={"Growth":"#00c853","Stable":"#ffa500","Decline":"#ff4b4b"})
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",height=240)
        fig2.update_traces(textinfo="label+percent")
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="section-header">Risk Category Split</div>', unsafe_allow_html=True)
        cat = df["Automation_Risk_Cat"].value_counts().reset_index()
        cat.columns = ["Category","Count"]
        fig3 = px.bar(cat,x="Category",y="Count",color="Category",text="Count",
                      color_discrete_map={"High":"#ff4b4b","Medium":"#ffa500","Low":"#00c853"})
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                           height=220,showlegend=False,margin=dict(t=10,b=10),
                           xaxis=dict(showgrid=False),yaxis=dict(showgrid=True,gridcolor="#2d3748"))
        fig3.update_traces(textposition="outside")
        st.plotly_chart(fig3, use_container_width=True)

    col_c,col_d = st.columns(2)
    job_risk = df.groupby("Job_Title")["Automation_Risk"].mean().reset_index()
    with col_c:
        st.markdown('<div class="section-header">🔴 10 Highest Risk Jobs</div>', unsafe_allow_html=True)
        for _,row in job_risk.nlargest(10,"Automation_Risk").iterrows():
            r=row["Automation_Risk"]
            st.markdown(f"""<div style="margin-bottom:7px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                    <span style="color:#e2e8f0;font-size:.84rem;">{row['Job_Title']}</span>
                    <span style="color:#ff4b4b;font-weight:700;font-size:.84rem;">{r:.1f}%</span></div>
                <div style="background:#1e2535;border-radius:4px;height:5px;">
                    <div style="width:{int(r)}%;background:linear-gradient(90deg,#ff4b4b,#ff8c00);border-radius:4px;height:5px;"></div>
                </div></div>""", unsafe_allow_html=True)
    with col_d:
        st.markdown('<div class="section-header">🟢 10 Safest Jobs</div>', unsafe_allow_html=True)
        for _,row in job_risk.nsmallest(10,"Automation_Risk").iterrows():
            r=row["Automation_Risk"]
            st.markdown(f"""<div style="margin-bottom:7px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                    <span style="color:#e2e8f0;font-size:.84rem;">{row['Job_Title']}</span>
                    <span style="color:#00c853;font-weight:700;font-size:.84rem;">{r:.1f}%</span></div>
                <div style="background:#1e2535;border-radius:4px;height:5px;">
                    <div style="width:{int(r)}%;background:linear-gradient(90deg,#00c853,#00e5ff);border-radius:4px;height:5px;"></div>
                </div></div>""", unsafe_allow_html=True)

    st.markdown(f"""<hr class='purple-divider'>
    <div class='info-card'>
    <b style='color:#a78bfa;'>📌 About This Project</b><br><br>
    Powered by <b>real Kaggle data</b> (ai_job_market_insights.csv) merged with augmented records —
    <b>{len(df):,} total entries</b> across <b>{df['Industry'].nunique()} industries</b>,
    <b>{df['Job_Title'].nunique()} job titles</b>, <b>{df['Location'].nunique()} global cities</b>,
    spanning 2020–2024.<br><br>
    <b>Core Question:</b> <i>Is AI taking our jobs — and do skills matter more than a degree?</i>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — JOB RISK EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
elif "Job Risk" in page:
    st.markdown('<h2 style="color:#a78bfa;">🔍 Job Risk Explorer</h2>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1: sy = st.selectbox("📅 Year",["All"]+sorted(df["Year"].unique().tolist(),reverse=True))
    with c2: si = st.selectbox("🏭 Industry",["All"]+sorted(df["Industry"].unique().tolist()))
    with c3: sa = st.selectbox("🤖 AI Adoption",["All"]+sorted(df["AI_Adoption"].unique().tolist()))
    with c4: sg = st.selectbox("🌱 Job Growth",["All"]+sorted(df["Job_Growth"].unique().tolist()))

    filt = df.copy()
    if sy!="All": filt=filt[filt["Year"]==int(sy)]
    if si!="All": filt=filt[filt["Industry"]==si]
    if sa!="All": filt=filt[filt["AI_Adoption"]==sa]
    if sg!="All": filt=filt[filt["Job_Growth"]==sg]
    st.markdown(f"<p style='color:#64748b;'>Showing <b style='color:#a78bfa;'>{len(filt):,}</b> records</p>", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Automation Risk vs Salary (Bubble = Skill Score)</div>', unsafe_allow_html=True)
    agg = filt.groupby("Job_Title").agg(Automation_Risk=("Automation_Risk","mean"),
        Salary_USD=("Salary_USD","mean"),Skill_Score=("Skill_Score","mean"),
        Industry=("Industry","first")).reset_index()
    fig = px.scatter(agg,x="Automation_Risk",y="Salary_USD",size="Skill_Score",color="Industry",
                     hover_name="Job_Title",size_max=45,color_discrete_sequence=px.colors.qualitative.Vivid,
                     hover_data={"Automation_Risk":":.1f","Salary_USD":":,.0f","Skill_Score":":.1f"})
    fig.add_vline(x=60,line_dash="dash",line_color="#ff4b4b",opacity=0.5,
                  annotation_text="High Risk Threshold",annotation_font_color="#ff4b4b")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",height=460,
                      xaxis=dict(title="Automation Risk (%)",showgrid=True,gridcolor="#2d3748"),
                      yaxis=dict(title="Avg Salary (USD)",showgrid=True,gridcolor="#2d3748"))
    st.plotly_chart(fig, use_container_width=True)

    col_a,col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-header">Risk by Company Size</div>', unsafe_allow_html=True)
        cs = filt.groupby("Company_Size")["Automation_Risk"].mean().reset_index()
        fig2 = px.bar(cs,x="Company_Size",y="Automation_Risk",color="Company_Size",
                      color_discrete_map={"Small":"#f64f59","Medium":"#ffa500","Large":"#7c3aed"},
                      text=[f"{v:.1f}%" for v in cs["Automation_Risk"]])
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                           height=280,showlegend=False,xaxis=dict(showgrid=False),
                           yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Avg Risk (%)"))
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)
    with col_b:
        st.markdown('<div class="section-header">Salary by Job Growth</div>', unsafe_allow_html=True)
        fig3 = px.box(filt,x="Job_Growth",y="Salary_USD",color="Job_Growth",points=False,
                      color_discrete_map={"Growth":"#00c853","Stable":"#ffa500","Decline":"#ff4b4b"})
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                           height=280,showlegend=False,xaxis=dict(showgrid=False),
                           yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Salary (USD)"))
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-header">Full Summary Table</div>', unsafe_allow_html=True)
    tbl = filt.groupby("Job_Title").agg(Industry=("Industry","first"),
        Avg_Risk=("Automation_Risk","mean"),Avg_Salary=("Salary_USD","mean"),
        Skill_Score=("Skill_Score","mean"),AI_Adoption=("AI_Adoption","first"),
        Degree=("Degree_Required","first"),Growth=("Job_Growth","first"),
        Company_Size=("Company_Size","first")).reset_index().sort_values("Avg_Risk",ascending=False)
    tbl["Avg_Risk"]   = tbl["Avg_Risk"].round(1)
    tbl["Avg_Salary"] = tbl["Avg_Salary"].apply(lambda x:f"${x:,.0f}")
    tbl["Skill_Score"]= tbl["Skill_Score"].round(1)
    st.dataframe(tbl, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — SKILLS VS DEGREE
# ══════════════════════════════════════════════════════════════════════════════
elif "Skills vs" in page:
    st.markdown('<h2 style="color:#a78bfa;">⚖️ Skills vs Degree Analysis</h2>', unsafe_allow_html=True)
    st.markdown("Does a degree protect you from AI automation — or is your skill set what really matters?")

    col_a,col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-header">Automation Risk: Degree vs No Degree</div>', unsafe_allow_html=True)
        dr = df.groupby("Degree_Required")["Automation_Risk"].agg(["mean","std"]).reset_index()
        fig = px.bar(dr,x="Degree_Required",y="mean",error_y="std",color="Degree_Required",
                     color_discrete_map={"Yes":"#7c3aed","No":"#f64f59"},
                     text=[f"{v:.1f}%" for v in dr["mean"]],
                     labels={"mean":"Avg Risk (%)","Degree_Required":"Degree Required"})
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                          height=300,showlegend=False,yaxis=dict(showgrid=True,gridcolor="#2d3748"))
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        t,p = stats.ttest_ind(df[df["Degree_Required"]=="Yes"]["Automation_Risk"],
                               df[df["Degree_Required"]=="No"]["Automation_Risk"])
        st.markdown(f"""<div class='info-card'><b style='color:#a78bfa;'>📐 T-Test: Risk by Degree</b><br><br>
        t = {t:.4f} &nbsp;|&nbsp; p = {p:.6f}<br><br>
        {'✅ <b style="color:#00c853;">Significant</b> — degree impacts risk (p < 0.05)' if p<0.05
         else '❌ No significant difference (p ≥ 0.05)'}</div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-header">Salary: Degree vs No Degree</div>', unsafe_allow_html=True)
        fig2 = px.box(df,x="Degree_Required",y="Salary_USD",color="Degree_Required",points=False,
                      color_discrete_map={"Yes":"#7c3aed","No":"#f64f59"})
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                           height=300,showlegend=False,xaxis_title="Degree Required",
                           yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Salary (USD)"))
        st.plotly_chart(fig2, use_container_width=True)
        t2,p2 = stats.ttest_ind(df[df["Degree_Required"]=="Yes"]["Salary_USD"],
                                  df[df["Degree_Required"]=="No"]["Salary_USD"])
        st.markdown(f"""<div class='info-card'><b style='color:#a78bfa;'>📐 T-Test: Salary by Degree</b><br><br>
        t = {t2:.4f} &nbsp;|&nbsp; p = {p2:.6f}<br><br>
        {'✅ <b style="color:#00c853;">Degree holders earn significantly more</b>' if p2<0.05
         else '❌ No significant salary difference'}</div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Skill Score vs Automation Risk (with Trend Lines)</div>', unsafe_allow_html=True)
    samp = df.sample(min(1500,len(df)),random_state=1)
    fig3 = px.scatter(samp,x="Skill_Score",y="Automation_Risk",color="Degree_Required",opacity=0.5,
                      trendline="ols",color_discrete_map={"Yes":"#7c3aed","No":"#f64f59"},
                      labels={"Skill_Score":"Skill Score (%)","Automation_Risk":"Automation Risk (%)"})
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",height=360,
                       xaxis=dict(showgrid=True,gridcolor="#2d3748"),yaxis=dict(showgrid=True,gridcolor="#2d3748"))
    st.plotly_chart(fig3, use_container_width=True)

    corr = df["Skill_Score"].corr(df["Automation_Risk"])
    st.markdown(f"""<div class='info-card'><b style='color:#a78bfa;'>🔗 Pearson Correlation: Skill Score ↔ Risk</b><br><br>
    r = <b style='color:{"#00c853" if corr<0 else "#ff4b4b"};'>{corr:.4f}</b>&nbsp;&nbsp;
    {'📉 Higher skills → lower risk. Skills DO protect careers!' if corr<0 else '📈 Positive correlation.'}
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Risk by AI Adoption × Degree</div>', unsafe_allow_html=True)
    grp = df.groupby(["AI_Adoption","Degree_Required"])["Automation_Risk"].mean().reset_index()
    fig4 = px.bar(grp,x="AI_Adoption",y="Automation_Risk",color="Degree_Required",barmode="group",
                  color_discrete_map={"Yes":"#7c3aed","No":"#f64f59"},
                  category_orders={"AI_Adoption":["Low","Medium","High"]})
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",height=320,
                       xaxis=dict(showgrid=False),yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Avg Risk (%)"))
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — GLOBAL & COMPANY VIEW
# ══════════════════════════════════════════════════════════════════════════════
elif "Global" in page:
    st.markdown('<h2 style="color:#a78bfa;">🌍 Global & Company View</h2>', unsafe_allow_html=True)
    st.markdown("How does automation risk vary across global cities and company sizes?")

    col_a,col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-header">Automation Risk by City</div>', unsafe_allow_html=True)
        city = df.groupby("Location")["Automation_Risk"].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(city,x="Location",y="Automation_Risk",color="Automation_Risk",
                     color_continuous_scale="RdYlGn_r",text=[f"{v:.1f}%" for v in city["Automation_Risk"]])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                          height=340,coloraxis_showscale=False,xaxis=dict(showgrid=False,tickangle=-30),
                          yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Avg Risk (%)"))
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.markdown('<div class="section-header">Average Salary by City</div>', unsafe_allow_html=True)
        sal_city = df.groupby("Location")["Salary_USD"].mean().sort_values(ascending=False).reset_index()
        fig2 = px.bar(sal_city,x="Location",y="Salary_USD",color="Salary_USD",
                      color_continuous_scale="Purples",text=[f"${v:,.0f}" for v in sal_city["Salary_USD"]])
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                           height=340,coloraxis_showscale=False,xaxis=dict(showgrid=False,tickangle=-30),
                           yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Avg Salary (USD)"))
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

    col_c,col_d = st.columns(2)
    with col_c:
        st.markdown('<div class="section-header">Automation Risk by Company Size</div>', unsafe_allow_html=True)
        cs = df.groupby("Company_Size")["Automation_Risk"].mean().reset_index()
        fig3 = px.bar(cs,x="Company_Size",y="Automation_Risk",color="Company_Size",
                      color_discrete_map={"Small":"#f64f59","Medium":"#ffa500","Large":"#7c3aed"},
                      text=[f"{v:.1f}%" for v in cs["Automation_Risk"]])
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                           height=300,showlegend=False,xaxis=dict(showgrid=False),
                           yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Avg Risk (%)"))
        fig3.update_traces(textposition="outside")
        st.plotly_chart(fig3, use_container_width=True)
    with col_d:
        st.markdown('<div class="section-header">Salary by Company Size</div>', unsafe_allow_html=True)
        fig4 = px.box(df,x="Company_Size",y="Salary_USD",color="Company_Size",points=False,
                      color_discrete_map={"Small":"#f64f59","Medium":"#ffa500","Large":"#7c3aed"})
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                           height=300,showlegend=False,xaxis=dict(showgrid=False),
                           yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Salary (USD)"))
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-header">Risk Heatmap: City × Industry</div>', unsafe_allow_html=True)
    heat = df.groupby(["Location","Industry"])["Automation_Risk"].mean().reset_index()
    pvt  = heat.pivot(index="Industry",columns="Location",values="Automation_Risk")
    fig5 = px.imshow(pvt,color_continuous_scale="RdYlGn_r",aspect="auto",labels=dict(color="Risk (%)"))
    fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                       height=500,margin=dict(l=160,r=20,t=20,b=20))
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown('<div class="section-header">Top 20 In-Demand Skills</div>', unsafe_allow_html=True)
    sk_all = df["Skills"].dropna().str.split(", ").explode()
    sk_cnt = sk_all.value_counts().head(20).reset_index()
    sk_cnt.columns = ["Skill","Count"]
    fig6 = px.bar(sk_cnt,x="Count",y="Skill",orientation="h",color="Count",color_continuous_scale="Purples")
    fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                       height=520,coloraxis_showscale=False,margin=dict(l=160,r=20,t=20,b=20),
                       xaxis=dict(showgrid=True,gridcolor="#2d3748"),yaxis=dict(showgrid=False))
    st.plotly_chart(fig6, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — TREND ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif "Trend" in page:
    st.markdown('<h2 style="color:#a78bfa;">📈 Trend Analysis (2020–2024)</h2>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Automation Risk Trend by Industry</div>', unsafe_allow_html=True)
    yr = df.groupby(["Year","Industry"])["Automation_Risk"].mean().reset_index()
    fig = px.line(yr,x="Year",y="Automation_Risk",color="Industry",markers=True,
                  color_discrete_sequence=px.colors.qualitative.Vivid)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",height=420,
                      xaxis=dict(showgrid=True,gridcolor="#2d3748",dtick=1),
                      yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Avg Risk (%)"))
    fig.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig, use_container_width=True)

    col_a,col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-header">Remote Work Growth Over Time</div>', unsafe_allow_html=True)
        rem = df.groupby("Year").apply(lambda x:(x["Remote_Work"]=="Yes").mean()*100,
                                        include_groups=False).reset_index(name="Pct")
        fig2 = px.area(rem,x="Year",y="Pct",color_discrete_sequence=["#7c3aed"])
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                           height=280,xaxis=dict(showgrid=True,gridcolor="#2d3748",dtick=1),
                           yaxis=dict(showgrid=True,gridcolor="#2d3748",title="% Remote Jobs"))
        fig2.update_traces(fillcolor="rgba(124,58,237,0.2)")
        st.plotly_chart(fig2, use_container_width=True)
    with col_b:
        st.markdown('<div class="section-header">Average Salary by Year</div>', unsafe_allow_html=True)
        sal = df.groupby("Year")["Salary_USD"].mean().reset_index()
        fig3 = px.bar(sal,x="Year",y="Salary_USD",color_discrete_sequence=["#f64f59"],
                      text=[f"${v:,.0f}" for v in sal["Salary_USD"]])
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                           height=280,xaxis=dict(showgrid=False,dtick=1),
                           yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Avg Salary (USD)"))
        fig3.update_traces(textposition="outside")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-header">Automation Risk Heatmap: Job × Year</div>', unsafe_allow_html=True)
    ht  = df.groupby(["Job_Title","Year"])["Automation_Risk"].mean().reset_index()
    pvt = ht.pivot(index="Job_Title",columns="Year",values="Automation_Risk")
    fig4 = px.imshow(pvt,color_continuous_scale="RdYlGn_r",aspect="auto",labels=dict(color="Risk (%)"))
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                       height=580,margin=dict(l=180,r=20,t=20,b=20))
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-header">Job Demand Index by AI Adoption Level</div>', unsafe_allow_html=True)
    dem = df.groupby(["Year","AI_Adoption"])["Job_Demand_Index"].mean().reset_index()
    fig5 = px.line(dem,x="Year",y="Job_Demand_Index",color="AI_Adoption",markers=True,
                   color_discrete_map={"High":"#ff4b4b","Medium":"#ffa500","Low":"#00c853"})
    fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",height=320,
                       xaxis=dict(showgrid=True,gridcolor="#2d3748",dtick=1),
                       yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Demand Index"))
    fig5.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig5, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — STATISTICAL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif "Statistical" in page:
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score, mean_absolute_error
    from sklearn.preprocessing import LabelEncoder

    st.markdown('<h2 style="color:#a78bfa;">📊 Statistical Analysis</h2>', unsafe_allow_html=True)
    tab1,tab2,tab3,tab4 = st.tabs(["📋 Descriptive","📏 Confidence Intervals","🎲 Probability","📉 Regression"])

    with tab1:
        st.markdown('<div class="section-header">Descriptive Statistics</div>', unsafe_allow_html=True)
        desc = df[["Automation_Risk","Salary_USD","Skill_Score","Experience_Years","Job_Demand_Index"]].describe().T
        desc.columns=["Count","Mean","Std Dev","Min","Q1","Median","Q3","Max"]
        st.dataframe(desc.round(2), use_container_width=True)

        var = st.selectbox("Variable for Distribution",["Automation_Risk","Salary_USD","Skill_Score","Experience_Years"])
        show_norm = st.checkbox("Overlay Normal Distribution",value=True)
        dcol = df[var].dropna()
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=dcol,nbinsx=30,name="Observed",marker_color="#7c3aed",
                                    opacity=0.7,histnorm="probability density"))
        if show_norm:
            mu,sig = dcol.mean(),dcol.std()
            xr = np.linspace(dcol.min(),dcol.max(),200)
            fig.add_trace(go.Scatter(x=xr,y=stats.norm.pdf(xr,mu,sig),mode="lines",
                                     name="Normal Fit",line=dict(color="#f64f59",width=2.5)))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                          height=340,xaxis=dict(showgrid=True,gridcolor="#2d3748"),
                          yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Density"))
        st.plotly_chart(fig, use_container_width=True)
        _,pn = stats.shapiro(dcol.sample(min(500,len(dcol)),random_state=42))
        sk,ku = dcol.skew(),dcol.kurtosis()
        st.markdown(f"""<div class='info-card'><b style='color:#a78bfa;'>Shapiro-Wilk — {var}</b><br><br>
        p={pn:.6f} | Skewness={sk:.4f} | Kurtosis={ku:.4f}<br><br>
        {'✅ <b style="color:#00c853;">Normally distributed</b>' if pn>=0.05
         else '❌ <b style="color:#ff4b4b;">Not normally distributed</b>'} (p {'≥' if pn>=0.05 else '<'} 0.05)
        </div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-header">95% Confidence Intervals by Industry</div>', unsafe_allow_html=True)
        ci_var = st.selectbox("Variable",["Automation_Risk","Salary_USD","Skill_Score"])
        ci_rows = []
        for ind,grp in df.groupby("Industry"):
            d=grp[ci_var].dropna(); n=len(d); mu=d.mean(); se=stats.sem(d)
            lo,hi=stats.t.interval(0.95,df=n-1,loc=mu,scale=se)
            ci_rows.append({"Industry":ind,"Mean":mu,"CI_Low":lo,"CI_High":hi,"n":n})
        ci_df = pd.DataFrame(ci_rows).sort_values("Mean")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ci_df["Mean"],y=ci_df["Industry"],mode="markers",
                                  marker=dict(size=10,color="#7c3aed"),
                                  error_x=dict(type="data",array=ci_df["CI_High"]-ci_df["Mean"],
                                               arrayminus=ci_df["Mean"]-ci_df["CI_Low"],
                                               color="#a78bfa",thickness=2,width=6)))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                          height=440,xaxis=dict(showgrid=True,gridcolor="#2d3748",title=ci_var),
                          yaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(ci_df.round(2), use_container_width=True, hide_index=True)

    with tab3:
        st.markdown('<div class="section-header">Risk Category Probability</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            cat_c = df["Automation_Risk_Cat"].value_counts()
            fig = px.pie(values=cat_c.values,names=cat_c.index,hole=0.45,color=cat_c.index,
                         color_discrete_map={"Low":"#00c853","Medium":"#ffa500","High":"#ff4b4b"})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",height=300)
            fig.update_traces(textinfo="label+percent")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            thr = st.slider("Risk Threshold (%)",10,90,60,5)
            pa  = (df["Automation_Risk"]>=thr).mean()*100
            mu_r,sig_r = df["Automation_Risk"].mean(),df["Automation_Risk"].std()
            pna = (1-stats.norm.cdf(thr,mu_r,sig_r))*100
            st.markdown(f"""<div class='info-card' style='margin-top:10px;'>
            <b style='color:#a78bfa;'>P(Risk ≥ {thr}%) Empirical</b><br>
            <span style='font-size:2.2rem;color:#ff4b4b;font-weight:800;'>{pa:.1f}%</span><br><br>
            <b style='color:#a78bfa;'>P(X ≥ {thr}%) Normal Approx</b><br>
            <span style='font-size:2.2rem;color:#ffa500;font-weight:800;'>{pna:.1f}%</span><br><br>
            <i style='color:#64748b;'>μ={mu_r:.2f}, σ={sig_r:.2f}</i>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header">P(High Risk | Industry)</div>', unsafe_allow_html=True)
        cond = df.groupby("Industry").apply(lambda x:(x["Automation_Risk"]>=60).mean()*100,
                                             include_groups=False).reset_index(name="P_High").sort_values("P_High",ascending=False)
        fig2 = px.bar(cond,x="Industry",y="P_High",color="P_High",color_continuous_scale="RdYlGn_r",
                      text=[f"{v:.1f}%" for v in cond["P_High"]])
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                           height=340,coloraxis_showscale=False,xaxis=dict(showgrid=False,tickangle=-30),
                           yaxis=dict(showgrid=True,gridcolor="#2d3748",title="P(High Risk) %"))
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="section-header">P(Growth | Company Size)</div>', unsafe_allow_html=True)
        cond2 = df.groupby("Company_Size").apply(lambda x:(x["Job_Growth"]=="Growth").mean()*100,
                                                   include_groups=False).reset_index(name="P_Growth")
        fig3 = px.bar(cond2,x="Company_Size",y="P_Growth",color="Company_Size",
                      color_discrete_map={"Small":"#f64f59","Medium":"#ffa500","Large":"#7c3aed"},
                      text=[f"{v:.1f}%" for v in cond2["P_Growth"]])
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                           height=280,showlegend=False,xaxis=dict(showgrid=False),
                           yaxis=dict(showgrid=True,gridcolor="#2d3748",title="P(Growth) %"))
        fig3.update_traces(textposition="outside")
        st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        st.markdown('<div class="section-header">Regression: Predicting Automation Risk</div>', unsafe_allow_html=True)
        rdf = df.copy()
        encs = {}
        for col in ["Degree_Required","AI_Adoption","Remote_Work","Job_Growth","Company_Size"]:
            le = LabelEncoder(); rdf[col+"_enc"]=le.fit_transform(rdf[col].fillna("Unknown")); encs[col]=le
        feats = ["Skill_Score","Salary_USD","Experience_Years","Degree_Required_enc",
                 "AI_Adoption_enc","Remote_Work_enc","Job_Growth_enc","Company_Size_enc","Year","Job_Demand_Index"]
        X=rdf[feats].dropna(); y=rdf.loc[X.index,"Automation_Risk"]
        Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=0.2,random_state=42)

        col1,col2 = st.columns(2)
        with col1:
            st.markdown("**📏 Linear Regression**")
            lr=LinearRegression().fit(Xtr,ytr); yp=lr.predict(Xte)
            r2=r2_score(yte,yp); mae=mean_absolute_error(yte,yp)
            fig=px.scatter(x=yte,y=yp,opacity=0.4,color_discrete_sequence=["#7c3aed"],
                           labels={"x":"Actual (%)","y":"Predicted (%)"})
            fig.add_shape(type="line",x0=5,y0=5,x1=98,y1=98,line=dict(color="#f64f59",dash="dash"))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                              height=300,xaxis=dict(showgrid=True,gridcolor="#2d3748"),
                              yaxis=dict(showgrid=True,gridcolor="#2d3748"))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"<div class='info-card'><b>R²:</b> {r2:.4f}<br><b>MAE:</b> {mae:.2f}%</div>",unsafe_allow_html=True)
        with col2:
            st.markdown("**🌲 Random Forest Regression**")
            rf=RandomForestRegressor(n_estimators=100,random_state=42).fit(Xtr,ytr); yp2=rf.predict(Xte)
            r2b=r2_score(yte,yp2); mae2=mean_absolute_error(yte,yp2)
            fig2=px.scatter(x=yte,y=yp2,opacity=0.4,color_discrete_sequence=["#f64f59"],
                            labels={"x":"Actual (%)","y":"Predicted (%)"})
            fig2.add_shape(type="line",x0=5,y0=5,x1=98,y1=98,line=dict(color="#7c3aed",dash="dash"))
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                               height=300,xaxis=dict(showgrid=True,gridcolor="#2d3748"),
                               yaxis=dict(showgrid=True,gridcolor="#2d3748"))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown(f"<div class='info-card'><b>R²:</b> {r2b:.4f}<br><b>MAE:</b> {mae2:.2f}%<br>"
                        f"<b>Better:</b> {'🌲 Random Forest' if r2b>r2 else '📏 Linear Reg'}</div>",unsafe_allow_html=True)

        st.markdown('<div class="section-header">Feature Importance (Random Forest)</div>', unsafe_allow_html=True)
        imp=pd.DataFrame({"Feature":feats,"Importance":rf.feature_importances_}).sort_values("Importance")
        fig3=px.bar(imp,x="Importance",y="Feature",orientation="h",color="Importance",
                    color_continuous_scale="Purples",text=[f"{v:.3f}" for v in imp["Importance"]])
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                           height=400,coloraxis_showscale=False,margin=dict(l=180),
                           xaxis=dict(showgrid=True,gridcolor="#2d3748"),yaxis=dict(showgrid=False))
        fig3.update_traces(textposition="outside")
        st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — AI RISK PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
elif "Predictor" in page:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import LabelEncoder

    st.markdown('<h2 style="color:#a78bfa;">🔮 AI Risk Predictor</h2>', unsafe_allow_html=True)
    st.markdown("Enter your profile — our Random Forest model will predict your automation risk.")

    @st.cache_resource
    def train_model(n):
        _df=df.copy(); encs={}
        for col in ["Degree_Required","AI_Adoption","Remote_Work","Job_Growth","Company_Size"]:
            le=LabelEncoder(); _df[col+"_enc"]=le.fit_transform(_df[col].fillna("Unknown")); encs[col]=le
        feats=["Skill_Score","Salary_USD","Experience_Years","Degree_Required_enc",
               "AI_Adoption_enc","Remote_Work_enc","Job_Growth_enc","Company_Size_enc","Year","Job_Demand_Index"]
        X=_df[feats].dropna(); y=_df.loc[X.index,"Automation_Risk"]
        rf=RandomForestRegressor(n_estimators=120,random_state=42).fit(X,y)
        return rf,encs

    model,encoders = train_model(len(df))

    col_in,col_out = st.columns([1,1])
    with col_in:
        st.markdown('<div class="section-header">Your Job Profile</div>', unsafe_allow_html=True)
        skill   = st.slider("🧠 Skill Score (%)",10,100,65)
        sal     = st.number_input("💰 Expected Salary (USD)",25000,300000,70000,5000)
        exp     = st.slider("📅 Years of Experience",0,20,3)
        deg     = st.selectbox("🎓 Degree Required?",["Yes","No"])
        ai      = st.selectbox("🤖 AI Adoption in Field",["High","Medium","Low"])
        rem     = st.selectbox("🏠 Remote Work?",["Yes","No"])
        growth  = st.selectbox("🌱 Job Growth Outlook",["Growth","Stable","Decline"])
        csize   = st.selectbox("🏢 Company Size",["Large","Medium","Small"])
        demand  = st.slider("📈 Job Demand Index",20,120,70)
        go_btn  = st.button("🔮 Predict My Risk",use_container_width=True,type="primary")

    with col_out:
        st.markdown('<div class="section-header">Result</div>', unsafe_allow_html=True)
        if go_btn:
            inp=[[skill,sal,exp,
                  encoders["Degree_Required"].transform([deg])[0],
                  encoders["AI_Adoption"].transform([ai])[0],
                  encoders["Remote_Work"].transform([rem])[0],
                  encoders["Job_Growth"].transform([growth])[0],
                  encoders["Company_Size"].transform([csize])[0],
                  2024,demand]]
            risk=float(np.clip(model.predict(inp)[0],5,98))
            if risk>=65:   lvl,col,em="HIGH","#ff4b4b","🔴"; msg="⚠️ High risk. Focus on <b>AI-augmentation & soft skills</b>."
            elif risk>=35: lvl,col,em="MEDIUM","#ffa500","🟡"; msg="⚡ Moderate risk. Stay updated with industry AI tools."
            else:          lvl,col,em="LOW","#00c853","🟢"; msg="✅ Relatively safe. Keep building domain expertise."
            st.markdown(f"""
            <div style='text-align:center;background:linear-gradient(135deg,#1e2535,#252d40);
                        border:2px solid {col}55;border-radius:18px;padding:30px 20px;margin-bottom:14px;'>
                <div style='font-size:3rem;'>{em}</div>
                <div style='font-size:.9rem;color:#94a3b8;'>Predicted Automation Risk</div>
                <div style='font-size:4rem;font-weight:900;color:{col};'>{risk:.1f}%</div>
                <div style='font-size:.95rem;font-weight:700;color:{col};background:{col}22;
                            border-radius:20px;padding:3px 16px;display:inline-block;margin-top:6px;'>{lvl} RISK</div>
            </div>
            <div class='info-card'>{msg}</div>""", unsafe_allow_html=True)
            fig=go.Figure(go.Indicator(mode="gauge+number",value=risk,
                title={"text":"Automation Risk %","font":{"color":"#cbd5e1"}},
                gauge={"axis":{"range":[0,100],"tickcolor":"#cbd5e1"},"bar":{"color":col},
                       "bgcolor":"#1e2535",
                       "steps":[{"range":[0,35],"color":"#00c85322"},{"range":[35,65],"color":"#ffa50022"},
                                 {"range":[65,100],"color":"#ff4b4b22"}],
                       "threshold":{"line":{"color":"white","width":3},"thickness":0.75,"value":risk}}))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                              height=250,margin=dict(l=20,r=20,t=40,b=10))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""<div style='text-align:center;padding:60px 20px;color:#475569;'>
                <div style='font-size:3rem;margin-bottom:12px;'>🔮</div>
                Fill your profile and click <b style='color:#7c3aed;'>Predict My Risk</b>
                </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Industry Averages — How Do You Compare?</div>', unsafe_allow_html=True)
    ia=df.groupby("Industry")["Automation_Risk"].mean().reset_index().sort_values("Automation_Risk")
    fig_c=px.bar(ia,x="Industry",y="Automation_Risk",color="Automation_Risk",
                 color_continuous_scale="RdYlGn_r",text=[f"{v:.1f}%" for v in ia["Automation_Risk"]])
    fig_c.add_hline(y=df["Automation_Risk"].mean(),line_dash="dash",line_color="#a78bfa",
                    annotation_text=f"Overall Avg: {df['Automation_Risk'].mean():.1f}%",
                    annotation_font_color="#a78bfa")
    fig_c.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#cbd5e1",
                        height=340,coloraxis_showscale=False,xaxis=dict(showgrid=False,tickangle=-30),
                        yaxis=dict(showgrid=True,gridcolor="#2d3748",title="Avg Risk (%)"))
    fig_c.update_traces(textposition="outside")
    st.plotly_chart(fig_c, use_container_width=True)