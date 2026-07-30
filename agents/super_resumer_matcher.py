"""
Super Resumer Resume Matcher
RAG-based resume matching using LangChain for C# and Python AI roles
"""

from typing import Dict, Any, List, Optional
try:
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    from langchain.embeddings import OpenAIEmbeddings
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    from langchain.chat_models import ChatOpenAI
import logging
import os

# Make FAISS optional
try:
    from langchain.vectorstores import FAISS
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("FAISS not available, using fallback matching without vector stores")

logger = logging.getLogger(__name__)


class SuperResumerMatcher:
    """RAG-based resume matcher for Super Resumer."""
    
    def __init__(self, config, openrouter_api_key: str = None):
        self.config = config
        self.openrouter_api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
        self.match_threshold = config.MATCH_THRESHOLD
        
        # Initialize embeddings with OpenRouter (or fallback to OpenAI)
        try:
            if self.openrouter_api_key:
                # Use OpenRouter for embeddings
                self.embeddings = OpenAIEmbeddings(
                    openai_api_key=self.openrouter_api_key,
                    openai_api_base="https://openrouter.ai/api/v1"
                )
            else:
                # Fallback to OpenAI
                self.embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize embeddings: {str(e)}")
            self.embeddings = None
        
        # Resume stores
        self.csharp_vectorstore = None
        self.python_vectorstore = None
        
        # Initialize LLM for matching analysis
        self.llm = self._initialize_llm()
        
    def _initialize_llm(self):
        """Initialize LLM for matching analysis."""
        try:
            if self.openrouter_api_key:
                return ChatOpenAI(
                    openai_api_key=self.openrouter_api_key,
                    openai_api_base="https://openrouter.ai/api/v1",
                    model="anthropic/claude-3-opus",  # or another model
                    temperature=0
                )
            else:
                return ChatOpenAI(
                    openai_api_key=self.config.OPENAI_KEY,
                    model="gpt-4",
                    temperature=0
                )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            return None
    
    def load_resume(self, resume_path: str) -> str:
        """Load resume text from file."""
        try:
            if resume_path.endswith('.pdf'):
                # PDF parsing
                import PyPDF2
                with open(resume_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                return text
            elif resume_path.endswith('.txt'):
                with open(resume_path, 'r') as file:
                    return file.read()
            else:
                logger.warning(f"Unsupported resume format: {resume_path}")
                return ""
        except Exception as e:
            logger.error(f"Error loading resume {resume_path}: {str(e)}")
            return ""
    
    def create_vector_store(self, resume_text: str):
        """Create vector store from resume text."""
        if not self.embeddings or not resume_text:
            return None
        
        if not FAISS_AVAILABLE:
            logger.warning("FAISS not available, returning text chunks instead")
            # Return chunks directly when FAISS is not available
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(resume_text)
            return chunks
            
        try:
            # Split resume into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            
            chunks = text_splitter.split_text(resume_text)
            
            # Create documents
            documents = [Document(page_content=chunk) for chunk in chunks]
            
            # Create vector store
            vectorstore = FAISS.from_documents(documents, self.embeddings)
            
            return vectorstore
            
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            return None
    
    def load_resumes(self):
        """Load and index both C# and Python AI resumes."""
        logger.info("Loading resumes for matching...")
        
        # Load C# resume
        csharp_text = self.load_resume(self.config.RESUME_C_SHARP)
        if csharp_text:
            self.csharp_vectorstore = self.create_vector_store(csharp_text)
            if self.csharp_vectorstore:
                logger.info("C# resume loaded successfully")
            else:
                logger.warning("C# resume loading had issues")
        else:
            logger.warning("C# resume not found or could not be loaded")
        
        # Load Python AI resume
        python_text = self.load_resume(self.config.RESUME_PYTHON_AI)
        if python_text:
            self.python_vectorstore = self.create_vector_store(python_text)
            if self.python_vectorstore:
                logger.info("Python AI resume loaded successfully")
            else:
                logger.warning("Python AI resume loading had issues")
        else:
            logger.warning("Python AI resume not found or could not be loaded")
    
    def detect_tech_stack(self, job_description: str) -> str:
        """Detect if job requires C# or Python AI skills."""
        job_desc_lower = job_description.lower()
        
        csharp_keywords = ['c#', '.net', 'asp.net', 'c-sharp', 'microsoft']
        python_keywords = ['python', 'machine learning', 'ai', 'artificial intelligence', 
                          'deep learning', 'nlp', 'pytorch', 'tensorflow']
        
        csharp_score = sum(1 for keyword in csharp_keywords if keyword in job_desc_lower)
        python_score = sum(1 for keyword in python_keywords if keyword in job_desc_lower)
        
        if csharp_score > python_score:
            return 'csharp'
        elif python_score > csharp_score:
            return 'python_ai'
        else:
            return 'ambiguous'  # Could be either

    def _invoke_llm(self, prompt: str) -> str:
        """Call ChatOpenAI with LangChain v1 invoke API."""
        response = self.llm.invoke(prompt)
        if hasattr(response, "content"):
            return response.content
        return str(response)
    
    def calculate_match_score(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate match score for a job using RAG or fallback."""
        if not self.llm:
            return {"match_score": 0, "analysis": "LLM not available"}
        
        job_description = job.get('description', '')
        if not job_description:
            return {"match_score": 0, "analysis": "No job description"}
        
        # Detect appropriate resume
        tech_stack = self.detect_tech_stack(job_description)
        
        # Select appropriate resume data
        resume_data = None
        resume_type = "Unknown"
        
        if tech_stack == 'csharp' and self.csharp_vectorstore:
            resume_data = self.csharp_vectorstore
            resume_type = "C# Developer"
        elif tech_stack == 'python_ai' and self.python_vectorstore:
            resume_data = self.python_vectorstore
            resume_type = "Python AI Developer"
        else:
            # Use both or default to one
            if self.csharp_vectorstore:
                resume_data = self.csharp_vectorstore
                resume_type = "C# Developer (default)"
            elif self.python_vectorstore:
                resume_data = self.python_vectorstore
                resume_type = "Python AI Developer (default)"
            else:
                return {"match_score": 0, "analysis": "No resumes loaded"}
        
        try:
            # Check if using vector store or text chunks
            if FAISS_AVAILABLE and hasattr(resume_data, 'as_retriever'):
                # Use RAG with vector store
                from langchain.chains import RetrievalQA
                qa_chain = RetrievalQA.from_chain_type(
                    llm=self.llm,
                    chain_type="stuff",
                    retriever=resume_data.as_retriever(search_kwargs={"k": 3})
                )
                
                # Analyze match
                analysis_prompt = f"""
                Analyze this job description and determine how well it matches the resume context provided.
                Job Description: {job_description}
                
                Provide a match score from 0-100 and explain your reasoning.
                Consider: skills match, experience level, role alignment, and requirements.
                
                Return your answer in this format:
                MATCH_SCORE: [score]
                ANALYSIS: [your analysis]
                RESUME_TYPE: [resume type used]
                """
                
                result = qa_chain.run(analysis_prompt)
            else:
                # Use direct text analysis with resume chunks
                resume_text = "\n".join(resume_data) if isinstance(resume_data, list) else str(resume_data)
                
                analysis_prompt = f"""
                Analyze this job description and determine how well it matches the resume provided.
                
                Job Description: {job_description}
                
                Resume: {resume_text[:2000]}  # First 2000 chars to avoid token limits
                
                Provide a match score from 0-100 and explain your reasoning.
                Consider: skills match, experience level, role alignment, and requirements.
                
                Return your answer in this format:
                MATCH_SCORE: [score]
                ANALYSIS: [your analysis]
                RESUME_TYPE: [resume type used]
                """
                
                result = self._invoke_llm(analysis_prompt)
            
            # Parse result (same for both methods)
            match_score = 0
            analysis = "Analysis failed"
            
            for line in result.split('\n'):
                if 'MATCH_SCORE:' in line:
                    try:
                        match_score = int(line.split('MATCH_SCORE:')[1].strip())
                    except:
                        pass
                elif 'ANALYSIS:' in line:
                    analysis = line.split('ANALYSIS:')[1].strip()
            
            return {
                "match_score": match_score,
                "analysis": analysis,
                "resume_type": resume_type,
                "tech_stack_detected": tech_stack
            }
            
        except Exception as e:
            logger.error(f"Error calculating match score: {str(e)}")
            # Fallback to keyword-based matching
            logger.info("Using fallback keyword-based matching")
            return self._fallback_match_score(job_description, resume_type, tech_stack)
            
            # Parse result (same for both methods)
            match_score = 0
            analysis = "Analysis failed"
            
            for line in result.split('\n'):
                if 'MATCH_SCORE:' in line:
                    try:
                        match_score = int(line.split('MATCH_SCORE:')[1].strip())
                    except:
                        pass
                elif 'ANALYSIS:' in line:
                    analysis = line.split('ANALYSIS:')[1].strip()
            
            return {
                "match_score": match_score,
                "analysis": analysis,
                "resume_type": resume_type,
                "tech_stack_detected": tech_stack
            }
            
        
    def _fallback_match_score(self, job_description: str, resume_type: str, tech_stack: str) -> Dict[str, Any]:
        """Fallback keyword-based matching when LLM fails - more generous scoring."""
        job_desc_lower = job_description.lower()
        
        # Define keywords based on resume type
        if 'c#' in resume_type.lower() or tech_stack == 'csharp':
            keywords = ['c#', '.net', 'asp.net', 'c-sharp', 'microsoft', 'sql server', 'azure', 'entity framework', 'visual studio', 'developer', 'backend', 'fullstack', 'software']
            base_score = 75  # Higher base score for C# jobs
        else:  # Python/AI
            keywords = ['python', 'machine learning', 'ai', 'artificial intelligence', 'deep learning', 'nlp', 'pytorch', 'tensorflow', 'pandas', 'numpy', 'scikit-learn', 'data science', 'developer', 'engineer']
            base_score = 80  # Higher base score for Python/AI jobs
        
        # Count keyword matches
        keyword_matches = sum(1 for keyword in keywords if keyword in job_desc_lower)
        
        # Calculate match score based on keyword density - more generous
        match_score = min(98, base_score + (keyword_matches * 3))  # Higher base, +3% per keyword
        
        # Boost score for well-matching jobs
        if keyword_matches >= 3:
            match_score = min(99, match_score + 5)  # Additional boost for good matches
        
        # Create analysis
        matched_keywords = [kw for kw in keywords if kw in job_desc_lower]
        analysis = f"Keyword-based matching: Found {len(matched_keywords)} matching keywords: {', '.join(matched_keywords[:5])}"
        
        return {
            "match_score": match_score,
            "analysis": analysis,
            "resume_type": resume_type,
            "tech_stack_detected": tech_stack
        }
    
    def filter_by_threshold(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter jobs by match threshold."""
        matched_jobs = []
        
        for job in jobs:
            match_result = self.calculate_match_score(job)
            job['match_analysis'] = match_result
            job['match_score'] = match_result.get('match_score', 0)
            
            if job['match_score'] >= self.match_threshold:
                job['status'] = 'pending_review'  # For manual review
                matched_jobs.append(job)
            else:
                job['status'] = 'rejected'
                job['rejection_reason'] = f"Match score {job['match_score']}% below threshold {self.match_threshold}%"
        
        logger.info(f"Filtered {len(jobs)} jobs, {len(matched_jobs)} passed threshold")
        
        return matched_jobs