from typing import List, Dict, Any
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

class ChatEngine:
    def __init__(self):
        # Initialize Ollama
        self.llm = Ollama(model="llama2")
        self.conversation_history = []

    def _create_prompt(self) -> ChatPromptTemplate:
        """
        Create the prompt template for the chat.
        """
        template = """Answer the question based on the following context:

Context:
{context}

Question: {question}

Answer:"""
        
        return ChatPromptTemplate.from_template(template)

    def _format_context(self, search_results: List[Dict[str, Any]]) -> str:
        """
        Format the search results into a context string.
        """
        context_parts = []
        for result in search_results:
            source = result["metadata"]["source"]
            page = result["metadata"]["page"]
            text = result["text"]
            context_parts.append(f"From {source} (Page {page}):\n{text}\n")
        
        return "\n".join(context_parts)

    def generate_response(self, query: str, relevant_docs: List[Dict[str, Any]], chat_history: List[Dict[str, str]] = None) -> str:
        try:
            context = "\n".join([doc["text"] for doc in relevant_docs])
            prompt = f"""Based on the following context, please answer the question. If the answer cannot be found in the context, say so.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"""
            response = self.llm.invoke(prompt)
            return response.strip()
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error while generating the response. Please try again."

    def chat(self, query: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process a chat query and return the response with sources.
        """
        # Format the context from search results
        context = self._format_context(search_results)
        
        # Create the chain
        chain = (
            {"context": lambda x: x["context"], "question": lambda x: x["question"]}
            | self._create_prompt()
            | self.llm
            | StrOutputParser()
        )
        
        # Get the response
        response = chain.invoke({
            "context": context,
            "question": query
        })
        
        # Store in conversation history
        self.conversation_history.append({
            "query": query,
            "response": response,
            "sources": [{
                "source": result["metadata"]["source"],
                "page": result["metadata"]["page"]
            } for result in search_results]
        })
        
        return {
            "response": response,
            "sources": [{
                "source": result["metadata"]["source"],
                "page": result["metadata"]["page"]
            } for result in search_results]
        }

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get the conversation history.
        """
        return self.conversation_history

    def clear_history(self) -> None:
        """
        Clear the conversation history.
        """
        self.conversation_history = [] 