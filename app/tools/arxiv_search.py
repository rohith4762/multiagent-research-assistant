import arxiv

arxiv_client = arxiv.Client(page_size=5, delay_seconds=5.0, num_retries=3)

def search_arxiv(query, max_results=3):
    search = arxiv.Search(query=query, max_results=max_results)
    docs = []
    for r in arxiv_client.results(search):
        docs.append(
            f"Published: {r.published.date()}\n"
            f"Title: {r.title}\n"
            f"Authors: {', '.join(a.name for a in r.authors)}\n"
            f"Summary: {r.summary[:2000]}"
        )
    return "\n\n".join(docs) if docs else "No good Arxiv Result was found"
