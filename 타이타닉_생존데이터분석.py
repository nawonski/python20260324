import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from urllib.request import urlopen

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")

# Step 1: 타이타닉 데이터셋 로드
print("=" * 50)
print("타이타닉호 생존데이터 분석")
print("=" * 50)

# 온라인에서 직접 로드
url = "https://raw.githubusercontent.com/pandas-dev/pandas/master/doc/data/titanic.csv"
df = pd.read_csv(url)

print("\n[1] 원본 데이터 정보")
print(f"데이터 크기: {df.shape}")
print(f"\n데이터 타입:\n{df.dtypes}")
print(f"\n처음 5행:\n{df.head()}")

# Step 2: 데이터 클랜징
print("\n" + "=" * 50)
print("[2] 데이터 클랜징")
print("=" * 50)

# 결측치 확인
print("\n결측치 현황:")
missing_data = df.isnull().sum()
print(missing_data[missing_data > 0])

# 분석에 필요한 컬럼만 선택 (Survived, Sex)
df_cleaned = df[['Survived', 'Sex']].copy()

# 결측치 제거
print(f"\n클랜징 전 데이터 크기: {df_cleaned.shape[0]}행")
df_cleaned = df_cleaned.dropna()
print(f"클랜징 후 데이터 크기: {df_cleaned.shape[0]}행")

# Sex 컬럼 값 확인
print(f"\n성별 분포:")
print(df_cleaned['Sex'].value_counts())

# Step 3: 남성과 여성의 생존율 계산
print("\n" + "=" * 50)
print("[3] 성별별 생존율 분석")
print("=" * 50)

# 성별별 생존율
survival_by_gender = df_cleaned.groupby('Sex')['Survived'].agg(['sum', 'count', 'mean'])
survival_by_gender.columns = ['생존자수', '전체인원', '생존율']
print(f"\n생존율 통계 (생존율은 0~1 범위):")
print(survival_by_gender)

# 백분율로 표시
print(f"\n생존율 (백분율):")
for gender in df_cleaned['Sex'].unique():
    survival_rate = df_cleaned[df_cleaned['Sex'] == gender]['Survived'].mean() * 100
    print(f"{gender}: {survival_rate:.2f}%")

# Step 4: 그래프 시각화
print("\n" + "=" * 50)
print("[4] 그래프 생성 중...")
print("=" * 50)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 그래프 1: 생존율 비교 (막대 그래프)
survival_rates = df_cleaned.groupby('Sex')['Survived'].mean() * 100
colors = ['#FF6B6B', '#4ECDC4']
axes[0].bar(survival_rates.index, survival_rates.values, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
axes[0].set_ylabel('Survival Rate (%)', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Gender', fontsize=12, fontweight='bold')
axes[0].set_title('Survival Rate by Gender', fontsize=14, fontweight='bold')
axes[0].set_ylim(0, 100)
axes[0].grid(axis='y', alpha=0.3)

# 각 바에 생존율 값 표시
for i, (gender, rate) in enumerate(survival_rates.items()):
    axes[0].text(i, rate + 2, f'{rate:.1f}%', ha='center', fontsize=11, fontweight='bold')

# 그래프 2: 성별별 생존/사망 인원수 (누적 막대 그래프)
survival_counts = df_cleaned.groupby(['Sex', 'Survived']).size().unstack(fill_value=0)
survival_counts.columns = ['Dead', 'Survived']

x_pos = np.arange(len(survival_counts.index))
width = 0.6

axes[1].bar(x_pos, survival_counts['Dead'], width, label='Dead', color='#FF6B6B', alpha=0.8, edgecolor='black', linewidth=2)
axes[1].bar(x_pos, survival_counts['Survived'], width, bottom=survival_counts['Dead'], 
           label='Survived', color='#4ECDC4', alpha=0.8, edgecolor='black', linewidth=2)

axes[1].set_ylabel('Number of People', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Gender', fontsize=12, fontweight='bold')
axes[1].set_title('Survival Count by Gender', fontsize=14, fontweight='bold')
axes[1].set_xticks(x_pos)
axes[1].set_xticklabels(survival_counts.index)
axes[1].legend(loc='upper right', fontsize=11)
axes[1].grid(axis='y', alpha=0.3)

# 각 섹션에 수치 표시
for i, gender in enumerate(survival_counts.index):
    dead = survival_counts.loc[gender, 'Dead']
    survived = survival_counts.loc[gender, 'Survived']
    axes[1].text(i, dead/2, str(dead), ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    axes[1].text(i, dead + survived/2, str(survived), ha='center', va='center', fontsize=10, fontweight='bold', color='white')

plt.tight_layout()

# 그래프 저장
output_file = r'c:\work\타이타닉_생존율분석.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n그래프가 저장되었습니다: {output_file}")

plt.show()

print("\n" + "=" * 50)
print("분석 완료!")
print("=" * 50)
