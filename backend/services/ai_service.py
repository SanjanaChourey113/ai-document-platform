from transformers import pipeline

# Load once (important)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def generate_summary(text):
    try:
        # HuggingFace has input limit, so trim
        text = text[:1000]

        result = summarizer(
            text,
            max_length=120,
            min_length=30,
            do_sample=False
        )

        return result[0]['summary_text']

    except Exception as e:
        return f"Summary error: {str(e)}"


def extract_metadata(text):
    try:
        words = text.split()

        # Simple keyword extraction
        keywords = list(set(words))

        return {
            "keywords": keywords[:10],
            "length": len(text),
            "type": "document"
        }

    except Exception as e:
        return {"error": str(e)}
    



# reuse your existing model OR create new
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def generate_answer(context, question):
    try:
        result = qa_pipeline(
            question=question,
            context=context
        )

        return result["answer"]

    except Exception as e:
        return f"Error: {str(e)}"