import pandas as pd
from bertopic import BERTopic
import nltk
from nltk.tokenize import word_tokenize

# Load necessary NLTK data
nltk.download('punkt')

# Function to process text (optional, depending on how clean your text is)
def preprocess_text(text):
    # Tokenize and remove unwanted characters (simple example)
    tokens = word_tokenize(text.lower())
    return ' '.join(tokens)

# Load CSV file
df = pd.read_csv("master.csv")

# Extract the dialogues
dialogues = df['Dialogue'].apply(preprocess_text).tolist()

# Create and fit the BERTopic model
model = BERTopic()
topics, probs = model.fit_transform(dialogues)

# Display the topics
print("Topics discovered:")
for topic_num, words in model.get_topics():
    print(f"Topic {topic_num}:")
    print([word for word, _ in words[:5]])

# Map topics to emotions based on the words in each topic
# Define a simple mapping of keywords to emotions
emotion_mapping = {
    "anger": ["fight", "hate", "angry", "violence", "rage", "conflict"],
    "happiness": ["happy", "joy", "excited", "love", "laugh", "smile"],
    "fear": ["scared", "frightened", "danger", "threat", "horror"],
    "sadness": ["cry", "tears", "sad", "loss", "grief"],
    "surprise": ["surprised", "shock", "amazed", "unexpected"],
    "disgust": ["disgust", "sick", "gross", "nasty"]
}

# Function to map topics to emotions
def map_topic_to_emotion(topic_words):
    for emotion, keywords in emotion_mapping.items():
        if any(keyword in topic_words for keyword in keywords):
            return emotion
    return "neutral"  # Default if no emotion is found

# Now, for each dialogue, find the corresponding topic and predict the emotion
df['Topic'] = topics
df['Emotion'] = df['Topic'].apply(lambda topic: map_topic_to_emotion([word for word, _ in model.get_topics()[topic]]))

# Display the dialogue along with its predicted emotion
for index, row in df.iterrows():
    print(f"Dialogue: {row['Dialogue']}")
    print(f"Predicted Emotion: {row['Emotion']}")
    print("------")
