"""Audit reproductible de Zenodo 18912903. Aucun fichier individuel exporté."""
import io, json, hashlib, urllib.request, pathlib, datetime
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate

ROOT=pathlib.Path(__file__).resolve().parent
meta=json.load(urllib.request.urlopen('https://zenodo.org/api/records/18912903',timeout=60))
raw=urllib.request.urlopen(meta['files'][0]['links']['self'],timeout=60).read()
assert hashlib.md5(raw).hexdigest()==meta['files'][0]['checksum'].split(':')[1]
xls=pd.ExcelFile(io.BytesIO(raw)); df=pd.read_excel(xls,keep_default_na=False)
y=pd.to_numeric(df.Loan_Default_Status)
leaks=['Days_Past_Due','Loan_Recovery_Procedure','Default_Rate_Percent']
num=list(df.select_dtypes(include='number').columns)
def summary(g):
 return {'n':len(g),'defaults':int(g.Loan_Default_Status.sum()),'loan_sum':float(g.Loan_Amount_KES.sum()),'loan_median':float(g.Loan_Amount_KES.median()),'revenue_median':float(g.Monthly_Revenue_KES.median()),'education_blank':int((g.Education_Level=='').sum()),'collateral_blank':int((g.Collateral_Type=='').sum())}
cohorts=[]
for keys,g in df.groupby(['County','Business_Sector','Location_Type']):
 cohorts.append(dict(zip(['county','sector','location'],keys))|summary(g))
profiles=[]
for c in df:
 d={'name':c,'type':'numérique' if c in num else 'catégorielle','blank':int((df[c]=='').sum()),'unique':int(df[c].nunique()),'leak':c in leaks}
 if c in num: d.update({k:float(v) for k,v in df[c].describe().to_dict().items()})
 else: d['values']={str(k) or '(vide)':int(v) for k,v in df[c].value_counts(dropna=False).items()}
 profiles.append(d)
cv=StratifiedKFold(5,shuffle=True,random_state=42); models=[]
for mode in ['avec_fuites','sans_fuites_identifiees']:
 X=df.drop(columns=['Loan_Default_Status']+(leaks if mode!='avec_fuites' else []))
 nc=list(X.select_dtypes(include='number').columns); cc=[c for c in X if c not in nc]
 for name,model in [('Régression logistique',LogisticRegression(max_iter=2000)),('Forêt aléatoire',RandomForestClassifier(n_estimators=150,min_samples_leaf=5,random_state=42,n_jobs=2))]:
  prep=ColumnTransformer([('num',make_pipeline(SimpleImputer(strategy='median'),StandardScaler()),nc),('cat',make_pipeline(SimpleImputer(missing_values='',strategy='most_frequent'),OneHotEncoder(handle_unknown='ignore')),cc)])
  scores=cross_validate(make_pipeline(prep,model),X,y,cv=cv,scoring={'auc':'roc_auc','ap':'average_precision','balanced_accuracy':'balanced_accuracy','accuracy':'accuracy','brier':'neg_brier_score'},n_jobs=1)
  models.append({'mode':mode,'model':name,'metrics':{k:{'mean':float((-v if k=='test_brier' else v).mean()),'sd':float(v.std(ddof=1))} for k,v in scores.items() if k.startswith('test_')}})
  print(mode,name,models[-1]['metrics'],flush=True)
corr=df[num].corr().Loan_Default_Status.drop('Loan_Default_Status').sort_values(key=abs,ascending=False)
data={'record':18912903,'doi':meta['doi'],'retrieved':datetime.datetime.now(datetime.timezone.utc).isoformat(),'md5':hashlib.md5(raw).hexdigest(),'sha256':hashlib.sha256(raw).hexdigest(),'sheets':xls.sheet_names,'shape':list(df.shape),'summary':summary(df),'cohorts':cohorts,'profiles':profiles,'models':models,'correlations':corr.to_dict(),'duplicates':int(df.duplicated().sum()),'dpd_cross':pd.crosstab(y,df.Days_Past_Due>=90).to_dict(),'versions':{'pandas':pd.__version__,'sklearn':sklearn.__version__},'license':meta['metadata'].get('license'),'creator':meta['metadata']['creators']}
(ROOT/'dist').mkdir(exist_ok=True)
(ROOT/'dist'/'audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
(ROOT/'dist'/'data.js').write_text('window.AUDIT='+json.dumps(data,ensure_ascii=False)+';')
(ROOT/'metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
print('DONE',data['shape'],data['summary'],data['dpd_cross'],flush=True)
