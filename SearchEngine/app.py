import re
from flask import Flask, render_template, request
from search import Search

app = Flask(__name__)


es = Search()


@app.get('/')
def index():
    return render_template('index.html')

@app.post('/')
def handle_search():
    query = request.form.get('query', '')
    from_ = request.form.get('from_', type=int, default=0)
    size = 5  # Results per page

    # Clean and parse the query (no filters anymore)
    parsed_query = query.strip()

    # Build search query
    if parsed_query:
        search_query = {
            'must': {
                'multi_match': {
                    'query': parsed_query,
                    'fields': ['name^2', 'summary', 'content'],
                }
            }
        }
    else:
        search_query = {
            'must': {
                'match_all': {}
            }
        }

    # Perform the search query
    results = es.search(
        query={
            'bool': {
                **search_query,
            }
        },
        knn={
            'field': 'embedding',
            'query_vector': es.get_embedding(parsed_query),
            'k': 10,
            'num_candidates': 50,
        },
        rank={
            'rrf': {}
        },
        size=size,
        from_=from_,  # This is critical for pagination
    )

    # Pagination logic
    total_results = results['hits']['total']['value']
    total_pages = (total_results + size - 1) // size  # Round up to the nearest whole number
    current_page = from_ // size + 1  # Current page number (1-based)

    # Remove aggregation logic (no more category/filters)
    aggs = {}

    return render_template('index.html', results=results['hits']['hits'],
                           query=query, from_=from_,
                           total=total_results, aggs=aggs,
                           current_page=current_page, total_pages=total_pages)


@app.get('/document/<id>')
def get_document(id):
    document = es.retrieve_document(id)
    title = document['_source']['name']
    paragraphs = document['_source']['content'].split('\n')
    return render_template('document.html', title=title, paragraphs=paragraphs)

@app.cli.command()
def reindex():
    """Regenerate the Elasticsearch index."""
    response = es.reindex()
    print(f'Index with {len(response["items"])} documents created '
          f'in {response["took"]} milliseconds.')

def extract_filters(query):
    # Since we no longer need category or year filters, we just return an empty filter list
    return {}, query


if __name__ == '__main__':
    app.run(debug=True, port=9200)
