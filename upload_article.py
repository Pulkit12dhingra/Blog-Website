import pypandoc
import argparse
import os

def docx_to_html(docx_path, html_path):
    output = pypandoc.convert_file(
        docx_path,
        'html',
        outputfile=html_path,
        extra_args=['--highlight-style=tango']  # Apply syntax highlighting
    )
    return output

def clean_html(html_path):
    with open(html_path, "r") as file:
        html_content = file.read()
        
        # find the line <p>&lt;pre&gt;&lt;code class=”language-python”&gt;</p> and replace it with <pre><code class=”language-python”>
        html_content = html_content.replace("<p>&lt;pre&gt;&lt;code class=”language-python”&gt;</p>", "<pre><code class=”language-python”>")

        # find the line <p>&lt;code&gt;&lt;/pre&gt;</p> and replace it with </code></pre>
        html_content = html_content.replace("<p>&lt;code&gt;&lt;/pre&gt;</p>", "</code></pre>")

        # put the content in body block
        html_content = f"""<body>
         <div class="p-3 mb-2 bg-secondary-subtle text-secondary-emphasis">
        {html_content}
        </div>
        </body>
        """

        # add a header block and link the css file
        html_content = f"""<!DOCTYPE html>
        <html>
        <head>
            <title>Article</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
            <div class="p-3 mb-2 bg-primary-subtle text-primary-emphasis">
            <div class="d-flex justify-content-between align-items-center">
            <h1 class="mb-0">Pulkit's Blog Website</h1>
            <!-- Right-aligned paragraph -->
            <p class="mb-0">
             Please review my <a href="https://pulkit-blog-website.onrender.com/#">Blog Website</a> for more such articles
             <br>
             Know more about me at: <a href="https://pulkit12dhingra.github.io/portfolio/" target="_blank">Portfolio</a> | <a href="https://pulkit12dhingra.github.io/portfolio/" target="_blank">LinkedIn</a>
              <br>
            </div>
             </p>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.2.0/styles/default.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.2.0/highlight.min.js"></script>
            <script>hljs.highlightAll();</script>
            <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
            </div>
        </head>

        {html_content}
        </html>"""

    with open(html_path, "w") as file:
        file.write(html_content)

    return "Html saved to the location"

def main():
    parser = argparse.ArgumentParser(description="Convert DOCX to HTML with syntax highlighting.")
    parser.add_argument("docx_filename", help="The DOCX file to convert.")
    args = parser.parse_args()

    docx_filename = args.docx_filename
    html_filename = os.path.splitext(os.path.basename(docx_filename))[0] + ".html"
    html_path = os.path.join("templates", "Articles", html_filename)

    # Convert DOCX to HTML with syntax highlighting
    docx_to_html(docx_filename, html_path)
    clean_html(html_path)

if __name__ == "__main__":
    main()
    # Sample usage:
    # python /Users/pulkit/Desktop/projects/blog-website/upload_article.py /path/to/your/article.docx
