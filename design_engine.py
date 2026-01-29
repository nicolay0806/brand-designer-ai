import re
import google.generativeai as genai

class BrandDesigner:
    def __init__(self):
        pass

    def generate_design_concept(self, api_key, brand_info, product_info):
        """
        使用 Google Gemini 生成設計理念。
        """
        if not api_key:
            return ("請輸入 Google API Key 以開始設計。", None)
        
        try:
            # 設定 Google API
            genai.configure(api_key=api_key)
            
            # 使用 gemini-1.5-flash，這顆模型邏輯跟創意都很強
            model = genai.GenerativeModel('gemini-1.5-flash-001')
            
            system_prompt = "你是一位世界級的工業設計師 (Industrial Designer)，擅長將品牌識別 (Brand DNA) 轉化為實體產品設計。請用繁體中文回答，語氣專業且富有創意。"
            
            user_prompt = f"""
            {system_prompt}

            品牌資訊:
            - 名稱: {brand_info.get('name')}
            - 核心關鍵字: {brand_info.get('keywords')}
            - 品牌色系: {brand_info.get('colors')}
            
            產品需求:
            - 產品類型: {product_info.get('type')}
            - 材質偏好: {product_info.get('material')}
            - 特殊需求: {product_info.get('features')}
            
            請提供一個詳細的產品設計概念 (Design Concept)，結構如下：
            1. **設計核心 (Core Philosophy)**: 為什麼這樣設計符合品牌形象？請運用設計詞彙（如 CMF、人體工學、語意學）。
            2. **造型語言 (Form Language)**: 描述形狀、線條流動、比例。
            3. **功能亮點 (Key Features)**: 針對特殊需求提出的解決方案。
            4. **材質與工藝 (Material & Finish)**: 建議的表面處理方式。
            
            (注意：本版本專注於文字概念生成)
            """
            
            response = model.generate_content(user_prompt)
            return response.text, None # Gemini API 暫時不回傳圖片 Prompt
            
        except Exception as e:
            return (f"發生錯誤: {str(e)}", None)

    def generate_image_url(self, api_key, prompt):
        # Google 的免費 API 暫時不支援直接的圖片生成 URL，這邊先回傳 None
        return None
