import re
import google.generativeai as genai
from PIL import Image

class BrandDesigner:
    def __init__(self):
        pass

    def generate_design_concept(self, api_key, brand_info, product_info):
        if not api_key:
            return ("請輸入 Google API Key。", None)
        
        try:
            genai.configure(api_key=api_key)
            
            # 【修改重點 1】# 改用 Gemini 3 Flash Preview
            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            system_prompt = "你是一位世界級工業設計師。請用繁體中文回答。"
            
            user_prompt = f"""
            {system_prompt}
            品牌: {brand_info.get('name')} ({brand_info.get('keywords')})
            產品: {product_info.get('type')} ({product_info.get('material')})
            需求: {product_info.get('features')}
            
            請提供：
            1. 設計理念
            2. 外觀描述
            3. 功能亮點
            
            最後一行請務必提供英文圖片提示詞，格式為：
            IMAGE_PROMPT: <英文提示詞內容>
            """
            
            response = model.generate_content(user_prompt)
            content = response.text
            
            image_prompt = None
            match = re.search(r'IMAGE_PROMPT:\s*(.*)', content, re.DOTALL)
            if match:
                image_prompt = match.group(1).strip()
            
            return content, image_prompt
            
        except Exception as e:
            return (f"文字生成錯誤: {str(e)}", None)

    def generate_image_data(self, api_key, prompt):
        if not api_key or not prompt:
            return None
            
        try:
            genai.configure(api_key=api_key)
            
            # 【修改重點 2】改用官方文件推薦的 Imagen 4.0 正式版
            imagen_model = genai.ImageGenerationModel("imagen-4.0-generate-001")
            
            result = imagen_model.generate_images(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio="1:1",
                safety_filter_level="block_only_high",
                person_generation="allow_adult",
            )
            return result.images[0]
            
        except Exception as e:
            print(f"圖片生成錯誤: {e}")
            return None
