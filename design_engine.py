import re
import google.generativeai as genai
from PIL import Image

class BrandDesigner:
    def __init__(self):
        pass

    def generate_design_concept(self, api_key, brand_info, product_info):
        """
        使用 Gemini 3 Flash 生成深度設計白皮書。
        """
        if not api_key:
            return ("請輸入 Google API Key。", None)
        
        try:
            genai.configure(api_key=api_key)
            
            # 【核心設定】使用 Gemini 3 Flash Preview (速度快、邏輯強)
            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            # 設定人設：首席設計總監
            system_prompt = """
            你是一位享譽國際的首席工業設計總監，擅長運用深度的設計哲學、材料科學 (CMF) 與人體工學來闡述設計。
            你的強項是「說故事 (Storytelling)」，能將冰冷的工業產品轉化為富有溫度的藝術品。
            請用繁體中文回答，語氣要專業、優雅、精煉且極具說服力，如同你在為頂級客戶進行提案簡報。
            """
            
            user_prompt = f"""
            {system_prompt}
            
            【設計專案背景】
            品牌識別: {brand_info.get('name')}
            品牌關鍵字: {brand_info.get('keywords')}
            品牌色系: {brand_info.get('colors')}
            
            【產品規格】
            產品類型: {product_info.get('type')}
            材質運用: {product_info.get('material')}
            功能需求: {product_info.get('features')}
            
            請撰寫一份 **極度詳盡、深度極高** 的產品設計提案白皮書。
            請不要只列出清單，請針對每一點進行深入的論述與分析。內容應包含以下章節：

            ### 1. 設計哲學與核心敘事 (Design Philosophy)
            - 請深入探討品牌精神如何轉化為實體線條。
            - 定義這個設計的「靈魂」是什麼？請賦予一個富有詩意的設計代號（例如：Project Horizon 或 Flow State）。
            
            ### 2. 造型語言與美學分析 (Form & Aesthetics)
            - 詳細描述產品的輪廓（Silhouette）、比例（Proportion）與線條流動。
            - 解釋為何選擇這樣的幾何形態？它如何與光影互動？是否有參數化設計的應用？
            
            ### 3. CMF 深度解析 (Color, Material, Finish)
            - **Color (色彩)**: 深入描述色彩的層次、色號與情感意涵。
            - **Material (材質)**: 不只說材質名稱，請解釋選材的物理特性（如導熱性、重量、永續性）。
            - **Finish (工藝)**: 描述表面處理工藝（如噴砂、陽極氧化、PVD鍍膜、拉絲），以及手指觸摸時的細膩觸感。
            
            ### 4. 人體工學與使用者體驗 (Ergonomics & UX)
            - 分析使用者與產品互動的每一個瞬間（拿取、開啟、使用、放置）。
            - 針對「功能需求」提出具體的解決方案，並解釋其運作原理。
            
            ### 5. 情境敘事 (User Scenario)
            - 請描繪一個具體的使用場景：使用者身處何地？光線如何？當他使用這項產品時，感受到了什麼？(請寫得像電影劇本一樣有畫面感)

            ---
            最後，請根據上述設計，提供一段用於 AI 繪圖的英文 Prompt。
            請務必放在最後一行，並以 "IMAGE_PROMPT:" 開頭。
            IMAGE_PROMPT: <在此放入詳細的英文圖片提示詞，包含光影、材質、視角設定>
            """
            
            # 生成內容
            response = model.generate_content(user_prompt)
            content = response.text
            
            # 抓取圖片提示詞
            image_prompt = None
            match = re.search(r'IMAGE_PROMPT:\s*(.*)', content, re.DOTALL)
            if match:
                image_prompt = match.group(1).strip()
            
            return content, image_prompt
            
        except Exception as e:
            return (f"文字生成錯誤 (請檢查 API Key 或模型權限): {str(e)}", None)

    def generate_image_data(self, api_key, prompt):
        """
        使用 Imagen 4 生成圖片，回傳 PIL Image 物件。
        """
        if not api_key or not prompt:
            return None
            
        try:
            genai.configure(api_key=api_key)
            
            # 使用 Imagen 4 正式版
            imagen_model = genai.ImageGenerationModel("imagen-4.0-generate-001")
            
            result = imagen_model.generate_images(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio="1:1",
                safety_filter_level="block_only_high",
                person_generation="allow_adult",
            )
            
            # 回傳第一張圖片
            return result.images[0]
            
        except Exception as e:
            print(f"圖片生成錯誤: {e}")
            return None
