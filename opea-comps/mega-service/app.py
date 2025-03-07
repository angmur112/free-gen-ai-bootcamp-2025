# File: app.py
# Description: Example service implementation using the comps framework

# Standard library imports
import os

# Third-party imports
from fastapi import HTTPException

# Local imports
from comps.cores.proto.api_protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
    UsageInfo
)
from comps.cores.mega.constants import ServiceType, ServiceRoleType
from comps import MicroService, ServiceOrchestrator

# Environment variables configuration
EMBEDDING_SERVICE_HOST_IP = os.getenv("EMBEDDING_SERVICE_HOST_IP", "0.0.0.0")
EMBEDDING_SERVICE_PORT = os.getenv("EMBEDDING_SERVICE_PORT", 6000)
LLM_SERVICE_HOST_IP = os.getenv("LLM_SERVICE_HOST_IP", "0.0.0.0")
LLM_SERVICE_PORT = os.getenv("LLM_SERVICE_PORT", 9000)

# Main service class
class ExampleService:
    """Example service that handles chat completion requests."""
    
    def __init__(self, host="0.0.0.0", port=8000):
        """Initialize the service with host and port."""
        os.environ["TELEMETRY_ENDPOINT"] = ""
        self.host = host
        self.port = port
        self.endpoint = "/v1/example-service"
        self.megaservice = ServiceOrchestrator()

    def add_remote_service(self):
        """Configure and add remote LLM service."""
        llm = MicroService(
            name="llm",
            host=LLM_SERVICE_HOST_IP,
            port=LLM_SERVICE_PORT,
            endpoint="/v1/chat/completions",
            use_remote_service=True,
            service_type=ServiceType.LLM,
        )
        self.megaservice.add(llm)
    
    def start(self):
        """Start the service with configured routes."""
        self.service = MicroService(
            self.__class__.__name__,
            service_role=ServiceRoleType.MEGASERVICE,
            host=self.host,
            port=self.port,
            endpoint=self.endpoint,
            input_datatype=ChatCompletionRequest,
            output_datatype=ChatCompletionResponse,
        )
        self.service.add_route(self.endpoint, self.handle_request, methods=["POST"])
        self.service.start()

    async def handle_request(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Handle incoming chat completion requests."""
        try:
            # Prepare Ollama request format
            ollama_request = {
                "model": request.model or "llama3.2:1b",
                "messages": [
                    {
                        "role": "user",
                        "content": request.messages
                    }
                ],
                "stream": False
            }
            
            # Process request through orchestrator
            result = await self.megaservice.schedule(ollama_request)
            
            # Process response
            content = self._process_llm_response(result)
            
            # Create and return formatted response
            return ChatCompletionResponse(
                model=request.model or "example-model",
                choices=[
                    ChatCompletionResponseChoice(
                        index=0,
                        message=ChatMessage(
                            role="assistant",
                            content=content
                        ),
                        finish_reason="stop"
                    )
                ],
                usage=UsageInfo(
                    prompt_tokens=0,
                    completion_tokens=0,
                    total_tokens=0
                )
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def _process_llm_response(self, result):
        """Helper method to process LLM response."""
        if isinstance(result, tuple) and len(result) > 0:
            llm_response = result[0].get('llm/MicroService')
            if hasattr(llm_response, 'body'):
                response_body = b""
                for chunk in llm_response.body_iterator:
                    response_body += chunk
                return response_body.decode('utf-8')
            return "No response content available"
        return "Invalid response format"

# Service initialization
if __name__ == "__main__":
    example = ExampleService()
    example.add_remote_service()
    example.start()