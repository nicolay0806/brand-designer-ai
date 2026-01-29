import streamlit as st
from design_engine import BrandDesigner

# Page Configuration
st.set_page_config(
    page_title="Brand Product Designer AI",
    page_icon="🎨",
    layout="wide"
)

# Initialize Designer
designer = BrandDesigner()

# Sidebar - Settings
with st.sidebar:
    st.header("設定 (Settings)")
    api_key = st.text_input("OpenAI API Key", type="password", help="請輸入您的 OpenAI API Key 以啟用生成功能。")
    
    st.markdown("---")
    st.markdown("""
    ### 關於此機器人
    這是一個品牌產品設計助手。
    1. 輸入您的品牌資料。
    2. 描述您想製作的商品。
    3. AI 將為您生成設計理念與產品示意圖。
    """)

# Main Content
st.title("🎨 品牌產品設計機器人 (Brand Product Designer)")
st.markdown("請輸入品牌資訊與商品需求，AI 將為您量身打造設計方案。")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 品牌資料 (Brand Profile)")
    brand_name = st.text_input("品牌名稱 (Brand Name)", placeholder="例如：EcoLife")
    brand_keywords = st.text_input("風格關鍵字 (Keywords)", placeholder="例如：極簡、環保、自然、科技感")
    brand_colors = st.text_input("品牌色系 (Color Palette)", placeholder="例如：森林綠、大地色、米白")

with col2:
    st.subheader("2. 商品需求 (Product Request)")
    product_type = st.text_input("商品類別 (Product Type)", placeholder="例如：保溫瓶、T-shirt、包裝盒")
    product_material = st.text_input("材質偏好 (Materials)", placeholder="例如：304不鏽鋼、再生紙、有機棉")
    product_features = st.text_area("特殊需求/功能 (Features)", placeholder="例如：要有提把、保溫效果好、表面磨砂質感")

# Action
if st.button("✨ 開始設計 (Generate Design) ✨", type="primary"):
    if not api_key:
        st.warning("請先在左側欄位輸入 OpenAI API Key。")
    elif not brand_name or not product_type:
        st.warning("請至少輸入「品牌名稱」與「商品類別」。")
    else:
        brand_info = {
            "name": brand_name,
            "keywords": brand_keywords,
            "colors": brand_colors
        }
        product_info = {
            "type": product_type,
            "material": product_material,
            "features": product_features
        }
        
        with st.spinner("AI 正在發想設計理念... (Generating Concept...)"):
            concept_text, image_prompt = designer.generate_design_concept(api_key, brand_info, product_info)
        
        # Display Concept
        st.subheader("📝 設計理念 (Design Concept)")
        st.markdown(concept_text)
        
        if image_prompt:
            with st.spinner("AI 正在繪製產品設計圖... (Generating Image...)"):
                image_url = designer.generate_image_url(api_key, image_prompt)
                
            if image_url:
                st.subheader("🖼️ 產品設計圖 (Product Visual)")
                st.image(image_url, caption=f"{brand_name} - {product_type} Design", use_container_width=True)
            else:
                st.error("圖片生成失敗，請檢查 API Key 權限或稍後再試。")
        else:
            if "請輸入 OpenAI API Key" not in concept_text:
                st.info("未能提取圖片生成提示詞，僅提供文字設計概念。")
