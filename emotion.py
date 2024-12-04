from transformers import pipeline

# Function to identify the emotion of a dialogue
def identify_emotions(dialogue):
    # Use the pre-trained emotion classification pipeline (DistilRoBERTa model)
    classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", tokenizer="j-hartmann/emotion-english-distilroberta-base")
    
    # Get predictions for the given dialogue
    results = classifier(dialogue)
    
    # Extract emotion and confidence score
    emotion = results[0]['label']
    confidence_score = results[0]['score']
    
    return emotion, confidence_score

# Main code to test emotion detection
if __name__ == "__main__":
    dialogue = input("Enter a dialogue: ")

    emotion, confidence = identify_emotions(dialogue)
    
    print(f"Detected Emotion: {emotion}")
    print(f"Confidence Score: {confidence:.4f}")
