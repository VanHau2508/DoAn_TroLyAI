from sentence_transformers import SentenceTransformer
import numpy as np
import torch

class PhoBERTEmbedder:
    """
    PhoBERT Embedding Service
    Sử dụng sentence-transformers với PhoBERT model
    """

    def __init__(self, model_name='VoVanPhuc/sup-SimCSE-VietNamese-phobert-base'):
        """
        Initialize PhoBERT model
        - ' 'VoVanPhuc/sup-SimCSE-VietNamese-phobert-base'
        """
        print(f"🚀 Loading PhoBERT model: {model_name}...")

        #Check GPU availability
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"🖥️ Device: {self.device}")

        #Load model
        self.model = SentenceTransformer(model_name, device=self.device)
        print("✅ PhoBERT model loaded successfully")
        print(f"📏 Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
    
    def encode(self, texts, batch_size=32, show_progress=False):
        """
        Encode texts to embeddings
        
        Args:
            texts: str or List[str]
            batch_size: int
            show_progress: bool
            
        Returns:
            numpy.ndarray: embeddings
        """
        if isinstance(texts,str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )

        return embeddings
    
    def encode_query(self, query):
        """
        Encode single query

        Args:
            query: str

        Returns:
            numpy.ndarray: embedding vector
        """
        return self.encode(query)[0]
    
    def similarity(self, text1, text2):
        """
        Calculate cosine similarity between 2 texts
        
        Args:
            text1: str
            text2: str
        Returns:
            float: similarity score(0-1)
        """
        emb1 = self.encode(text1)
        emb2 = self.encode(text2)

        #Cosine similarity
        similarity = np.dot(emb1, emb2.T) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        return float(similarity[0][0])
    
    #Golbal instace
    _embedder = None

    def get_embedder():
        """Get or create embedder instance"""
        global _embedder
        if _embedder is None:
            _embedder = PhoBERTEmbedder()
        return _embedder