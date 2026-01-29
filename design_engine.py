import re
from openai import OpenAI

class BrandDesigner:
    def __init__(self):
        pass

    def generate_design_concept(self, api_key, brand_info, product_info):
        """
        Generates a design concept text and extracts an image prompt.
        Returns a tuple: (full_text_response, image_prompt)
        """
        if not api_key:
            return ("請輸入 OpenAI API Key 以開始設計。\nPlease enter your OpenAI API Key to start designing.", None)
        
        client = OpenAI(api_key=api_key)
        
        system_prompt = "你是一位世界級的工業設計師，擅長將品牌識別轉化為實體產品設計。請用繁體中文回答。"
        
        user_prompt = f"""
        品牌資訊:
        - 名稱: {brand_info.get('name')}
        - 核心關鍵字: {brand_info.get('keywords')}
        - 品牌色系: {brand_info.get('colors')}
        
        產品需求:
        - 產品類型: {product_info.get('type')}
        - 材質偏好: {product_info.get('material')}
        - 特殊需求: {product_info.get('features')}
        
        請提供一個詳細的產品設計概念，包含：
        1. 設計理念 (Concept): 為什麼這樣設計符合品牌形象？
        2. 外觀描述 (Visuals): 形狀、線條、顏色應用。
        3. 功能亮點 (Features): 如何滿足特殊需求。
        
        最後，請務必提供一段詳細的英文提示詞，用於生成產品圖片。
        請將這段英文提示詞放在最後，並以 "IMAGE_PROMPT:" 開頭。
        例如：
        IMAGE_PROMPT: A futuristic thermos bottle, matte black finish with neon blue lines...
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            content = response.choices[0].message.content
            
            # Extract image prompt
            image_prompt = None
            match = re.search(r'IMAGE_PROMPT:\s*(.*)', content, re.DOTALL)
            if match:
                image_prompt = match.group(1).strip()
            
            return content, image_prompt
            
        except Exception as e:
            return (f"發生錯誤: {str(e)}", None)

    def generate_image_url(self, api_key, prompt):
        """
        Generates an image using DALL-E 3 based on the prompt.
        Returns the image URL.
        """
        if not api_key or not prompt:
            return None
            
        client = OpenAI(api_key=api_key)
        
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return response.data[0].url
        except Exception as e:
            print(f"Image generation error: {e}")
            return None
