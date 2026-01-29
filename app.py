import streamlit as st
from design_engine import BrandDesigner

# Page Configuration
st.set_page_config(
    page_title="AI Design Director",
    page_icon="🎨",
    layout="wide"
)

# Initialize Designer
designer = BrandDesigner()

# Sidebar - Settings
with st.sidebar:
    st.header("設定 (Settings)")
    api_key = st.text_input("Google AI Studio Key", type="password", help="請輸入您的 Google Gemini API Key")
    
    st.markdown("---")
    st.markdown("""
    ### 關於此系統
    這是您的專屬 AI 設計總監。
    - **Engine**: Gemini 3 Flash Preview
    - **Visual**: Imagen 4
    """)

# Main Content
st.title("🎨 首席工業設計師 AI (Industrial Design Director)")
st.markdown("輸入品牌 DNA 與產品需求，為您生成深度設計白皮書與視覺提案。")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 品牌識別 (Brand Identity)")
    brand_name = st.text_input("品牌名稱 (Brand Name)", placeholder="例如：Tesla, Aesop, 或自創品牌")
    brand_keywords = st.text_input("風格關鍵字 (Keywords)", placeholder="例如：極簡、有機參數化、賽博龐克")
    brand_colors = st.text_input("品牌色系 (Color Palette)", placeholder="例如：消光黑、鈦銀、霓虹藍")

with col2:
    st.subheader("2. 產品定義 (Product Spec)")
    product_type = st.text_input("商品類別 (Product Type)", placeholder="例如：空氣清淨機、電競滑鼠、保溫瓶")
    product_material = st.text_input("材質設定 (Materials)", placeholder="例如：航太鋁合金、再生塑料、碳纖維")
    product_features = st.text_area("功能/特殊需求 (Features)", placeholder="例如：隱形觸控介面、模組化設計、可攜式")

# Action
if st.button("✨ 啟動設計提案 (Generate Proposal) ✨", type="primary"):
    if not api_key:
        st.warning("請先在左側欄位輸入 Google API Key。")
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
        
        # 1. 生成文字
        with st.spinner("AI 總監正在撰寫設計白皮書... (Thinking...)"):
            concept_text, image_prompt = designer.generate_design_concept(api_key, brand_info, product_info)
        
        # 顯示文字
        st.subheader("📝 設計提案白皮書")
        st.markdown(concept_text)
        
        # 2. 生成圖片
        if image_prompt:
            st.markdown("---")
            st.caption(f"Visual Prompt: {image_prompt}")
            
            with st.spinner("Imagen 4 正在進行產品渲染... (Rendering...)"):
                generated_image = designer.generate_image_data(api_key, image_prompt)
                
            if generated_image:
                st.subheader("🖼️ 產品視覺渲染圖")
                st.image(generated_image, caption=f"Design Concept: {brand_name} - {product_type}", use_container_width=True)
            else:
                st.error("圖片生成失敗。可能原因：1. Prompt 觸發安全機制 (商標/敏感詞) 2. 您的 API Key 尚未綁定計費帳號 (Free Tier 限制)。")
        else:
            if "文字生成錯誤" in concept_text:
                st.error("文字生成失敗，請檢查 API Key 是否正確。")
