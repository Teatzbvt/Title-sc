import streamlit as st
import random
import pandas as pd

from io import BytesIO

# ========================
# 默认示例词库（可被替换）
# ========================

DEFAULT_FEATURES = [
    "Snapdragon 8 Gen2", "16GB RAM", "108MP Camera", "8000mAh Battery",
    "7.3 inch Display", "1TB Storage", "Screen Fingerprint", "Facial Recognition",
    "Dual SIM", "Android 15 OS", "Electroplated Frame", "Frosted AG Glass Back",
    "Fast Charging", "5G", "Premium Build"
]

DEFAULT_MARKETING_WORDS = [
    "Global Hot Sale", "Limited Time Offer", "Flash Deal", "Exclusive Offer",
    "Super Discount", "Bulk Order", "Factory Direct", "Best Seller",
    "Free Shipping", "Fast Delivery", "Crazy Promotion", "Massive Savings",
    "Top Rated", "Money Back Guarantee", "High Performance", "Durable Design",
    "User Friendly", "Eco Friendly", "Hot Trending", "Must Have",
    "New Arrival", "Best Value", "Clearance Sale", "Season Sale",
    "Lowest Price", "Deal of the Day", "Customer Favorite", "Hot Pick",
    "Limited Stock", "Free Gift", "Bonus Offer", "Price Drop",
    "Online Exclusive", "Shop Now", "Hurry Up", "Don’t Miss",
    "Save Big", "Big Savings"
]

# ========================
# 页面设置
# ========================

st.set_page_config(page_title="📱 阿里国际站 标题生成器")

st.title("📱 阿里国际站 标题生成器 · 完整版")
st.write("输入型号、自定义功能参数、上传营销词，一键生成标题和关键词！")

# 型号输入
model = st.text_input("请输入机型（如 One Plus 12）", value="One Plus 12")

# 功能参数输入
features_input = st.text_area(
    "请输入功能参数（每行一个）",
    value="\n".join(DEFAULT_FEATURES),
    height=200
)
features_list = [line.strip() for line in features_input.split("\n") if line.strip()]

# 营销词上传
uploaded_file = st.file_uploader("上传营销词文件（txt，每行一个）")
if uploaded_file is not None:
    marketing_content = uploaded_file.read().decode("utf-8")
    marketing_list = [line.strip() for line in marketing_content.split("\n") if line.strip()]
else:
    marketing_list = DEFAULT_MARKETING_WORDS

# 生成条数
num = st.slider("选择要生成的条数", min_value=10, max_value=500, step=10, value=50)

# ========================
# 标题生成逻辑
# ========================

def gen_title():
    if len(features_list) < 4:
        return "⚠️ 功能参数至少需要 4 个！"

    parts = random.sample(features_list, 3)
    sell_point_candidates = [f for f in features_list if f not in parts]
    sell_point = random.choice(sell_point_candidates)

    marketing = random.choice(marketing_list)

    pos = random.randint(0, 4)
    title_parts = parts.copy()
    title_parts.append(sell_point)
    title_parts.append(marketing)
    title_parts.insert(pos, model)

    title = " ".join(title_parts)
    length = len(title.replace(",", ""))
    tries = 0

    while (length < 90 or length > 120) and tries < 10:
        parts = random.sample(features_list, 3)
        sell_point_candidates = [f for f in features_list if f not in parts]
        sell_point = random.choice(sell_point_candidates)
        marketing = random.choice(marketing_list)
        pos = random.randint(0, 4)
        title_parts = parts.copy()
        title_parts.append(sell_point)
        title_parts.append(marketing)
        title_parts.insert(pos, model)
        title = " ".join(title_parts)
        length = len(title.replace(",", ""))
        tries += 1

    return title

# ========================
# 关键词生成
# ========================

def gen_keywords_phrases():
    all_phrases = [x.lower() for x in features_list + marketing_list]
    keywords = []
    total_len = 0

    while total_len < 220:
        phrase = random.choice(all_phrases)
        if phrase not in keywords:
            phrase_len = len(phrase.replace(" ", ""))
            if total_len + phrase_len <= 340:
                keywords.append(phrase)
                total_len += phrase_len
            else:
                break
    return "\n".join(keywords)

# ========================
# 生成按钮
# ========================

if st.button("🚀 开始生成"):
    rows = []
    for _ in range(num):
        t = gen_title()
        k = gen_keywords_phrases()
        rows.append([t, k])
    df = pd.DataFrame(rows, columns=["标题", "关键词"])
    st.success(f"已生成 {num} 条数据 ✅")
    st.dataframe(df)

    # 保存 Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Titles')
    processed_data = output.getvalue()

    st.download_button(
        label="📥 点击下载 Excel 文件",
        data=processed_data,
        file_name='阿里国际站标题关键词.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
