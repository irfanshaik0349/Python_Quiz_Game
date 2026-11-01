import json, os, random
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session
ROOT=Path(__file__).resolve().parent
app=Flask(__name__); app.secret_key=os.environ.get("SECRET_KEY","dev-key-change-me")
def bank():
    with (ROOT/"python_question_bank.json").open(encoding="utf-8") as f: return json.load(f)["questions"]
@app.get("/")
def home():
    qs=bank()
    return render_template("index.html",topics=sorted({q["topic"] for q in qs}),total=len(qs))
@app.post("/api/start")
def start():
    d=request.get_json(force=True); qs=bank()
    if d.get("difficulty","All")!="All": qs=[q for q in qs if q["difficulty"]==d["difficulty"]]
    if d.get("topic","All")!="All": qs=[q for q in qs if q["topic"]==d["topic"]]
    random.shuffle(qs); qs=qs[:max(5,min(50,int(d.get("count",20))))]
    if not qs:return jsonify(error="No questions match these filters."),400
    session["quiz"]=qs;session["answers"]=[];session["name"]=str(d.get("name","Student"))[:40]
    return jsonify(name=session["name"],questions=[{k:q[k] for k in ("id","topic","difficulty","question","options")} for q in qs])
@app.post("/api/answer")
def answer():
    d=request.get_json(force=True); qs=session.get("quiz",[]); answers=session.get("answers",[]); i=int(d.get("index",-1))
    if i<0 or i>=len(qs) or i!=len(answers):return jsonify(error="Invalid question position."),400
    q=qs[i]; ok=d.get("choice")==q["answer"]; answers.append({"correct":ok});session["answers"]=answers
    return jsonify(correct=ok,answer=q["answer"],explanation=q["explanation"],score=sum(x["correct"] for x in answers))
@app.get("/api/result")
def result():
    qs=session.get("quiz",[]);ans=session.get("answers",[]);n=len(qs);s=sum(x["correct"] for x in ans)
    return jsonify(name=session.get("name","Student"),score=s,total=n,percentage=round(s*100/n) if n else 0)
if __name__=="__main__":app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
