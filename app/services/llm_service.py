from typing import Dict, Optional, List
from datetime import datetime
from fastapi import HTTPException
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import CallbackManager
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PromptRequest(BaseModel):
    prompt: str
    system_context: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 150

class PromptResponse(BaseModel):
    response: str
    metadata: Dict
    safe_prompt: bool

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.llm = OpenAI(
            temperature=0.7,
            openai_api_key=self.api_key,
            max_tokens=150
        )

    def _check_prompt_safety(self, prompt: str) -> bool:
        """
        Basic prompt safety checker to detect potential injection attacks.
        In production, implement more sophisticated checks.
        """
        dangerous_patterns = [
            "ignore previous instructions",
            "disregard safety",
            "bypass security",
            "system command",
            "exec(",
            "eval(",
            ";",  # SQL injection attempt
            "--",  # SQL comment
            "/*",  # SQL comment block
            "{{",  # Template injection
            "${",  # Template injection
            "<script>",  # XSS attempt
        ]
        
        prompt_lower = prompt.lower()
        return not any(pattern.lower() in prompt_lower for pattern in dangerous_patterns)

    def _sanitize_prompt(self, prompt: str) -> str:
        """
        Sanitize the prompt to remove potentially dangerous content.
        """
        # Remove any HTML tags
        import re
        prompt = re.sub(r'<[^>]+>', '', prompt)
        
        # Escape special characters
        special_chars = ['$', '{', '}', '<', '>', '(', ')', ';']
        for char in special_chars:
            prompt = prompt.replace(char, f'\\{char}')
            
        return prompt

    async def generate_response(self, request: PromptRequest) -> PromptResponse:
        """
        Generate a response using the LLM with safety checks and monitoring.
        """
        # Check prompt safety
        is_safe = self._check_prompt_safety(request.prompt)
        if not is_safe:
            raise ValueError("Potentially unsafe prompt detected")

        # Sanitize the prompt
        safe_prompt = self._sanitize_prompt(request.prompt)

        # Create a prompt template with system context if provided
        if request.system_context:
            template = f"{request.system_context}\n\nUser: {{prompt}}\nAssistant:"
        else:
            template = "User: {prompt}\nAssistant:"

        prompt_template = PromptTemplate(
            input_variables=["prompt"],
            template=template
        )

        # Create and run the chain
        chain = LLMChain(
            llm=self.llm,
            prompt=prompt_template
        )

        # Generate response
        try:
            response = await chain.arun(prompt=safe_prompt)
            
            # Collect metadata for monitoring
            metadata = {
                "tokens_used": len(response.split()),
                "prompt_tokens": len(safe_prompt.split()),
                "timestamp": str(datetime.utcnow()),
                "model": "gpt-3.5-turbo",  # Update based on actual model used
                "temperature": request.temperature or 0.7,
                "max_tokens": request.max_tokens or 150
            }

            return PromptResponse(
                response=response,
                metadata=metadata,
                safe_prompt=is_safe
            )

        except Exception as e:
            # Log the error and raise a sanitized version
            # In production, implement proper error logging
            print(f"Error generating response: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Error generating response"
            )

# Initialize the LLM service
llm_service = LLMService()
