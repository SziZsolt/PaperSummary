from ai_engine import PDFSummarizerAI

def main():
    ai = PDFSummarizerAI()
    ai.load_models()

    text = (
        "This paper introduces a transformer-based method for summarizing "
        "scientific documents. The model is fine-tuned with domain adapters "
        "and evaluated on specialized datasets."
    )

    out = ai.generate_summary(text, "nlp")
    print("SUMMARY:")
    print(out)

if __name__ == "__main__":
    main()