import streamlit as st
from design_engine import BrandDesigner

st.set_page_config(page_title="Brand Product Designer AI", page_icon="🎨", layout="wide")
designer = BrandDesigner()

with st.sidebar:
    st.header("設定 (Settings)")
    api_key = st.text_input("Google AI Studio Key", type="password")

st.title("🎨 品牌產品設計機器人 (Google Edition)")

col1, col2 = st.columns(2)
with col1:
    st.subheader("1. 品牌資料")
    brand_name = st.text_input("品牌名稱", "Lexus")
    brand_keywords = st.text_input("風格關鍵字", "極簡、未來感")
    brand_colors = st.text_input("品牌色系", "黑、銀")

with col2:
    st.subheader("2. 商品需求")
    product_type = st.text_input("商品類別", "保溫瓶")
    product_material = st.text_input("材質", "鈦金屬")
    product_features = st.text_area("特徵", "參數化紋理")

if st.button("✨ 開始設計 ✨", type="primary"):
    if not api_key:
        st.warning("請輸入 API Key")
    else:
        brand_info = {"name": brand_name, "keywords": brand_keywords, "colors": brand_colors}
        product_info = {"type": product_type, "material": product_material, "features": product_features}
        
        with st.spinner("AI 正在發想設計理念..."):
            concept_text, image_prompt = designer.generate_design_concept(api_key, brand_info, product_info)
        
        st.subheader("📝 設計理念")
        st.markdown(concept_text)
        
        if image_prompt:
            st.info(f"圖片提示詞: {image_prompt}")
            with st.spinner("Imagen 4 正在繪圖中 (這可能需要幾秒鐘)..."):
                # 注意：這裡改呼叫 generate_image_data
                generated_image = designer.generate_image_data(api_key, image_prompt)
                
            if generated_image:
                st.subheader("🖼️ 產品設計圖")
                # 直接顯示圖片物件
                st.image(generated_image, caption=f"{brand_name} - {product_type}", use_container_width=True)
            else:
                st.error("圖片生成失敗，可能是 Prompt 被安全過濾器擋下了，或是模型暫時忙碌。")
