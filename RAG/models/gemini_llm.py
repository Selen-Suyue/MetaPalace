from typing import Any, List, Mapping, Optional, Dict
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
import google.generativeai as genai
from PIL.ImageFile import ImageFile

class GeminiLLM(LLM):
    model: str = 'gemini-2.0-flash'
    api_key: str = None

    def _call(self, 
              prompt : str, 
              img: Optional[ImageFile] = None,
              stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        client = genai.configure(
            api_key=self.api_key
        )

        def gen_gemini_params(prompt, img: ImageFile = None):
            if img is None:
                contents = prompt
            else:   
                contents = [
                    prompt,
                    img
                ]
            return contents
        
        contents = gen_gemini_params(prompt, img)
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(
            contents=contents
        )

        return response.text
    
    @property
    def _default_params(self) -> Dict[str, Any]:
        return {}

    @property
    def _llm_type(self) -> str:
        return "gemini"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {**{"model": self.model}, **self._default_params}