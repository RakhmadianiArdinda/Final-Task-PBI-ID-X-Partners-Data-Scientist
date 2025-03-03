# -*- coding: utf-8 -*-
"""FinalTask_ID/XPartners_DataScientist_RakhmadianiArdindaChaerunnisa.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-Sbzm1ikxJIIgGiVo5Nn0AKhrY0s1aV4

# **IMPORT DATASET FROM GOOGLE DRIVE**
"""

from google.colab import drive
import pandas as pd
import os
# Periksa apakah drive sudah terpasang. Pasang kembali jika terjadi kesalahan
if not os.path.exists('/content/drive'):  # Apakah suatu file ada dalam sistem
  drive.mount('/content/drive',force_remount=True) # Untuk merefresh kepercayaan
else:
  print("Drive sudah terpasang")
df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Internship/loan_data_2007_2014.csv')
print("\nGAMBARAN UMUM DATA\n",df.head())

"""# **DATA UNDERSTANDING**

1. STRUKTUR DATASET
"""

df

df.columns

# DataFrame untuk menyimpan kolom dan tipe data
df_type = pd.DataFrame({'Columns':df.columns, 'Type':df.dtypes.values})
# Kelompokkan berdasarkan tipe data
df_type = df_type.sort_values(by="Type").reset_index(drop=True)
df_type.index = df_type.index + 1 # Start from 1 index

from tabulate import tabulate
print(tabulate(df_type,headers="keys",tablefmt="grid"))

df[df.duplicated()]

df_null = df.isnull().sum().reset_index()
df_null.columns = ["Columns","Null Values"]
df_null.index = df_null.index + 1 # Start from 1 index

# Show columns with Null Values > 0
df_null_filter = df_null[df_null["Null Values"]>0].sort_values(by = "Null Values")
from tabulate import tabulate
print(tabulate(df_null_filter,headers="keys",tablefmt="grid"))

"""2. HANDLING MISSING VALUES"""

# Drop columns with only null values
drop_only_null = df.dropna(axis = 1, how = 'all')
print(drop_only_null.shape)

# If missing values is <5% from all dataset -> drop rows
five_percent = round((5/100)*len(df))
print(five_percent) # The result is 23314

# Null counts
null_counts = drop_only_null.isna().sum(axis=0)
print(null_counts)

def percent_missing(data):
  # Total null values
  null_val = data.isnull().sum()
  # Percentage null values
  null_val_percentage = 100 * data.isnull().sum() / len(data)
  # Create table result
  null_val_table = pd.concat([null_val,null_val_percentage],axis=1)
  # Give a name to the column
  null_val_table_name = null_val_table.rename(columns = {0 : 'Jumlah Null Values', 1 : 'Persentase Null Values'})
  # Sort by percentage of null values by descending
  null_val_table_name = null_val_table_name[null_val_table_name['Jumlah Null Values'] != 0].sort_values('Persentase Null Values',ascending=False).round(1)
  return null_val_table_name

df_missing = percent_missing(drop_only_null)
print(df_missing)

# Drop columns with > 50% missing values
threshold = len(df)*0.5
drop_col = drop_only_null.dropna(axis = 1, thresh=threshold)
print(drop_col.shape)

# Check missing values to make sure the code is correct
drop_col_missing = percent_missing(drop_col)
print(drop_col_missing)

# Create heatmap
import missingno as msno
msno.heatmap(drop_col)

# Count the correlation missing values between columns
missing_cor = df.isnull().corr()

# Column pairs with correlation = 1
correlated_cols = []
for col in missing_cor.columns:
  for idx in missing_cor.index:
    if col != idx and missing_cor.loc[idx,col] == 1:
      correlated_cols.append((idx,col))
print("Kolom dengan korelasi 1:")
print(correlated_cols)

# Create dataframe based on correlation columns
unique_correlated_cols = set([col for pair in correlated_cols for col in pair]) # Only for unique pairs
df_filtered = drop_col[list(unique_correlated_cols)]
print(df_filtered)

# Handling missing values with mean using SimpleImputer
from sklearn.impute import SimpleImputer
# Copy dataframe for imputation result
df_imputed = drop_col.copy()
# Filter only numeric columns
numeric_cols = drop_col.select_dtypes(include='number').columns
# Use SimpleImputer only for numeric columns
imputer = SimpleImputer(strategy = 'mean')
df_imputed[numeric_cols] = imputer.fit_transform(drop_col[numeric_cols])
print(df_imputed)
# Check missing values using function percent_missing(df)
missing_after_imputed = percent_missing(df_imputed)
print(missing_after_imputed)

print(df_imputed[['next_pymnt_d','emp_title','emp_length','last_pymnt_d','last_credit_pull_d','earliest_cr_line','title']])

print(df_imputed[['next_pymnt_d','emp_title','emp_length','last_pymnt_d','last_credit_pull_d','earliest_cr_line','title']].dtypes)

# Use SimpleImputer to fill missing values in object
imputer_object = SimpleImputer(strategy='most_frequent')
# Select only object (string) columns
string_col = df_imputed.select_dtypes(include='object')
# Apply imputation
df_imputed[string_col.columns] = imputer_object.fit_transform(string_col)
print(df_imputed)
# Check missing values using function percent_missing(df)
missing_after_object = percent_missing(df_imputed)
print(missing_after_object)

df_null_imputed = df_imputed.isnull().sum().reset_index()
df_null_imputed.columns = ["Columns","Null Values"]
df_null_imputed.index = df_null_imputed.index + 1 # Start from 1 index

# Show columns with Null Values
imputed_null = df_null_imputed[df_null_imputed["Null Values"]>0].sort_values(by = "Null Values")
from tabulate import tabulate
print(tabulate(imputed_null,headers="keys",tablefmt="grid"))

df_imputed.isnull().sum()

# Check if 'Unnamed: 0' column exists before trying to print or drop it
if 'Unnamed: 0' in df_imputed.columns:
    print(df_imputed['Unnamed: 0'])
    # Drop column 'Unnamed: 0'
    df_imputed.drop('Unnamed: 0',axis = 'columns', inplace = True)
    print(df_imputed.shape)
else:
    print("Column 'Unnamed: 0' not found in the DataFrame.")

df_imputed.columns

df_imputed.shape

"""2. STATISTIK DESKRIPTIF"""

print(df_imputed.head)

# Describe the data only numeric
df_imputed.describe()

# Describe the data only object
df_imputed.describe(include="object")

print(df_imputed.select_dtypes(include='object').columns)

print(df_imputed['pymnt_plan'])

# Correlation among the features

# List numeric columns
cols_num = df_imputed.select_dtypes(exclude=object).columns.tolist()
print(cols_num)

# List categoric columns
cols_cat = df_imputed.select_dtypes(include=object).columns.tolist()
print(cols_cat)

# Correlation between numeric columns
cor_matrix = df_imputed[cols_num].corr()
cor_matrix

import matplotlib.pyplot as plt
import seaborn as sns

# Atur ukuran heatmap sebelum plotting
plt.figure(figsize=(20, 10))  # Sesuaikan ukuran sesuai kebutuhan

# Plot heatmap dengan ukuran yang lebih besar
sns.heatmap(cor_matrix, annot=False, cmap="coolwarm")  # cmap untuk warna lebih jelas

# Tampilkan plot
plt.show()

"""# **VISUALISASI DATA**

1. VISUALISASI DATA NUMERIK
"""

### DISTRIBUSI DATA -> HISTOGRAM ###

import seaborn as sns
import matplotlib.pyplot as plt

num_cols = ['loan_amnt', 'funded_amnt', 'int_rate', 'installment', 'annual_inc', 'dti']
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 8))
for i, col in enumerate(num_cols):
    sns.histplot(data=df, x=col, kde=True, ax=axes[i//3, i%3])
    axes[i//3, i%3].set_title(f'Distribusi {col}')
plt.tight_layout()
plt.show()

### SOLUSI KETIDAKSEIMBANGAN DATA BERDASARKAN VISUALISASI DIATAS (KOLOM ANNUAL_INC) ###
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Buat kolom baru dengan log transform
df_imputed['log_annual_inc'] = np.log1p(df_imputed['annual_inc'])  # log(1 + annual_inc) untuk menghindari log(0)

# Plot sebelum dan sesudah log transform
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Distribusi asli
sns.histplot(df_imputed['annual_inc'], bins=50, kde=True, ax=axes[0])
axes[0].set_title("Distribusi Annual Income (Sebelum Log Transform)")
axes[0].set_xlabel("Annual Income (USD)")
axes[0].set_ylabel("Count")
axes[0].set_xscale('linear')  # Skala normal

# Distribusi setelah log transform
sns.histplot(df_imputed['log_annual_inc'], bins=50, kde=True, ax=axes[1])
axes[1].set_title("Distribusi Log Annual Income (Setelah Log Transform)")
axes[1].set_xlabel("Log(Annual Income)")
axes[1].set_ylabel("Count")

plt.tight_layout()
plt.show()

### SOLUSI UNTUK INSTALLMENT ###
import numpy as np
# Menangani skewness dengan log transformation
df_imputed['log_installment'] = np.log1p(df_imputed['installment'])  # log(1 + installment)

# Menangani skewness dengan square root transformation
df_imputed['sqrt_installment'] = np.sqrt(df_imputed['installment'])

# Membuat kategori (Binning) -> Mengelompokkan installment ke dalam kategori
bins = [0, 100, 300, 600, 1000, df_imputed['installment'].max()]
labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
df_imputed['installment_category'] = pd.cut(df_imputed['installment'], bins=bins, labels=labels)

# Visualisasi
import seaborn as sns
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.histplot(df_imputed['installment'], kde=True, ax=axes[0])
axes[0].set_title('Sebelum Transformasi')

sns.histplot(df_imputed['log_installment'], kde=True, ax=axes[1])
axes[1].set_title('Log Transform')

sns.histplot(df_imputed['sqrt_installment'], kde=True, ax=axes[2])
axes[2].set_title('Square Root Transform')

plt.tight_layout()
plt.show()

"""PERIKSA SKEWNESS"""

import pandas as pd

# Hitung skewness hanya untuk kolom numerik
skewness_values = df_imputed[cols_num].skew().sort_values(ascending=False)
print(skewness_values)

# Cek proporsi nilai nol dalam kolom numerik
zero_counts = (df_imputed[cols_num] == 0).sum() / len(df_imputed)
print(zero_counts[zero_counts > 0.5])  # Menampilkan kolom dengan lebih dari 50% nilai nol

"""
BAGI DATA MENJADI GOOD AND BAD"""

# Definisikan kategori GOOD dan BAD
good_status = ["Fully Paid", "Current", "Does not meet the credit policy. Status:Fully Paid"]
bad_status = ["Charged Off", "Default", "Late (31-120 days)", "Late (16-30 days)",
              "Does not meet the credit policy. Status: Charged Off"]

status_column = "loan_status"

# Buat kolom target: 1 = GOOD, 0 = BAD
df_imputed["target"] = df_imputed[status_column].apply(lambda x: 1 if x in good_status else (0 if x in bad_status else np.nan))

# Ada 3 loan_status yang belum dikategorikan bad or good
df_imputed.loc[df_imputed["loan_status"] == "In Grace Period", "target"] = 0
df_imputed.loc[df_imputed["loan_status"] == "Does not meet the credit policy. Status:Charged Off", "target"] = 0

# Cek status yang memiliki target NaN
unclassified_status = df_imputed[df_imputed["target"].isna()]["loan_status"].unique()
print("Status yang belum dikategorikan:", unclassified_status)

# Cek distribusi target
print(df_imputed["target"].value_counts(dropna=False))

"""LANJUT ATASI JUMLAH 0 YANG LEBIH DARI 50%"""

import seaborn as sns
import matplotlib.pyplot as plt

# Cek korelasi dengan target
correlations = df_imputed.select_dtypes(include=['number']).corr()['target'].abs().sort_values(ascending=False)

# Tampilkan hanya kolom yang banyak nol
correlations = correlations[zero_counts[zero_counts > 0.5].index]

print(correlations)

# Visualisasi heatmap
plt.figure(figsize=(8, 4))
sns.heatmap(correlations.to_frame(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Korelasi Kolom yang Banyak Nol dengan Target")
plt.show()

# Cek jumlah kolom sebelum penghapusan
print("Jumlah kolom sebelum:", len(df_imputed.columns))

# Pastikan hanya kolom yang ada yang akan dihapus (Kolom dengan korelasi rendah)
low_corr_cols = ["delinq_2yrs", "pub_rec", "collections_12_mths_ex_med", "acc_now_delinq", "tot_coll_amt"]
existing_cols = [col for col in low_corr_cols if col in df_imputed.columns]  # Pastikan kolom ada sebelum dihapus

# Hapus kolom yang ada
df_imputed.drop(columns=existing_cols, inplace=True)

# Cek jumlah kolom setelah penghapusan
print("Jumlah kolom setelah:", len(df_imputed.columns))

# Cek apakah kolom benar-benar sudah terhapus
print("Kolom yang tersisa:", df_imputed.columns)

print(df_imputed.isna().sum()[df_imputed.isna().sum() > 0])  # Tampilkan hanya kolom yang masih ada NaN

"""VISUALISASI LAGI"""

import seaborn as sns
import matplotlib.pyplot as plt

# Perbarui variable cols_num setelah penghapusan beberapa kolom
cols_num = df_imputed.select_dtypes(exclude=object).columns.tolist()

# KARENA ERROR MAKA: exclude 'installment_category' from cols_num jika sudah ada
if 'installment_category' in cols_num:
    cols_num.remove('installment_category')

# Histogram untuk semua fitur numerik dengan lebih banyak ruang antar subplot
fig, axes = plt.subplots(nrows=len(cols_num) // 3 + 1, ncols=3, figsize=(18, len(cols_num) * 1.5))
fig.suptitle("Distribusi Variabel Numerik\n", fontsize=16)

# Flatten axes untuk menghindari error saat plotting
axes = axes.flatten()

for i, col in enumerate(cols_num):
    sns.histplot(df_imputed[col], bins=30, kde=True, ax=axes[i], color="royalblue")
    axes[i].set_title(col, fontsize=12)

# Hapus subplot kosong
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout(pad=3)  # Beri lebih banyak padding antar subplot
plt.show()

# Boxplot dengan lebih banyak ruang antar variabel
plt.figure(figsize=(18, len(cols_num) * 0.6))  # Ukuran lebih tinggi
df_melted = df_imputed.melt(id_vars="target", value_vars=cols_num)
sns.boxplot(x="value", y="variable", data=df_melted, orient="h", showfliers=True, palette="coolwarm")
plt.title("Boxplot Variabel Numerik", fontsize=14)
plt.xlabel("Nilai")
plt.ylabel("Variabel")

plt.grid(axis="x", linestyle="--", alpha=0.6)  # Tambahkan grid biar lebih jelas
plt.show()

"""# **TINDAK LANJUT HASIL VISUALISASI**"""

### DROP VARIABEL TIDAK BERGUNA ###
df_imputed.drop(columns=['id','member_id','policy_code'], inplace=True)
# Perbarui variabel cols_num
cols_num = df_imputed.select_dtypes(exclude=object).columns.tolist()

"""HAPUS KOLOM annual_inc dan installment KARENA SUDAH PAKAI YANG TRANSFORMASI"""

# Hapus variabel asli setelah transformasi
df_imputed.drop(columns=['annual_inc', 'installment'], inplace=True)

# Perbarui daftar variabel numerik
cols_num = df_imputed.select_dtypes(exclude=object).columns.tolist()

# Hapus log_installment
df_imputed.drop(columns='log_installment',inplace=True)

# Perbarui daftar variabel numerik
cols_num = df_imputed.select_dtypes(exclude=object).columns.tolist()

print(df_imputed.shape)

import seaborn as sns
import matplotlib.pyplot as plt

# Perbarui variable cols_num setelah penghapusan beberapa kolom
cols_num = df_imputed.select_dtypes(exclude=object).columns.tolist()

# KARENA ERROR MAKA: exclude 'installment_category' from cols_num jika sudah ada
if 'installment_category' in cols_num:
    cols_num.remove('installment_category')

# Histogram untuk semua fitur numerik dengan lebih banyak ruang antar subplot
fig, axes = plt.subplots(nrows=len(cols_num) // 3 + 1, ncols=3, figsize=(18, len(cols_num) * 1.5))
fig.suptitle("Distribusi Variabel Numerik\n", fontsize=16)

# Flatten axes untuk menghindari error saat plotting
axes = axes.flatten()

for i, col in enumerate(cols_num):
    sns.histplot(df_imputed[col], bins=30, kde=True, ax=axes[i], color="royalblue")
    axes[i].set_title(col, fontsize=12)

# Hapus subplot kosong
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout(pad=3)  # Beri lebih banyak padding antar subplot
plt.show()

# Boxplot dengan lebih banyak ruang antar variabel
plt.figure(figsize=(18, len(cols_num) * 0.6))  # Ukuran lebih tinggi
df_melted = df_imputed.melt(id_vars="target", value_vars=cols_num)
sns.boxplot(x="value", y="variable", data=df_melted, orient="h", showfliers=True, palette="coolwarm")
plt.title("Boxplot Variabel Numerik", fontsize=14)
plt.xlabel("Nilai")
plt.ylabel("Variabel")

plt.grid(axis="x", linestyle="--", alpha=0.6)  # Tambahkan grid biar lebih jelas
plt.show()

"""# **VISUALISASI DATA KATEGORIK**

GRADE
"""

plt.figure(figsize=(10, 5))
sns.countplot(data=df, x='grade', hue='loan_status', palette='viridis')
plt.title("Distribusi Grade berdasarkan Status Loan\n")
plt.show()

"""HOME OWNERSHIP"""

plt.figure(figsize=(10, 5))
sns.countplot(data=df, x='home_ownership', hue='loan_status', palette='viridis')
plt.title("Distribusi Home Ownership berdasarkan Status Loan")
plt.show()

"""LOAN STATUS PER TAHUN"""

df['issue_d'] = pd.to_datetime(df['issue_d'], format='%b-%y', errors='coerce')
df['year'] = df['issue_d'].dt.year

plt.figure(figsize=(10,5))
sns.lineplot(data=df.groupby('year')['loan_status'].value_counts().unstack(), marker='o')
plt.title("Tren Jumlah Peminjam GOOD dan BAD per Tahun")
plt.show()

"""STATUS LOAN BERDASARKAN TERM (DURASI PINJAMAN)"""

plt.figure(figsize=(8,5))
sns.countplot(data=df, x='term', hue='loan_status', palette='Set1')
plt.title("Distribusi Loan Berdasarkan Durasi Pinjaman")
plt.show()

"""PURPOSES"""

import matplotlib.pyplot as plt
import seaborn as sns

# Set ukuran figure
plt.figure(figsize=(12, 6))

# Plot countplot untuk kolom kategorik 'purpose'
sns.countplot(y=df_imputed['purpose'], order=df_imputed['purpose'].value_counts().index, palette='viridis')

# Tambahkan judul
plt.title('Distribusi Purpose dalam Dataset', fontsize=14)
plt.xlabel('Jumlah')
plt.ylabel('Purpose')

# Tampilkan plot
plt.show()

"""EMPLOYEE TITLE"""

import matplotlib.pyplot as plt
import seaborn as sns

# Ambil 10 pekerjaan paling umum
top_10_jobs = df_imputed['emp_title'].value_counts().nlargest(10)

# Set ukuran figure
plt.figure(figsize=(12, 6))

# Buat bar chart
sns.barplot(x=top_10_jobs.values, y=top_10_jobs.index, palette='coolwarm')

# Tambahkan judul dan label
plt.title('10 Pekerjaan Paling Umum dalam Dataset', fontsize=14)
plt.xlabel('Jumlah')
plt.ylabel('Job Title')

# Tampilkan plot
plt.show()

"""VERIFICATION STATUS"""

import matplotlib.pyplot as plt

# Hitung jumlah masing-masing kategori
verification_counts = df_imputed['verification_status'].value_counts()

# Warna yang lebih elegan
colors = ['#FFA200', '#FF8800', '#FFD500']

# Efek explode agar salah satu slice lebih menonjol
explode = (0.05, 0.05, 0.05)  # Semua kategori sedikit keluar

# Buat pie chart
plt.figure(figsize=(8, 8))
plt.pie(verification_counts, labels=verification_counts.index, autopct='%1.1f%%',
        startangle=140, colors=colors, explode=explode, shadow=True,
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.2})

# Tambahkan judul
plt.title('Distribusi Verification Status', fontsize=14, fontweight='bold')

# Tampilkan plot
plt.show()

"""# **IDENTIFIKASI DISTRIBUSI SKEWED (CONDONG KIRI/KANAN)**

# **FEATURE ENGINEERING**

HAPUS KOLOM ZIP CODE DAN URL
"""

df_imputed.drop(columns=['zip_code', 'url'], inplace=True)
print(df_imputed.columns)

cols_cat = df_imputed.select_dtypes(include=['object']).columns.tolist()
df_categorical = df_imputed[cols_cat]

# Cek hasil
print(df_categorical.columns)
print(df_categorical.head)
print(df_imputed.shape)

"""LABEL ENCODING"""

!pip install category_encoders

import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import category_encoders as ce

# Salin dataset agar tidak merusak data asli
df_encoded = df_imputed.copy()

# 1. Ordinal Encoding untuk kategori yang memiliki urutan
ordinal_mapping = {
    'grade': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    'emp_length': ['< 1 year', '1 year', '2 years', '3 years', '4 years', '5 years',
                   '6 years', '7 years', '8 years', '9 years', '10+ years']
}

# Encoding untuk 'grade'
df_encoded['grade'] = df_encoded['grade'].map({val: idx for idx, val in enumerate(ordinal_mapping['grade'])})

# Encoding untuk 'emp_length'
df_encoded['emp_length'] = df_encoded['emp_length'].map({val: idx for idx, val in enumerate(ordinal_mapping['emp_length'])})

# 2. One-Hot Encoding untuk kategori tanpa urutan
onehot_features = ['home_ownership', 'verification_status', 'purpose', 'application_type', 'initial_list_status', 'pymnt_plan']
df_encoded = pd.get_dummies(df_encoded, columns=onehot_features, drop_first=True)

# 3. Binary Encoding untuk kolom dengan banyak nilai unik
binary_features = ['emp_title', 'addr_state', 'title']
binary_encoder = ce.BinaryEncoder(cols=binary_features)
df_encoded = binary_encoder.fit_transform(df_encoded)

# 4. Convert Date Columns ke Unix Timestamp
date_features = ['issue_d', 'earliest_cr_line', 'last_pymnt_d', 'next_pymnt_d', 'last_credit_pull_d']
for col in date_features:
    df_encoded[col] = pd.to_datetime(df_encoded[col], errors='coerce').astype('int64') // 10**9  # Konversi ke detik

# Cek hasil akhir
print(df_encoded.shape)
print(df_encoded.head())

df_encoded.columns

"""PISAHKAN FITUR DAN TARGET"""

# (KARENA ERROR SEBELUMNYA)
# Convert 'term' column to numerical representation if it's not already
# For example, map ' 36 months' to 36 and ' 60 months' to 60:
df_encoded['term'] = df_encoded['term'].str.extract('(\d+)').astype(float)

X = df_encoded.drop(columns=['target'])  # Hapus kolom target dari fitur
y = df_encoded['target']  # Ambil kolom target

"""BAGI DATA TRAIN DAN TEST"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# stratify=y -> agar proporsi kelas GOOD vs BAD seimbang

"""FEATURE SCALING DENGAN STANDARDSCALER ATAU MINMAXSCALER"""

# Convert all columns in X_train and X_test to numeric using pd.to_numeric
# Errors='coerce' will replace non-numeric values with NaN
for col in X_train.columns:
    X_train[col] = pd.to_numeric(X_train[col], errors='coerce')
    X_test[col] = pd.to_numeric(X_test[col], errors='coerce')

# Impute NaN values if any are created (using SimpleImputer or your preferred method)
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='mean')  # Or other strategy
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

# Now apply StandardScaler
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""# **LOGISTIC REGRESSION**

PERCOBAAN LOGISTIC REGRESSION PERTAMA
"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

model_lr = LogisticRegression()
model_lr.fit(X_train_scaled, y_train)

y_pred = model_lr.predict(X_test_scaled)
print(classification_report(y_test, y_pred))

"""PERBAIKAN 1: RESAMPLING DATA (OVERSAMPLING/UNDERSAMPLING) MENGGUNAKAN SMOTE UNTUK MENAMBAH SAMPEL KELAS MINORITTAS"""

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)

model_lr.fit(X_train_resampled, y_train_resampled)
y_pred = model_lr.predict(X_test_scaled)
print(classification_report(y_test, y_pred))

### CEK ROC-AUC Score --> Jika mendekati 1 maka model bekerja dengan baik ###
from sklearn.metrics import roc_auc_score

y_pred_proba = model_lr.predict_proba(X_test_scaled)[:, 1]
roc_auc = roc_auc_score(y_test, y_pred_proba)
print("ROC-AUC Score:", roc_auc)

"""CEK KOEFISIEN MODEL"""

print("Shape of model_lr.coef_:", model_lr.coef_.shape)
print("Number of features in X:", len(X.columns))
print("Original X shape:", X.shape)
print("Scaled X_train shape:", X_train_scaled.shape)
print("SMOTE X_train shape:", X_train_resampled.shape)

"""# **MODEL LAIN**

RANDOM FOREST
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Inisialisasi model Random Forest
model_rf = RandomForestClassifier(n_estimators=100, random_state=42)
model_rf.fit(X_train_resampled, y_train_resampled)

# Prediksi
y_pred_rf = model_rf.predict(X_test_scaled)
y_pred_proba_rf = model_rf.predict_proba(X_test_scaled)[:, 1]

# Evaluasi
print("Random Forest Classification Report:\n", classification_report(y_test, y_pred_rf))
print("ROC-AUC Score:", roc_auc_score(y_test, y_pred_proba_rf))

"""XGBOOST"""

import xgboost as xgb

# Inisialisasi model XGBoost
model_xgb = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
model_xgb.fit(X_train_resampled, y_train_resampled)

# Prediksi
y_pred_xgb = model_xgb.predict(X_test_scaled)
y_pred_proba_xgb = model_xgb.predict_proba(X_test_scaled)[:, 1]

# Evaluasi
print("XGBoost Classification Report:\n", classification_report(y_test, y_pred_xgb))
print("ROC-AUC Score:", roc_auc_score(y_test, y_pred_proba_xgb))

"""# **EDITING BEFORE FINALISASI**

HYPERPARAMETER TUNING UNTUK MODEL TERBAIK (RANDOM FOREST DAN XGBOOST)
"""

from sklearn.model_selection import RandomizedSearchCV
from xgboost import XGBClassifier
import numpy as np

# Definisikan model
xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")

# Tentukan hyperparameter grid
param_dist = {
    'n_estimators': [100, 300, 500],
    'max_depth': [3, 6, 9],
    'learning_rate': np.linspace(0.01, 0.2, 5),
    'subsample': np.linspace(0.6, 1.0, 3)
}

# Lakukan RandomizedSearchCV (coba 20 kombinasi secara acak)
random_search = RandomizedSearchCV(
    xgb, param_dist, n_iter=20, cv=3, scoring='roc_auc',
    n_jobs=-1, verbose=2, random_state=42
)
random_search.fit(X_train_resampled, y_train_resampled)

# Cetak hasil terbaik
print("Best parameters:", random_search.best_params_)
print("Best ROC-AUC Score:", random_search.best_score_)