import pandas as pd
import numpy as np

pd.set_option("display.max_columns", 50) # настройка пандас, максимальное кол-во колонок, которое можно увидеть, по длине
pd.set_option("display.width", 90) # обращение к настройкам пандас, макс кол-во столбцов по ширине, сколько будет выводиться в ряд символов, 


# 1. импорт и первичное исследование


url = "https://s3-eu-west-1.amazonaws.com/shanebucket/downloads/uk-500.csv"
# url = "data/uk-500.csv"

df_origin = pd.read_csv(url)

COLUMNS_TO_DROP = [] # если надо удалить какие-то столбцы, кот читать не надо, их можно написать в квадратных скобках, большие буквы - константные переменные - переменная. которая не изменяется

print("\n--- head ---")
print(df_origin.head()) # вывели рялки

print("\n--- info ---")
print(df_origin.info())  # информацию

print("\n--- describe ---") # описывает статистические данные числового типа 
print(df_origin.describe())

print("\n--- describe for str ---") # описывает статистические данные строк
print(df_origin.describe(include=[object]).T)

print("--- null ---")   # посчитали сколько пустых значений и 
# print(df.isna().sum())
print(df_origin.isna().sum().sort_values(ascending=False).head(20))

print("--- duplicated ---")
print(df_origin.duplicated().sum()) # поиск дубликатов

print("--- List columns ---")
# list_col = df.columns
# print(list(list_col))
for i, col in enumerate(df_origin.columns):
    print(f"{i:02d}. {col}")   # выволим информацию списком, какие у нас есть столбики


    
# 2. Очистка данных
df = df_origin.copy()

if COLUMNS_TO_DROP:
    print("\n--- delete columns in list ---")
    df = df.drop(columns=[col for col in COLUMNS_TO_DROP if col in df.columns], errors='ignore')  # df используется чтобы чтото вернуть с оригинала

    # columns = []    
    # for col in COLUMNS_TO_DROP:
    #     if col in df.columns:
    #         columns.append(col)  # аналог верхнего решения
else:
    print("\nCOLUMNS_TO_DROP = []")

  
def standardize_text(s):
    if pd.isna(s):
        return np.nan
    
    if not isinstance(s, str):
        s = str(s)
        
    s = s.strip()
    s = " ".join(s.split())
    
    return s


possible_email_cols = [c for c in df.columns if "email" in c.lower()]
possible_web_cols = [c for c in df.columns if ("web" in c.lower() or "website" in c.lower() or "url" in c.lower())]
possible_phone_cols = [c for c in df.columns if ("phone" in c.lower() or "telephone" in c.lower() or "tel" in c.lower())]
possible_fax_cols = [c for c in df.columns if "fax" in c.lower()]
# F2 горячая клавиша - изменить название, к примеру было df_raw стало df.columns

# генерация списка
# [переменная цикла(с применяемыми операциями) for переменная цикла in где проходимся]
# [0, 1, 2, 3]
# [n for n in range(4)]


print("\nPossible columns:")
print("Email cols:", possible_email_cols)
print("Web cols:", possible_web_cols)
print("Phone cols:", possible_phone_cols)
print("Fax cols:", possible_fax_cols)


# Применение переменные

for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].apply(standardize_text)

# email    
for col in possible_email_cols:
    df[col] = df[col].str.lower()
    
# web    
for col in possible_web_cols:
    df[col] = df[col].str.lower()
    
# clean phone/fax
def clean_phone(x):
    if pd.isna(x):
        return np.nan
    s = str(x)
    s = s.strip()
    
    # plus = ""
    # if s.startswith("+"):
    #     plus = "+"
    
    plus = "+" if s.startswith("+") else ""
    
    # digits = ""
    # for ch in s:
    #     if ch.isdigit():
    #         digits += ch
            
    digits = "".join(ch for ch in s if ch.isdigit())
    
    if digits == "":
        return np.nan
    
    # 'q1w2e3-4567' -> digits='1234567'
    # 'qwe--rty' -> digits=''
    
    return plus + digits
    
for col in possible_phone_cols + possible_fax_cols:
    df[col] = df[col].apply(clean_phone)


def title_if_str(s):
    if pd.isna(s):
        return np.nan
    return str(s).title()

city_cols = [c for c in df.columns if c.lower() in ("city", "city_name", "town")]

address_cols = [c for c in df.columns if c.lower() in ("address")]

name_cols = [c for c in df.columns if c.lower() in ("name", "first_name", "second _name", "last_name", "company_name")]

name_title = city_cols + address_cols + name_cols

if name_title:
    for col in name_title:
        df[col] = df[col].apply(title_if_str)
    print("\n--- name of title ---")
else:
    print("\n--- haven`t name ---")


# 3. создание нових колонок (Feature Engineering)

df["full_name"] = df.first_name + " " + df.last_name

df["city_length"] = df["city"].apply(len) # обращаемся к len и передаем каждое значение рядка

# df["city2"] = df["city"].str.len()

# df["is_gmail"] = 
# print([bool(s) for s in df["email"] if "@gmail.com" in str(s).lower()])

df["is_gmail"] = [True if "@gmail.com" in str(s).lower() else False for s in df["email"]]

# possible_email_cols = [c for c in df.columns if "email" in c.lower()]


# 4. Фильтрация даних

print("\n--- підвибірки ---")

# пользователи с доменом gmail.com
gmail_users = df.loc[df['is_gmail'] == True].copy()
# print(gmail_users)

print("Gmail users:", len(gmail_users))

# работники компании з “LLC” або “Ltd”

# df["company_name"]

df["company_name"] = df["company_name"].fillna("")
# print(df["company_name"].fillna(""))

mask_LLC_Ltd = df.company_name.str.contains(r"\b(LLC|Ltd|llc|LTD|ltd)\b", regex=True, na=False)
# print(mask_LLC_Ltd)

company_llc_ltd = df.loc[mask_LLC_Ltd].copy()
# print(company_llc_ltd)

print("Company LLC and Ltd:", len(company_llc_ltd))


# 5. Позиційна вибірка (iloc)

# iloc[row, col]

try:
    first_10_cols_2_5 = df.iloc[:10, 2:6]
    print("\nПерші 10 рядків + колонки 2–5")
    print(first_10_cols_2_5)
except Exception as e:
    print("Can`t (Перші 10 рядків + колонки 2–5):", e)


every_10th = df.iloc[::10, :].copy()
print("\nevery_10th")
print(every_10th)


random_5 = df.sample(5, random_state=42)
print("\nrandom 5 row")
print(random_5)


# 6. группировка и статистика

print("\n--- Групування та статистика ---") 
print(df["email"].str.split("@").str[-1].value_counts().head(5)) # head(5) - выдели мне конткретное кол-во значений и покажи, str.split("@") - делает возможность сделать значение и обратиться к нему


# city
# agg_by_city = df.groupby("city").agg(
#     people_count = ("city", "size"),
#     avg_people = ("first_name", "mean")
# )#.sort_values(people_count).head(10)

# print(agg_by_city)

df["domain"] = df["email"].str.split("@").str[-1]

agg_by_city = df.groupby("city").agg(
    people_count=("first_name", "count"),
    uniq_dom=("domain", "nunique")
).sort_values("people_count", ascending=False).head(10)

print(agg_by_city)

count_by_city = df.groupby('city').size().reset_index(name='count')

print(count_by_city)



# print(df.head())