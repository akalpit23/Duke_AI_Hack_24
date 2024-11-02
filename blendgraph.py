import bpy
import numpy as np
import os

# Check and import necessary libraries
try:
    import gensim.downloader as api
    from gensim.models import KeyedVectors
    from sklearn.decomposition import PCA
    from sklearn.datasets import fetch_20newsgroups
    import nltk
except ImportError as e:
    print("One or more required libraries are not installed in Blender's Python environment.")
    print("Please install the following libraries before running the script:")
    print("gensim, scikit-learn, nltk")
    import sys
    sys.exit()

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Set random seed for reproducibility
np.random.seed(42)

# Load the pre-trained Word2Vec model
print("Loading Word2Vec model. This may take a few minutes...")
word2vec_model = api.load('word2vec-google-news-300')
print("Model loaded successfully.")

# Preprocessing functions
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation

stop_words = set(stopwords.words('english'))
punctuation = set(punctuation)

def preprocess(text):
    """
    Preprocesses the input text by converting to lowercase, removing non-alphabetic characters,
    tokenizing, and removing stopwords and punctuation.
    """
    # Lowercase the text
    text = text.lower()
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords and punctuation
    tokens = [word for word in tokens if word not in stop_words and word not in punctuation]
    return tokens

# Load the 20 newsgroups dataset
print("Loading dataset...")
data = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))
texts = data.data
labels = data.target
category_names = data.target_names

# Sample a subset of the data for visualization
num_samples = 500  # Adjust as needed; larger numbers may slow down Blender
texts_sampled = texts[:num_samples]
labels_sampled = labels[:num_samples]
label_names = [category_names[label] for label in labels_sampled]

# Preprocess the sampled texts
print("Preprocessing texts...")
processed_texts = [preprocess(text) for text in texts_sampled]

# Compute document embeddings
def get_document_embedding(tokens, model):
    """
    Compute the document embedding by averaging the embeddings of the tokens present in the Word2Vec model.
    """
    valid_embeddings = []
    for token in tokens:
        if token in model:
            valid_embeddings.append(model[token])
    if valid_embeddings:
        # Average the embeddings
        document_embedding = np.mean(valid_embeddings, axis=0)
    else:
        # If no valid embeddings, return a zero vector
        document_embedding = np.zeros(model.vector_size)
    return document_embedding

print("Computing embeddings...")
embeddings = np.array([get_document_embedding(tokens, word2vec_model) for tokens in processed_texts])

print(f"Embedding shape: {embeddings.shape}")

# Apply PCA for dimensionality reduction
print("Applying PCA...")
pca = PCA(n_components=3)  # We use 3 components for 3D visualization in Blender
embeddings_pca = pca.fit_transform(embeddings)
print(f"PCA reduced shape: {embeddings_pca.shape}")

# Normalize embeddings for better visualization within Blender
min_vals = np.min(embeddings_pca, axis=0)
max_vals = np.max(embeddings_pca, axis=0)
embeddings_normalized = (embeddings_pca - min_vals) / (max_vals - min_vals) * 10  # Scale to [0,10]

# Create a new collection for the embeddings visualization
collection_name = "Word2Vec Embeddings"
if collection_name in bpy.data.collections:
    collection = bpy.data.collections[collection_name]
else:
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

# Remove existing objects in the collection (optional)
for obj in collection.objects:
    bpy.data.objects.remove(obj, do_unlink=True)

# Define colors for each category
import random
random.seed(42)
unique_labels = list(set(labels_sampled))
label_colors = {}
for label in unique_labels:
    # Generate a random color
    color = (random.random(), random.random(), random.random(), 1)
    label_colors[label] = color

# Create materials for each label
materials = {}
for label in unique_labels:
    mat = bpy.data.materials.new(name=f"Label_{label}")
    mat.diffuse_color = label_colors[label]
    materials[label] = mat

# Plot the embeddings as spheres in Blender
print("Creating objects in Blender...")
for idx, point in enumerate(embeddings_normalized):
    label = labels_sampled[idx]
    x, y, z = point
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(x, y, z))
    obj = bpy.context.active_object
    # Assign material based on label
    obj.data.materials.append(materials[label])
    # Add the object to the collection
    collection.objects.link(obj)
    # Unlink from the default collection
    bpy.context.scene.collection.objects.unlink(obj)

print("Visualization created successfully.")
