import pandas as pd
from sentence_transformers import SentenceTransformer, util
import numpy as np
import faiss

class RecommendationEngine:
    def __init__(self, dataset_path):
        self.dataset = pd.read_csv(dataset_path, encoding='ISO-8859-1')
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Pretrained transformer model
        
        # Preprocess the dataset and handle missing descriptions
        self.dataset['Description'] = self.dataset['Description'].fillna('')
        self.dataset['Title'] = self.dataset['Course_name'].fillna('')
        
        # Generate embeddings for both Title and Description
        self.dataset['Embeddings'] = self.dataset.apply(self._generate_embeddings, axis=1)
        
        # Build FAISS index for fast similarity search
        self.index = self._build_faiss_index()

    def _generate_embeddings(self, row):
        """Generate combined embeddings for the course title and description."""
        text = f"{row['Course_name']} {row['Description']}"
        return self.model.encode(text, convert_to_tensor=True)

    def _build_faiss_index(self):
        """Build a FAISS index for fast similarity search."""
        embeddings = np.array([embedding.cpu().numpy() for embedding in self.dataset['Embeddings']])
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)  # Add embeddings to FAISS index
        return index

    def _find_similar_courses(self, query_embedding, top_n=10):
        """Find the top N most similar courses to the query embedding."""
        D, I = self.index.search(np.array([query_embedding.cpu().numpy()]), top_n)
        return self.dataset.iloc[I[0]]

    def get_recommendations(self, query):
        """Get top recommendations for a given query."""
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        recommendations = self._find_similar_courses(query_embedding)
        return recommendations
