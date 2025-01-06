from itemadapter import ItemAdapter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from reportlab.lib.colors import black, grey

class FandomScraperPipeline:
    def process_item(self, item, spider):
        # Existing pipeline functionality
        return item

class PdfPipeline:
    def open_spider(self, spider):
        # Open PDF document and initialize the canvas
        self.filename = "scraped_data.pdf"
        self.c = canvas.Canvas(self.filename, pagesize=letter)
        self.width, self.height = letter
        self.y_position = self.height - 60  # Starting Y position for text with more top margin

    def close_spider(self, spider):
        # Save and close the PDF
        self.c.save()

    def process_item(self, item, spider):
        # Write each scraped item (title, content, and URL) to the PDF
        title = item.get("title", "No title")
        content = item.get("content", "No content available")
        url = item.get("url", "No URL")

        # Add title to PDF with larger font size and bold styling
        self.c.setFont("Helvetica-Bold", 16)
        self.c.drawString(40, self.y_position, f"Title: {title}")
        self.y_position -= 30  # Extra space after title

        # Draw a separator line below the title for better readability
        self.c.setStrokeColor(grey)
        self.c.line(40, self.y_position, self.width - 40, self.y_position)
        self.y_position -= 20

        # Add URL in a smaller font for secondary information
        self.c.setFont("Helvetica-Oblique", 10)
        self.c.setFillColor(grey)
        self.c.drawString(40, self.y_position, f"URL: {url}")
        self.c.setFillColor(black)
        self.y_position -= 20

        # Add content with line wrapping and page management
        self.c.setFont("Helvetica", 12)
        content_lines = content.splitlines()

        for line in content_lines:
            if self.y_position < 50:  # Check if we need a new page
                self.c.showPage()
                self.y_position = self.height - 60  # Reset y position with top margin
                self.c.setFont("Helvetica", 12)  # Reset font for new page

            # Wrap and indent each paragraph with improved readability
            wrapped_text = self.wrap_text(line, self.width - 80)
            for subline in wrapped_text:
                self.c.drawString(60, self.y_position, subline)  # Add indentation to each line
                self.y_position -= 16  # Line spacing for readability

        # Add extra spacing between articles for separation
        self.y_position -= 40

        return item

    def wrap_text(self, text, max_width):
        """Utility function to wrap text to fit within max width."""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            # Check if the current line fits within the max width
            if self.c.stringWidth(' '.join(current_line), "Helvetica", 12) > max_width:
                # If not, finalize the current line and start a new one
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]

        lines.append(' '.join(current_line))  # Add the last line
        return lines

