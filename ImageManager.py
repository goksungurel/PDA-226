import io
import requests
from PIL import Image
from urllib.parse import quote

class ImageManager:
    def __init__(self):
        self.url = "https://image.pollinations.ai/prompt/"
        #the url needed to prompt the images, pollinations

        self.genreSums = {
           "Pop": "vibrant pop art aesthetic, bright neon accents, clean modern design",
            "Rock": "gritty rock aesthetic, high contrast, vintage vinyl texture",
            "Hip-Hop / Rap": "urban street art aesthetic, bold graffiti elements, dramatic lighting",
            "Electronic": "cyberpunk synthwave style, neon glows, futuristic digital art",
            "Indie": "dreamy lo-fi aesthetic, pastel colors, vintage film grain",
            "R&B / Soul": "smooth retro soul aesthetic, warm moody lighting, elegant minimalist design",
            "Jazz": "classic monochrome jazz club aesthetic, smoky atmosphere, abstract geometric art",
            "Metal": "dark heavy metal aesthetic, intricate high-contrast illustration, aggressive themes",
            "Türk Pop": "modern bright aesthetic, colorful Mediterranean vibe, energetic design",
            "Klasik": "timeless classical fine art aesthetic, elegant oil painting texture, orchestral elegance"
        }
        #dictonary that stores the necessary prompts for the images
        #depending on genres

    def genCover(self, prompt, genre):
        style = self.genreSums.get(genre, "music album cover design")
        fullPrompt = f"album cover art, {prompt}, {style}, no text"
        #uses the genre desc.s above to prompt an image

        try:
            secure = quote(fullPrompt)
            url2 = f"{self.url}{secure}?width=600&height=600&nologo=true"
            #encoding the url to make it safer
            #quote turns unsafe chars (like the space) into safe chars (like %20)
            #so it doesent break

            response = requests.get(url2, timeout=90)
            response.raise_for_status()

            img = Image.open(io.BytesIO(response.content)).convert("RGB")
            #to make sure the format isnt something silly like RGBA
            #or greyscale
            return img
        
        except Exception as e:
            print(f"Image generation error: {e}")
            return None
        
    def resizeForGUI(self, img, targetSize = (250, 250)):
        if img:
            return img.resize(targetSize, Image.Resampling.LANCZOS)
        return None