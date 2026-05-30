import google.generativeai as genai
import json

class GeminiManager:

    def __init__(self, api_key):
        # Configure the API key
        genai.configure(api_key=api_key)

        # Initialize the AI model
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_album_metadata(self, journal_text, genre, era):

        # Instructions and JSON schema to send to Gemini
        prompt = f"""Based on the following journal entry/mood description, music genre, and era, create a fictional music album concept.
        
        Journal : {journal_text}
        Genre : {genre}
        Era : {era}
        
        return ONLY valid JSON with this schema:
        {{
         "album_name": "Fictional and creative album title",
         "artist_name": "Fictional artist or band name",
         "year" : integer (Generate a realistic year that is historically accurate for the chosen {era}),
         "label" : "Fictional record label name",
         "mood_description" : "An evocative and poetic 1-2 sentence description...",
         "cover_prompt" : "A detailed visual description for an AI image generator to create the album cover. It must reflect the visual aesthetic of the {genre} genre and MUST NOT include any text or letters.",
         "lastfm_tags": ["Array of exactly 6 lowercase tags. The first 3 MUST strictly combine the {era} and {genre} (e.g., '2000s hip hop', '00s rap'). The last 3 MUST act as a fallback, focusing ONLY on the {journal_text} and {genre} without the era (e.g., 'dark rap', 'street hip hop') in case exact era matches are rare."]
        }}
        
        """

        # Error handling block (prevents program crashes)
        try:
            # Send the request and retrieve the response text
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Markdown cleanup (Requirement 4)
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip().rstrip("`").strip()
            # Parse the text into a Python Dictionary (JSON)
            album_data = json.loads(text)

            return album_data

        except Exception as e:
            # Log the error and return None in case of failure
            print(f"Gemini API Error : {e}")
            return None
