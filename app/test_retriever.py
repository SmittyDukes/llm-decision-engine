from retriever import build_index, retrieve

#Build the index from your policy files
index, all_chunks = build_index()

#run a test query
query = "my power forward has 4 fouls in the third quarter should i sit him"

results = retrieve(query, index, all_chunks, k=3)

print(f'\nQuery: {query}\n')
print("Top retrieved chunks:\n")
for i, result in enumerate(results):
    print(f"[{i+1}] Source: {result['source']} | Score: {result['score']:.4f}")
    print(f"    {result['text'][:200]}...")
    print()