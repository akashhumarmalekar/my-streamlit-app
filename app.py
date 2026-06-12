
import streamlit as st
import pandas as pd
import json, os
from datetime import datetime, date
from collections import defaultdict
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(
    page_title="Swami Shreeji Attendance",
    page_icon="🙏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── MASTER DB ────────────────────────────────────────────────────────────────
MASTER = [
  {"name":"Abhay Ramesh Kotadiya","followup":"Yash Kaila","contact":"8928478896"},
  {"name":"Abhishek Bhagwan Mukhiya","followup":"Aditya Shrotriya","contact":"9892003415"},
  {"name":"Adarsh Murli Tilwani","followup":"Dhaval Chhaya","contact":"7984551596"},
  {"name":"Aditya Piyush Shrotriya","followup":"Vinit Hindocha","contact":"8879823171"},
  {"name":"Ajay Pravin Savaliya","followup":"Yash Kaila","contact":"9324558759"},
  {"name":"Akash Jayesh Humarmalekar","followup":"Vinit Hindocha","contact":"9930237099"},
  {"name":"Akshay Suresh Rao","followup":"Akash Humarmalekar","contact":"9699901501"},
  {"name":"Amit Ravindra Bhalala","followup":"Bhavyam Bhalala","contact":"7506028391"},
  {"name":"Amol Dilip Patil","followup":"Brijesh Mehta","contact":"9224496320"},
  {"name":"Anand Kishorbhai Shah","followup":"Bhavyam Bhalala","contact":"9594840439"},
  {"name":"Anand Sanjay Ramani","followup":"Brijesh Mehta","contact":"9769853819"},
  {"name":"Aniket Suresh Kharat","followup":"Aditya Shrotriya","contact":"7021538560"},
  {"name":"Anish Ratilal Parmar","followup":"Dhaval Chhaya","contact":"7715856562"},
  {"name":"Ankit Rajeshbhai Panchal","followup":"Akash Humarmalekar","contact":"9137049786"},
  {"name":"Ansh Sunil Parmar","followup":"Yash Kaila","contact":"8369993718"},
  {"name":"Arjun Natvar Ladva","followup":"Suvas Waghela","contact":"9137186952"},
  {"name":"Arjun Rameshbhai Ahir","followup":"Pawan Rathod","contact":"9022800163"},
  {"name":"Arpit Manish Gupta","followup":"Akash Humarmalekar","contact":"7977028327"},
  {"name":"Arpit Sunil Kariya","followup":"Bhavyam Bhalala","contact":"9920492797"},
  {"name":"Aryan Suresh Rao","followup":"Akash Humarmalekar","contact":"9820049799"},
  {"name":"Ayush Suresh Suthar","followup":"Suresh Suthar","contact":"9892085989"},
  {"name":"Bhavesh Jaswant Rathod","followup":"Pawan Rathod","contact":"9619280290"},
  {"name":"Bhavyam Hitesh Bhalala","followup":"Bhavyam Bhalala","contact":"9920381996"},
  {"name":"Brijesh Bipin Mehta","followup":"Brijesh Mehta","contact":"9892001425"},
  {"name":"Chirag Manish Gupta","followup":"Akash Humarmalekar","contact":"9920616491"},
  {"name":"Chirag Vinod Rathod","followup":"Pawan Rathod","contact":"9930174018"},
  {"name":"Deep Jitendra Sanghvi","followup":"Bhavyam Bhalala","contact":"9833568087"},
  {"name":"Deval Deepak Panchal","followup":"Akash Humarmalekar","contact":"8779042116"},
  {"name":"Devam Rajesh Mehta","followup":"Brijesh Mehta","contact":"9004777085"},
  {"name":"Devang Paresh Mehta","followup":"Brijesh Mehta","contact":"9029273088"},
  {"name":"Dhaval Rajesh Chhaya","followup":"Dhaval Chhaya","contact":"9820266040"},
  {"name":"Dhruv Rajesh Parmar","followup":"Dhaval Chhaya","contact":"8291049789"},
  {"name":"Divyesh Bhupat Meva","followup":"Divyesh Meva","contact":"7045000065"},
  {"name":"Hardik Naresh Parmar","followup":"Dhaval Chhaya","contact":"7021484512"},
  {"name":"Hardik Prakash Bhalala","followup":"Bhavyam Bhalala","contact":"9004020248"},
  {"name":"Hardik Suresh Suthar","followup":"Suresh Suthar","contact":"9619048383"},
  {"name":"Harsh Ashok Shetty","followup":"Brijesh Mehta","contact":"9757818823"},
  {"name":"Harsh Manish Gupta","followup":"Akash Humarmalekar","contact":"9987878757"},
  {"name":"Harsh Nilesh Panchal","followup":"Akash Humarmalekar","contact":"9321148868"},
  {"name":"Himanshu Dinesh Panchal","followup":"Akash Humarmalekar","contact":"9819680226"},
  {"name":"Hitesh Mahesh Bhalala","followup":"Bhavyam Bhalala","contact":"9004191610"},
  {"name":"Ishan Sanjay Gupta","followup":"Akash Humarmalekar","contact":"9769501009"},
  {"name":"Jay Dinesh Parmar","followup":"Dhaval Chhaya","contact":"9004080789"},
  {"name":"Jay Jitendra Sanghvi","followup":"Bhavyam Bhalala","contact":"9833391726"},
  {"name":"Jay Ramesh Rathod","followup":"Pawan Rathod","contact":"9167088029"},
  {"name":"Jayesh Ashok Suthar","followup":"Suresh Suthar","contact":"9004023895"},
  {"name":"Jignesh Manish Gupta","followup":"Akash Humarmalekar","contact":"9920120032"},
  {"name":"Jinil Divyesh Meva","followup":"Divyesh Meva","contact":"9004124782"},
  {"name":"Karan Arun Nagpure","followup":"Aditya Shrotriya","contact":"9323472897"},
  {"name":"Karan Jayesh Panchal","followup":"Akash Humarmalekar","contact":"9004020190"},
  {"name":"Kashyap Mahesh Suthar","followup":"Suresh Suthar","contact":"8850062699"},
  {"name":"Kaushal Ramesh Yadav","followup":"Pawan Rathod","contact":"9137136584"},
  {"name":"Ketan Mahesh Suthar","followup":"Suresh Suthar","contact":"9004015987"},
  {"name":"Kiran Ramesh Makwana","followup":"Aditya Shrotriya","contact":"9321019785"},
  {"name":"Krish Jitendra Parmar","followup":"Dhaval Chhaya","contact":"9004188976"},
  {"name":"Krunal Suresh Suthar","followup":"Suresh Suthar","contact":"8879820998"},
  {"name":"Kunal Ramesh Rathod","followup":"Pawan Rathod","contact":"9137108922"},
  {"name":"Laxman Arjun Baria","followup":"Pawan Rathod","contact":"9892002187"},
  {"name":"Mahesh Ramesh Bhalala","followup":"Bhavyam Bhalala","contact":"9004191605"},
  {"name":"Manav Jitendra Parmar","followup":"Dhaval Chhaya","contact":"9819015786"},
  {"name":"Manish Anil Gupta","followup":"Akash Humarmalekar","contact":"9820280099"},
  {"name":"Meet Bhupat Paghdar","followup":"Divyesh Meva","contact":"9004165498"},
  {"name":"Mihir Rajesh Parmar","followup":"Dhaval Chhaya","contact":"9967184899"},
  {"name":"Moksh Ramesh Suthar","followup":"Suresh Suthar","contact":"9892033210"},
  {"name":"Neel Kamlesh Panchal","followup":"Akash Humarmalekar","contact":"9004019867"},
  {"name":"Neel Ramesh Rathod","followup":"Pawan Rathod","contact":"9004101987"},
  {"name":"Neil Rajesh Mehta","followup":"Brijesh Mehta","contact":"9004012345"},
  {"name":"Nikhil Rajesh Panchal","followup":"Akash Humarmalekar","contact":"9004175319"},
  {"name":"Nikunj Suresh Suthar","followup":"Suresh Suthar","contact":"9004067892"},
  {"name":"Nilesh Ramesh Bhalala","followup":"Bhavyam Bhalala","contact":"9004188901"},
  {"name":"Nishant Mahesh Gupta","followup":"Akash Humarmalekar","contact":"9004189212"},
  {"name":"Nishit Jayesh Panchal","followup":"Akash Humarmalekar","contact":"9004021578"},
  {"name":"Om Ramesh Rathod","followup":"Pawan Rathod","contact":"9004097865"},
  {"name":"Parth Ramesh Panchal","followup":"Akash Humarmalekar","contact":"9004012789"},
  {"name":"Pawan Nanjibhai Rathod","followup":"Pawan Rathod","contact":"9594803219"},
  {"name":"Pratik Suresh Suthar","followup":"Suresh Suthar","contact":"8879819876"},
  {"name":"Preet Ramesh Yadav","followup":"Pawan Rathod","contact":"9004099871"},
  {"name":"Raj Dinesh Parmar","followup":"Dhaval Chhaya","contact":"9004020671"},
  {"name":"Raj Jayesh Panchal","followup":"Akash Humarmalekar","contact":"9004201879"},
  {"name":"Rajat Suresh Rao","followup":"Akash Humarmalekar","contact":"9004099867"},
  {"name":"Rajesh Ramesh Suthar","followup":"Suresh Suthar","contact":"9004019872"},
  {"name":"Ravi Ramesh Yadav","followup":"Pawan Rathod","contact":"9004097123"},
  {"name":"Rishabh Rajesh Panchal","followup":"Akash Humarmalekar","contact":"9004011789"},
  {"name":"Ritik Suresh Gupta","followup":"Akash Humarmalekar","contact":"9004088761"},
  {"name":"Rohan Ramesh Rathod","followup":"Pawan Rathod","contact":"9004098731"},
  {"name":"Rohit Rajesh Panchal","followup":"Akash Humarmalekar","contact":"9004011289"},
  {"name":"Rushabh Ramesh Mehta","followup":"Brijesh Mehta","contact":"9004088871"},
  {"name":"Sahil Suresh Suthar","followup":"Suresh Suthar","contact":"9004011998"},
  {"name":"Sarthak Rajesh Panchal","followup":"Akash Humarmalekar","contact":"9004017819"},
  {"name":"Saurabh Ramesh Yadav","followup":"Pawan Rathod","contact":"9004091287"},
  {"name":"Shivam Suresh Gupta","followup":"Akash Humarmalekar","contact":"9004018831"},
  {"name":"Shubham Rajesh Suthar","followup":"Suresh Suthar","contact":"9004076891"},
  {"name":"Siddharth Ramesh Mehta","followup":"Brijesh Mehta","contact":"9004089012"},
  {"name":"Soham Rajesh Panchal","followup":"Akash Humarmalekar","contact":"9004201571"},
  {"name":"Sujal Suresh Suthar","followup":"Suresh Suthar","contact":"9004012209"},
  {"name":"Sunjay Arjun Ladva","followup":"Suvas Waghela","contact":"9930372149"},
  {"name":"Suresh Damodar Suthar","followup":"Vinit Hindocha","contact":"9326206944"},
  {"name":"Suvas Pravin Waghela","followup":"Vinit Hindocha","contact":"9869123499"},
  {"name":"Tanish Umesh Bhalala","followup":"Suresh Suthar","contact":"9321372159"},
  {"name":"Tirth Kiran Parmar","followup":"Aditya Shrotriya","contact":"9082080571"},
  {"name":"Tushar Amrit Ratda","followup":"Bhavyam Bhalala","contact":"9326157626"},
  {"name":"Tushar Manoj Gupta","followup":"Akash Humarmalekar","contact":"8850781764"},
  {"name":"Tushar Suresh Solanki","followup":"Suresh Suthar","contact":"8591250611"},
  {"name":"Umesh Dhanji Bhalala","followup":"Pawan Rathod","contact":"9920049046"},
  {"name":"Upendra Jagbir Yadav","followup":"Pawan Rathod","contact":"8652155775"},
  {"name":"Vedant Devang Mehta","followup":"Yash Kaila","contact":"7738699819"},
  {"name":"Veeresh Gaurav Lingayat","followup":"Aditya Shrotriya","contact":"9819616877"},
  {"name":"Vinit Sanjay Hindocha","followup":"Vinit Hindocha","contact":"9820198422"},
  {"name":"Viral Mahesh Makwana","followup":"Aditya Shrotriya","contact":"9137049891"},
  {"name":"Viren Ajit Delkar","followup":"Akash Humarmalekar","contact":"7021897552"},
  {"name":"Vivek Manoj Gupta","followup":"Akash Humarmalekar","contact":"7977461849"},
  {"name":"Vivek Murli Tilwani","followup":"Dhaval Chhaya","contact":"9867297978"},
  {"name":"Yakshit Mahendra Patel","followup":"Yash Kaila","contact":"9323484048"},
  {"name":"Yash Hari Soni","followup":"Dhaval Chhaya","contact":"9653149347"},
  {"name":"Yash Jayanti Kaila","followup":"Vinit Hindocha","contact":"9867778997"},
  {"name":"Yash Mitesh Bhatda","followup":"Akash Humarmalekar","contact":"8591847916"},
  {"name":"Yogesh Rajesh Kajale","followup":"Akash Humarmalekar","contact":"8928280032"},
  {"name":"Yug Prasad Shetty","followup":"Brijesh Mehta","contact":"9136567791"},
  {"name":"Rahul Vitthal Savalia","followup":"Dhaval Chhaya","contact":""},
  {"name":"Avinash Vinayak Kadam","followup":"Akash Humarmalekar","contact":""},
]

# ─── Data helpers ─────────────────────────────────────────────────────────────
DATA_FILE = "shreeji_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"history":[],"extra_members":[],"fp_overrides":{},
            "cat_overrides":{},"session_notes":{},"ref_overrides":{},
            "abs_reasons":{},"suppress_master":False}

def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def calc_category(name, history):
    sessions = [s for s in history if any(r["name"]==name for r in s["records"])]
    if not sessions: return "N"
    r4 = sessions[-4:]; r6 = sessions[-6:]
    a4 = sum(1 for s in r4 if any(r["name"]==name and r["status"]=="P" for r in s["records"]))
    a6 = sum(1 for s in r6 if any(r["name"]==name and r["status"]=="P" for r in s["records"]))
    if a4 >= 1: return "R"
    if a6 >= 1: return "I"
    return "N"

def get_cat(name, history, cat_ov):
    return cat_ov.get(name) or calc_category(name, history)

def get_all_members(d):
    master = [] if d.get("suppress_master") else [
        {"name":m["name"],"followup":d["fp_overrides"].get(m["name"],m["followup"]),
         "contact":m["contact"],"is_extra":False} for m in MASTER]
    extra = [
        {"name":m["name"],"followup":d["fp_overrides"].get(m["name"],m.get("followup","")),
         "contact":m.get("contact",""),"reference":m.get("reference",""),
         "is_extra":True} for m in d.get("extra_members",[])]
    return master + extra

def consec_absent(name, history):
    sessions = [s for s in history if any(r["name"]==name for r in s["records"])]
    c = 0
    for s in reversed(sessions):
        r = next((x for x in s["records"] if x["name"]==name), None)
        if r and r["status"]=="A": c += 1
        else: break
    return c

# ─── Init session state ───────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "att" not in st.session_state:
    st.session_state.att = {}
if "sess_date" not in st.session_state:
    st.session_state.sess_date = date.today().strftime("%d %b %Y")
if "sabha" not in st.session_state:
    st.session_state.sabha = "Weekly"

D = st.session_state.data
members = get_all_members(D)
fps_list = sorted(set(m["followup"] for m in members))

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🙏 Swami Shreeji")
    st.caption("Yuvak Attendance System")
    st.divider()
    st.session_state.sess_date = st.text_input("Session Date", st.session_state.sess_date)
    st.session_state.sabha = st.selectbox("Sabha Type",
        ["Weekly","Special","Monthly","Other"],
        index=["Weekly","Special","Monthly","Other"].index(st.session_state.sabha))
    st.divider()
    st.metric("Members", len(members))
    st.metric("Sessions", len(D["history"]))

# ─── Navigation via selectbox (crash-safe alternative to tabs) ────────────────
PAGES = ["📊 Dashboard","📋 Attendance","📈 Report","🕒 Historic",
         "📅 Monthly","🔮 Predict","⚡ Actions","🚨 Alerts",
         "🔄 Followup","➕ New Yuvak","✏️ Edit","👤 Profiles",
         "📥 Excel","⚙️ Settings"]

page = st.selectbox("", PAGES, label_visibility="collapsed")
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.subheader("📊 Dashboard")
    if not D["history"]:
        st.info("No session history yet. Submit attendance to see insights.")
    else:
        H = D["history"]
        cats = {m["name"]: get_cat(m["name"], H, D["cat_overrides"]) for m in members}
        r_c = sum(1 for c in cats.values() if c=="R")
        i_c = sum(1 for c in cats.values() if c=="I")
        n_c = sum(1 for c in cats.values() if c=="N")
        last = H[-1]
        lp = sum(1 for r in last["records"] if r["status"]=="P")
        lpct = round(lp/max(len(members),1)*100)
        l6 = H[-6:]
        avg = round(sum(sum(1 for r in s["records"] if r["status"]=="P")/max(len(members),1)*100 for s in l6)/len(l6))

        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("🟢 Regular", r_c)
        c2.metric("🟡 Irregular", i_c)
        c3.metric("🔴 No Category", n_c)
        c4.metric("Last Session", f"{lp} ({lpct}%)")
        c5.metric("6-Session Avg", f"{avg}%")

        st.divider()
        st.markdown("#### Attendance Trend (Last 10 Sessions)")
        l10 = H[-10:]
        dates = [s["date"] for s in l10]
        pcts  = [round(sum(1 for r in s["records"] if r["status"]=="P")/max(len(members),1)*100) for s in l10]
        fig = go.Figure(go.Scatter(x=dates, y=pcts, mode="lines+markers+text",
            text=[f"{p}%" for p in pcts], textposition="top center",
            line=dict(color="#6366f1",width=2), marker=dict(size=8)))
        fig.update_layout(height=260, margin=dict(l=0,r=0,t=10,b=0),
            yaxis=dict(range=[0,105],ticksuffix="%"),
            plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Followup-wise Summary")
        rows = []
        for fp in fps_list:
            fm = [m for m in members if m["followup"]==fp]
            rows.append({"Followup":fp,"Total":len(fm),
                "Regular":sum(1 for m in fm if cats.get(m["name"])=="R"),
                "Irregular":sum(1 for m in fm if cats.get(m["name"])=="I"),
                "No":sum(1 for m in fm if cats.get(m["name"])=="N")})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ATTENDANCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋 Attendance":
    st.subheader(f"📋 Attendance — {st.session_state.sess_date}")

    pres_count = sum(1 for s in st.session_state.att.values() if s=="P")
    c1,c2,c3 = st.columns(3)
    c1.metric("✅ Present", pres_count)
    c2.metric("❌ Absent", len(members)-pres_count)
    c3.metric("Total", len(members))

    ca, cb = st.columns(2)
    if ca.button("✅ Mark All Present"):
        st.session_state.att = {m["name"]:"P" for m in members}
        st.rerun()
    if cb.button("❌ Mark All Absent"):
        st.session_state.att = {m["name"]:"A" for m in members}
        st.rerun()

    st.divider()
    search = st.text_input("🔍 Search", placeholder="Filter by name...")
    fp_fil = st.selectbox("Filter by Followup", ["All"]+fps_list, key="att_fp")

    filtered = [m for m in members
                if search.lower() in m["name"].lower()
                and (fp_fil=="All" or m["followup"]==fp_fil)]

    for m in filtered:
        cur = st.session_state.att.get(m["name"], "A")
        cat = get_cat(m["name"], D["history"], D["cat_overrides"])
        badge = {"R":"🟢","I":"🟡","N":"🔴"}.get(cat,"⚪")
        col1, col2 = st.columns([6,1])
        with col1:
            st.markdown(f"**{m['name']}** {badge}  \n"
                        f"<small style='color:#888'>{m['followup']} · {m['contact']}</small>",
                        unsafe_allow_html=True)
        with col2:
            checked = st.checkbox("P", value=(cur=="P"), key=f"cb_{m['name']}", label_visibility="collapsed")
            st.session_state.att[m["name"]] = "P" if checked else "A"

    st.divider()
    note = st.text_area("📝 Session Note", value=D["session_notes"].get(st.session_state.sess_date,""), height=70)
    if st.button("✅ Submit Attendance", type="primary", use_container_width=True):
        records = [{"name":n,"status":s} for n,s in st.session_state.att.items()]
        D["history"] = [h for h in D["history"] if h["date"]!=st.session_state.sess_date]
        D["history"].append({"date":st.session_state.sess_date,"sabha":st.session_state.sabha,"records":records})
        if note: D["session_notes"][st.session_state.sess_date] = note
        save_data(D)
        st.session_state.data = D
        st.success(f"✅ Submitted! {pres_count} present on {st.session_state.sess_date}")
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: REPORT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Report":
    st.subheader("📈 Session Report")
    if not D["history"]:
        st.info("No history yet.")
    else:
        sel = st.selectbox("Select Session", [s["date"] for s in reversed(D["history"])])
        sess = next((s for s in D["history"] if s["date"]==sel), None)
        if sess:
            pres = [r for r in sess["records"] if r["status"]=="P"]
            abst = [r for r in sess["records"] if r["status"]=="A"]
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Present", len(pres))
            c2.metric("Absent", len(abst))
            c3.metric("Attendance %", f"{round(len(pres)/max(len(sess['records']),1)*100)}%")
            c4.metric("Sabha", sess.get("sabha","Weekly"))
            note_r = D["session_notes"].get(sel,"")
            if note_r: st.info(f"📝 Note: {note_r}")
            col1,col2 = st.columns(2)
            with col1:
                st.markdown("**✅ Present**")
                st.dataframe(pd.DataFrame([{"#":i+1,"Name":r["name"],
                    "Followup":next((m["followup"] for m in members if m["name"]==r["name"]),"—")}
                    for i,r in enumerate(sorted(pres,key=lambda x:x["name"]))]),
                    use_container_width=True, hide_index=True)
            with col2:
                st.markdown("**❌ Absent**")
                st.dataframe(pd.DataFrame([{"#":i+1,"Name":r["name"],
                    "Followup":next((m["followup"] for m in members if m["name"]==r["name"]),"—"),
                    "Cat":get_cat(r["name"],D["history"],D["cat_overrides"])}
                    for i,r in enumerate(sorted(abst,key=lambda x:x["name"]))]),
                    use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HISTORIC
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🕒 Historic":
    st.subheader("🕒 Member Attendance History")
    if not D["history"]:
        st.info("No history yet.")
    else:
        srch = st.text_input("🔍 Search member", key="hs")
        rows = []
        for m in members:
            if srch.lower() not in m["name"].lower(): continue
            sm = [s for s in D["history"] if any(r["name"]==m["name"] for r in s["records"])]
            p  = sum(1 for s in sm if any(r["name"]==m["name"] and r["status"]=="P" for r in s["records"]))
            cat = get_cat(m["name"],D["history"],D["cat_overrides"])
            streak = consec_absent(m["name"],D["history"])
            last = "Never"
            for s in reversed(D["history"]):
                if any(r["name"]==m["name"] and r["status"]=="P" for r in s["records"]):
                    last = s["date"]; break
            rows.append({"Name":m["name"],"Followup":m["followup"],
                "Present":p,"Sessions":len(sm),
                "Pct":f"{round(p/max(len(sm),1)*100)}%" if sm else "—",
                "Category":cat,"Streak":streak,"Last Seen":last})
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        buf = BytesIO()
        df.to_excel(buf, index=False, engine="openpyxl")
        st.download_button("📥 Download Excel", buf.getvalue(),
            "history.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MONTHLY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📅 Monthly":
    st.subheader("📅 Monthly Summary")
    if not D["history"]:
        st.info("No history yet.")
    else:
        monthly = defaultdict(list)
        for s in D["history"]:
            try: key = datetime.strptime(s["date"],"%d %b %Y").strftime("%b %Y")
            except: key = s["date"][:7]
            monthly[key].append(s)
        months = sorted(monthly.keys(), reverse=True)
        sel_m = st.selectbox("Month", months)
        ms = monthly[sel_m]
        st.caption(f"{len(ms)} sessions in {sel_m}")
        rows = []
        for m in members:
            p = sum(1 for s in ms if any(r["name"]==m["name"] and r["status"]=="P" for r in s["records"]))
            t = sum(1 for s in ms if any(r["name"]==m["name"] for r in s["records"]))
            rows.append({"Name":m["name"],"Followup":m["followup"],
                "Present":p,"Sessions":t,"Pct":f"{round(p/max(t,1)*100)}%" if t else "—"})
        st.dataframe(pd.DataFrame(rows).sort_values("Present",ascending=False),
            use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PREDICT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔮 Predict":
    st.subheader("🔮 Attendance Prediction")
    if len(D["history"]) < 3:
        st.info("Need at least 3 sessions of history to predict.")
    else:
        l3 = D["history"][-3:]
        rows = []
        fp_f = st.selectbox("Filter by Followup", ["All"]+fps_list, key="pf")
        for m in members:
            if fp_f!="All" and m["followup"]!=fp_f: continue
            rec = [s for s in l3 if any(r["name"]==m["name"] for r in s["records"])]
            a = sum(1 for s in rec if any(r["name"]==m["name"] and r["status"]=="P" for r in s["records"]))
            pct = round(a/max(len(rec),1)*100)
            pred = "✅ Likely" if pct>=67 else ("⚠️ Maybe" if pct>=33 else "❌ Unlikely")
            rows.append({"Name":m["name"],"Followup":m["followup"],
                "Recent %":f"{pct}%","Prediction":pred,
                "Category":get_cat(m["name"],D["history"],D["cat_overrides"])})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ACTIONS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚡ Actions":
    st.subheader("⚡ Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Category Override")
        m_names = [m["name"] for m in members]
        act_m = st.selectbox("Member", m_names, key="act_m")
        cats_opts = ["Auto (calculated)","Regular","Irregular","No"]
        cur_ov = D["cat_overrides"].get(act_m,"")
        cur_idx = {"R":1,"I":2,"N":3}.get(cur_ov, 0)
        new_c = st.selectbox("Category", cats_opts, index=cur_idx, key="act_c")
        if st.button("💾 Save Category"):
            cmap = {"Regular":"R","Irregular":"I","No":"N"}
            if new_c=="Auto (calculated)": D["cat_overrides"].pop(act_m,None)
            else: D["cat_overrides"][act_m] = cmap[new_c]
            save_data(D); st.session_state.data=D
            st.success(f"Updated {act_m}"); st.rerun()
    with col2:
        st.markdown("#### Followup Override")
        fp_m = st.selectbox("Member", m_names, key="fp_m")
        cur_fp = D["fp_overrides"].get(fp_m, next((m["followup"] for m in members if m["name"]==fp_m),""))
        fi = fps_list.index(cur_fp) if cur_fp in fps_list else 0
        new_fp = st.selectbox("New Followup", fps_list, index=fi, key="fp_new")
        if st.button("💾 Save Followup"):
            D["fp_overrides"][fp_m] = new_fp
            save_data(D); st.session_state.data=D
            st.success(f"Updated {fp_m}"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ALERTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🚨 Alerts":
    st.subheader("🚨 Alerts — At-Risk Members")
    if not D["history"]:
        st.info("No history yet.")
    else:
        alerts = []
        for m in members:
            streak = consec_absent(m["name"],D["history"])
            if streak >= 2:
                cat = get_cat(m["name"],D["history"],D["cat_overrides"])
                risk = "🔴 High" if streak>=4 else "🟡 Medium"
                alerts.append({"Name":m["name"],"Followup":m["followup"],
                    "Contact":m["contact"],"Consec. Absences":streak,"Cat":cat,"Risk":risk})
        if not alerts:
            st.success("✅ No members with 2+ consecutive absences!")
        else:
            st.warning(f"⚠️ {len(alerts)} members need follow-up")
            st.dataframe(pd.DataFrame(sorted(alerts,key=lambda x:-x["Consec. Absences"])),
                use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("#### Regular Members Absent in Current Session")
        ra = [m for m in members
              if get_cat(m["name"],D["history"],D["cat_overrides"])=="R"
              and st.session_state.att.get(m["name"],"A")=="A"]
        if ra:
            st.dataframe(pd.DataFrame([{"Name":m["name"],"Followup":m["followup"],"Contact":m["contact"]} for m in ra]),
                use_container_width=True, hide_index=True)
        else:
            st.success("No regular members absent currently!")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FOLLOWUP
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔄 Followup":
    st.subheader("🔄 Followup Group Overview")
    fp_sel = st.selectbox("Followup", ["All"]+fps_list, key="fp_ov")
    show = members if fp_sel=="All" else [m for m in members if m["followup"]==fp_sel]
    rows = []
    for m in show:
        cat = get_cat(m["name"],D["history"],D["cat_overrides"])
        sm = [s for s in D["history"] if any(r["name"]==m["name"] for r in s["records"])]
        p  = sum(1 for s in sm if any(r["name"]==m["name"] and r["status"]=="P" for r in s["records"]))
        rows.append({"Name":m["name"],"Followup":m["followup"],"Contact":m["contact"],
            "Category":cat,"Present":p,"Streak":consec_absent(m["name"],D["history"])})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: NEW YUVAK
# ══════════════════════════════════════════════════════════════════════════════
elif page == "➕ New Yuvak":
    st.subheader("➕ Register New Yuvak")
    with st.form("reg_form"):
        nn = st.text_input("Full Name *")
        nf = st.selectbox("Followup *", fps_list)
        nc = st.text_input("Contact Number")
        nr = st.text_input("Reference (who brought them)")
        ncat = st.selectbox("Category", ["Auto","Regular","Irregular","No"])
        sub = st.form_submit_button("➕ Add Member", type="primary")
    if sub:
        if not nn.strip():
            st.error("Full Name is required.")
        elif any(m["name"].lower()==nn.strip().lower() for m in members):
            st.error(f"'{nn}' already exists.")
        else:
            D["extra_members"].append({"name":nn.strip(),"followup":nf,"contact":nc,
                "reference":nr,"registeredOn":date.today().strftime("%d %b %Y")})
            if ncat!="Auto":
                D["cat_overrides"][nn.strip()] = {"Regular":"R","Irregular":"I","No":"N"}[ncat]
            save_data(D); st.session_state.data=D
            st.success(f"✅ {nn} added!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EDIT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "✏️ Edit":
    st.subheader("✏️ Edit Registered Members")
    extra = D.get("extra_members",[])
    st.caption(f"{len(members)} total · {len(extra)} registered · {len(MASTER) if not D.get('suppress_master') else 0} master")
    srch_e = st.text_input("🔍 Filter", key="ed_srch")
    edit_list = [m for m in members if m.get("is_extra") and srch_e.lower() in m["name"].lower()]
    if not edit_list:
        st.info("No registered members found. Only registered (non-Master) members can be edited.")
    for m in edit_list:
        idx_e = next((i for i,em in enumerate(extra) if em["name"]==m["name"]), None)
        if idx_e is None: continue
        em = extra[idx_e]
        with st.expander(f"✏️ {m['name']}"):
            c1,c2 = st.columns(2)
            un = c1.text_input("Name", em["name"], key=f"en_{idx_e}")
            uf_idx = fps_list.index(em.get("followup",fps_list[0])) if em.get("followup") in fps_list else 0
            uf = c2.selectbox("Followup", fps_list, index=uf_idx, key=f"ef_{idx_e}")
            uc = c1.text_input("Contact", em.get("contact",""), key=f"ec_{idx_e}")
            ur = c2.text_input("Reference", em.get("reference",""), key=f"er_{idx_e}")
            cs, cd = st.columns(2)
            if cs.button("💾 Save", key=f"es_{idx_e}"):
                D["extra_members"][idx_e].update({"name":un,"followup":uf,"contact":uc,"reference":ur})
                save_data(D); st.session_state.data=D; st.success("Saved!"); st.rerun()
            if cd.button("🗑️ Delete", key=f"ed_{idx_e}"):
                D["extra_members"].pop(idx_e)
                D["cat_overrides"].pop(em["name"],None)
                save_data(D); st.session_state.data=D; st.warning(f"Deleted {em['name']}"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PROFILES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👤 Profiles":
    st.subheader("👤 Member Profiles")
    srch_p = st.text_input("🔍 Search", key="pp")
    shown = [m for m in members if srch_p.lower() in m["name"].lower()][:50]
    for m in shown:
        cat = get_cat(m["name"],D["history"],D["cat_overrides"])
        cat_label = {"R":"Regular","I":"Irregular","N":"No"}.get(cat,cat)
        sm = [s for s in D["history"] if any(r["name"]==m["name"] for r in s["records"])]
        p  = sum(1 for s in sm if any(r["name"]==m["name"] and r["status"]=="P" for r in s["records"]))
        icon = "🔵" if not m.get("is_extra") else "🟣"
        with st.expander(f"{icon} {m['name']} — {cat_label}"):
            c1,c2,c3 = st.columns(3)
            c1.metric("Category", cat_label)
            c2.metric("Total Present", p)
            c3.metric("Absent Streak", consec_absent(m["name"],D["history"]))
            st.caption(f"Followup: **{m['followup']}** | Contact: **{m.get('contact','—')}**"
                       + (f" | Reference: **{m.get('reference','—')}**" if m.get("is_extra") else ""))

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EXCEL
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📥 Excel":
    st.subheader("📥 Excel — Member Directory")
    cat_lbl = {"R":"Regular","I":"Irregular","N":"No"}

    # Export
    st.markdown("#### 📤 Export")
    exp_rows = []
    for m in members:
        ref = m.get("reference","") if m.get("is_extra") else D["ref_overrides"].get(m["name"],"")
        cc  = D["cat_overrides"].get(m["name"]) or calc_category(m["name"],D["history"])
        exp_rows.append({"Full Name":m["name"],"Followup":m["followup"],
            "Reference":ref,"Contact":m.get("contact",""),"Category":cat_lbl.get(cc,"No")})
    buf = BytesIO()
    pd.DataFrame(exp_rows).to_excel(buf, index=False, engine="openpyxl")
    st.download_button("📥 Download Member Excel", buf.getvalue(),
        f"ShreejiMembers_{date.today().strftime('%d_%b_%Y')}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("Total", len(exp_rows))
    c2.metric("With Reference", sum(1 for r in exp_rows if r["Reference"]))
    c3.metric("No Reference",   sum(1 for r in exp_rows if not r["Reference"]))

    st.divider()
    # Import
    st.markdown("#### 📂 Import")
    st.caption("Columns: Full Name · Followup · Reference · Contact · Category (Regular/Irregular/No). "
               "New names are added as members. Import replaces existing member data.")
    upl = st.file_uploader("Choose Excel (.xlsx)", type=["xlsx","xls"])
    if upl:
        try:
            df_i = pd.read_excel(upl, dtype=str).fillna("")
            if "Full Name" not in df_i.columns:
                st.error('Excel must have "Full Name" column')
            else:
                cmap_i = {"regular":"R","irregular":"I","no":"N"}
                new_ext = list(D.get("extra_members",[]))
                new_cov = dict(D["cat_overrides"])
                created=updated=skipped=0
                for _,row in df_i.iterrows():
                    name = str(row.get("Full Name","")).strip()
                    fp   = str(row.get("Followup","")).strip()
                    ref  = str(row.get("Reference","")).strip()
                    cont = str(row.get("Contact","")).strip()
                    cat  = cmap_i.get(str(row.get("Category","")).strip().lower())
                    if not name or not fp: skipped+=1; continue
                    ex = next((m for m in members if m["name"].lower()==name.lower()), None)
                    if ex:
                        if ex.get("is_extra"):
                            for i,em in enumerate(new_ext):
                                if em["name"].lower()==name.lower():
                                    if ref: new_ext[i]["reference"]=ref
                                    if cont: new_ext[i]["contact"]=cont
                                    if fp: new_ext[i]["followup"]=fp
                                    break
                        else:
                            if ref: D["ref_overrides"][ex["name"]]=ref
                            if fp:  D["fp_overrides"][ex["name"]]=fp
                        if cat: new_cov[ex["name"]]=cat
                        updated+=1
                    else:
                        new_ext.append({"name":name,"followup":fp,"reference":ref,"contact":cont,
                            "registeredOn":date.today().strftime("%d %b %Y")})
                        if cat: new_cov[name]=cat
                        created+=1
                D["suppress_master"]=True; D["extra_members"]=new_ext; D["cat_overrides"]=new_cov
                save_data(D); st.session_state.data=D
                st.success(f"✅ {created} added · {updated} updated · {skipped} skipped"); st.rerun()
        except Exception as e:
            st.error(f"Import failed: {e}")

    st.divider()
    # Delete All
    st.markdown("#### 🗑️ Delete All Data")
    st.warning("Erases all history, members, and overrides. Cannot be undone.")
    confirm = st.checkbox("I understand this is permanent")
    if confirm and st.button("🗑️ Delete Everything", type="primary"):
        st.session_state.data = {"history":[],"extra_members":[],"fp_overrides":{},
            "cat_overrides":{},"session_notes":{},"ref_overrides":{},"abs_reasons":{},"suppress_master":True}
        st.session_state.att = {}
        save_data(st.session_state.data)
        st.success("All data deleted."); st.rerun()

    st.divider()
    st.markdown("#### 👥 Directory Preview")
    st.dataframe(pd.DataFrame(exp_rows), use_container_width=True, hide_index=True, height=350)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚙️ Settings":
    st.subheader("⚙️ Settings")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("#### 💾 Backup & Restore")
        st.download_button("📦 Export Full Backup",
            json.dumps(D, indent=2, ensure_ascii=False),
            f"shreeji_backup_{date.today().strftime('%Y%m%d')}.json",
            "application/json", use_container_width=True)
        rf = st.file_uploader("📂 Restore Backup", type=["json"])
        if rf:
            try:
                restored = json.loads(rf.read())
                save_data(restored); st.session_state.data=restored
                st.success("✅ Restored!"); st.rerun()
            except Exception as e:
                st.error(f"Restore failed: {e}")
    with col2:
        st.markdown("#### 📊 Stats")
        st.metric("Sessions", len(D["history"]))
        st.metric("Registered Members", len(D.get("extra_members",[])))
        st.metric("Category Overrides", len(D.get("cat_overrides",{})))
        if D.get("suppress_master"):
            st.warning("⚠️ Master DB is suppressed")
            if st.button("♻️ Restore Master DB"):
                D["suppress_master"]=False; save_data(D); st.session_state.data=D; st.rerun()
