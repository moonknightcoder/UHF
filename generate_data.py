import pandas as pd
import numpy as np

np.random.seed(42)

# --- Job definitions with realistic attributes ---
job_profiles = [
    # (title, industry, base_risk, ai_adoption, degree_required, base_salary, skills)
    ("Data Scientist",        "Technology",      25, "High",   True,  95000, ["Python","ML","Statistics","SQL","TensorFlow"]),
    ("ML Engineer",           "Technology",      20, "High",   True,  110000,["Python","Deep Learning","MLOps","Docker","Kubernetes"]),
    ("Software Developer",    "Technology",      30, "High",   True,  90000, ["Python","Java","Git","Algorithms","APIs"]),
    ("Data Analyst",          "Finance",         40, "Medium", False, 70000, ["Excel","SQL","Python","Tableau","Statistics"]),
    ("Accountant",            "Finance",         72, "Medium", True,  65000, ["Excel","Accounting","QuickBooks","Auditing","Tax"]),
    ("Financial Analyst",     "Finance",         55, "Medium", True,  80000, ["Excel","Financial Modeling","SQL","Bloomberg","CFA"]),
    ("Graphic Designer",      "Media",           38, "Low",    False, 55000, ["Photoshop","Illustrator","Figma","Creativity","Branding"]),
    ("Content Writer",        "Media",           75, "High",   False, 45000, ["Writing","SEO","Research","WordPress","Editing"]),
    ("Digital Marketer",      "Marketing",       50, "Medium", False, 60000, ["SEO","Google Ads","Analytics","Social Media","Email"]),
    ("HR Manager",            "Human Resources", 45, "Low",    True,  68000, ["Recruitment","HRIS","Communication","Leadership","Labor Law"]),
    ("Customer Support Rep",  "Services",        80, "High",   False, 38000, ["Communication","CRM","Problem Solving","Patience","Ticketing"]),
    ("Truck Driver",          "Logistics",       85, "Medium", False, 48000, ["Driving","Navigation","Safety","Logistics","CDL"]),
    ("Nurse",                 "Healthcare",      15, "Low",    True,  75000, ["Patient Care","EMR","Clinical Skills","Empathy","Medication"]),
    ("Doctor",                "Healthcare",       8, "Low",    True,  180000,["Diagnosis","Surgery","EMR","Research","Communication"]),
    ("Teacher",               "Education",       30, "Low",    True,  52000, ["Curriculum","Communication","EdTech","Patience","Assessment"]),
    ("Legal Advisor",         "Legal",           35, "Low",    True,  120000,["Legal Research","Contracts","Communication","Negotiation","Compliance"]),
    ("Paralegal",             "Legal",           62, "Medium", False, 55000, ["Legal Research","Documentation","MS Office","Filing","Compliance"]),
    ("Cybersecurity Analyst", "Technology",      18, "High",   True,  100000,["Network Security","Python","Ethical Hacking","SIEM","Firewalls"]),
    ("DevOps Engineer",       "Technology",      22, "High",   True,  105000,["Docker","Kubernetes","CI/CD","Linux","Cloud"]),
    ("AI Researcher",         "Technology",      10, "High",   True,  130000,["Python","Deep Learning","Research","Mathematics","PyTorch"]),
    ("Bank Teller",           "Finance",         88, "High",   False, 36000, ["Cash Handling","Customer Service","MS Office","Accuracy","Banking"]),
    ("Radiologist",           "Healthcare",      28, "High",   True,  250000,["Medical Imaging","Diagnosis","AI Tools","Clinical Skills","Anatomy"]),
    ("Journalist",            "Media",           42, "Medium", True,  50000, ["Writing","Research","Interviewing","SEO","Editing"]),
    ("Supply Chain Manager",  "Logistics",       48, "Medium", True,  85000, ["ERP","Analytics","Negotiation","SAP","Forecasting"]),
    ("Retail Cashier",        "Retail",          90, "High",   False, 30000, ["Customer Service","Cash Handling","POS Systems","Inventory","Sales"]),
    ("Civil Engineer",        "Engineering",     20, "Low",    True,  85000, ["AutoCAD","Project Management","Structural Analysis","Math","CAD"]),
    ("Electrician",           "Engineering",     15, "Low",    False, 60000, ["Wiring","Safety","Troubleshooting","NEC","Blueprint Reading"]),
    ("Psychologist",          "Healthcare",      12, "Low",    True,  85000, ["Therapy","Assessment","Counseling","Research","Empathy"]),
    ("UX Designer",           "Technology",      28, "Medium", False, 88000, ["Figma","User Research","Prototyping","CSS","Accessibility"]),
    ("Product Manager",       "Technology",      22, "Medium", True,  115000,["Roadmapping","Agile","Analytics","Communication","Jira"]),
]

records = []
years = [2020, 2021, 2022, 2023, 2024]

for year in years:
    for profile in job_profiles:
        title, industry, base_risk, ai_adopt, degree, base_sal, skills = profile
        n = np.random.randint(35, 65)
        for _ in range(n):
            # Risk increases slightly year over year
            risk_delta = (year - 2020) * np.random.uniform(0.5, 2.0)
            automation_risk = min(98, base_risk + risk_delta + np.random.normal(0, 5))
            automation_risk = max(5, automation_risk)

            # Salary with noise + slight growth
            sal_growth = (year - 2020) * 0.025
            salary = int(base_sal * (1 + sal_growth) + np.random.normal(0, base_sal * 0.10))
            salary = max(28000, salary)

            # Experience
            experience = max(0, int(np.random.normal(5, 3)))

            # Number of skills known (more skills = lower risk)
            skills_known = np.random.randint(2, len(skills) + 1)
            skill_score = round((skills_known / len(skills)) * 100, 1)

            # Remote work probability increases after 2020
            remote_prob = 0.2 + (year - 2020) * 0.07
            remote = np.random.choice(["Yes", "No"], p=[min(remote_prob, 0.65), max(1 - remote_prob, 0.35)])

            # Job demand trend (based on AI adoption)
            demand_map = {"High": [80, 120], "Medium": [50, 90], "Low": [30, 70]}
            lo, hi = demand_map[ai_adopt]
            job_demand_index = round(np.random.uniform(lo, hi), 1)

            records.append({
                "Year":               year,
                "Job_Title":          title,
                "Industry":           industry,
                "Automation_Risk":    round(automation_risk, 1),
                "AI_Adoption":        ai_adopt,
                "Degree_Required":    "Yes" if degree else "No",
                "Salary_USD":         salary,
                "Experience_Years":   experience,
                "Skill_Score":        skill_score,
                "Remote_Work":        remote,
                "Job_Demand_Index":   job_demand_index,
                "Skills":             ", ".join(np.random.choice(skills, skills_known, replace=False)),
            })

df = pd.DataFrame(records)
df.to_csv("/home/claude/ai_jobs_project/data/ai_job_market.csv", index=False)
print(f"Dataset created: {len(df)} rows, {df.shape[1]} columns")
print(df.dtypes)
print(df.head(3))
