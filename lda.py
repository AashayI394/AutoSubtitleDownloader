import pandas as pd
import nltk
import string
from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download stopwords and punkt for nltk
nltk.download('stopwords')
nltk.download('punkt')

# Load the CSV file containing dialogues (assuming it's in the same directory as the script)
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df.iloc[:, 3].dropna().tolist()  # Assuming the 'Dialogue' is in the 4th column (index 3)

# Preprocess the text (remove stopwords, punctuation, tokenize)
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])
    # Tokenize and remove stopwords
    tokens = word_tokenize(text.lower())
    return [word for word in tokens if word not in stop_words]

# Apply LDA model for topic modeling
def apply_lda(dialogues, num_topics=5):
    processed_dialogues = [preprocess_text(dialogue) for dialogue in dialogues]
    
    # Create a dictionary and a corpus for LDA
    dictionary = corpora.Dictionary(processed_dialogues)
    corpus = [dictionary.doc2bow(dialogue) for dialogue in processed_dialogues]
    
    # Train the LDA model
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
    
    return lda_model, dictionary

# Map topics to emotions manually based on the words in the topics
def map_topics_to_emotions(lda_model, num_topics=5):
    emotion_map = {}
    for topic_num in range(num_topics):
        # Get the top words for each topic
        topic_words = lda_model.show_topic(topic_num, topn=5)
        words = [word[0] for word in topic_words]
        
        # Map topics to emotions based on the most frequent words
        if any(word in words for word in ['happy', 'joy', 'excited', 'pleased']):
            emotion_map[topic_num] = 'happy'
        elif any(word in words for word in ['sad', 'cry', 'depressed', 'down']):
            emotion_map[topic_num] = 'sad'
        elif any(word in words for word in ['angry', 'furious', 'rage', 'frustrated']):
            emotion_map[topic_num] = 'angry'
        elif any(word in words for word in ['calm', 'relaxed', 'peaceful', 'serene']):
            emotion_map[topic_num] = 'calm'
        elif any(word in words for word in ['surprised', 'shocked', 'amazed', 'astonished']):
            emotion_map[topic_num] = 'surprised'
        else:
            emotion_map[topic_num] = 'unknown'
    
    return emotion_map

# Predict the emotion of a given dialogue
def predict_emotion(dialogue, lda_model, dictionary, emotion_map):
    # Preprocess the dialogue and convert it to bag-of-words format
    bow = dictionary.doc2bow(preprocess_text(dialogue))
    topic_distribution = lda_model.get_document_topics(bow)
    
    # Find the topic with the highest probability
    topic_num = max(topic_distribution, key=lambda x: x[1])[0]
    
    # Get the emotion associated with the topic
    emotion = emotion_map.get(topic_num, 'unknown')
    return emotion

# Main function to load data, train LDA, and predict emotion
def main(file_path, new_dialogue):
    # Load data
    dialogues = load_data(file_path)
    
    # Apply LDA model
    lda_model, dictionary = apply_lda(dialogues, num_topics=5)
    
    # Map LDA topics to emotions
    emotion_map = map_topics_to_emotions(lda_model, num_topics=5)
    
    # Predict the emotion for a new dialogue
    emotion = predict_emotion(new_dialogue, lda_model, dictionary, emotion_map)
    print(f"Predicted Emotion: {emotion}")

# Example usage
if __name__ == "__main__":
    file_path = 'master.csv'  # File path is in the same directory
    new_dialogue = "I am so happy and excited about this!"  # Test input dialogue
    main(file_path, new_dialogue)
