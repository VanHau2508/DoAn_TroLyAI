from app.ai_service.embedder import PhoBERTEmbedder

def test_phobert():
    print("=" * 60)
    print("🧪 TESTING PhoBERT EMBEDDER")
    print("=" * 60)

    # Initialize
    embedder = PhoBERTEmbedder()

    #Test 1: Single text encoding
    print("\n📝 Test 1: Encode single text")
    text = "Hôm nay tôi có lịch học gì?"
    embedding = embedder.encode_query(text)
    print(f"Text: {text}")
    print(f"Embedding shape: {embedding.shape}")
    print(f"Embedding Sample: {embedding[:5]}...")

    #Test 2: Batch encoing
    print("\n📝 Test 2: Encode multiple texts")
    texts = [
        "Lịch học hôm nay",
        "Deadline nào sắp hết hạn?",
        "Lịch thi tuần này"
    ]
    embeddings = embedder.encode(texts)
    print(f"Number of texts: {len(texts)}")
    print(f"Embeddings shape: {embeddings.shape}")

    #Test 3: Similarity
    print("\n📝 Test 3: Similarity calculation")
    text1 = "Hôm nay tôi có lịch học gì?"
    text2 = "Cho tôi xem lịch học hôm nay"
    text3 = "Deadline nào sắp hết hạn?"

    sim_12 = embedder.similarity(text1, text2)
    sim_13 = embedder.similarity(text1, text3)

    print(f"Text 1: {text1}")
    print(f"Text 2: {text2}")
    print(f"Similarity: {sim_12:.4f}")
    print()
    print(f"Text 1: {text1}")
    print(f"Text 3: {text3}")
    print(f"Similarity: {sim_13:.4f}")

    print("\n" + "=" * 60)
    print("✅ PhoBERT test completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_phobert()