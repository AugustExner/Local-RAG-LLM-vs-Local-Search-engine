from itemadapter import ItemAdapter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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

        # Process content with headers, lists, and tables
        self.c.setFont("Helvetica", 12)
        self.format_content(content)

        # Add extra spacing between articles for separation
        self.y_position -= 40

        return item

    def format_content(self, content):
        """Parse content and adjust formatting for headers, lists, and tables."""
        lines = content.splitlines()
        in_table = False
        table_data = []

        for line in lines:
            if self.y_position < 50:  # Check if we need a new page
                self.c.showPage()
                self.y_position = self.height - 60  # Reset y position with top margin
                self.c.setFont("Helvetica", 12)  # Reset font for new page

            # Detect table start (simple heuristic, adapt as needed)
            if line.strip().startswith("["):
                in_table = True
                table_data = []
                continue
            elif line.strip().startswith("]"):
                # End of table - render table and reset
                in_table = False
                self.draw_table(table_data)
                table_data = []
                self.y_position -= 20
                continue

            if in_table:
                # Collect table rows
                table_data.append(line.strip())
            elif line.startswith("- "):  # Bullet point
                wrapped_lines = self.wrap_text("• " + line[2:], self.width - 80)
                for wrapped_line in wrapped_lines:
                    self.c.drawString(60, self.y_position, wrapped_line)
                    self.y_position -= 16
            else:  # Regular text or header
                wrapped_lines = self.wrap_text(line, self.width - 80)
                for wrapped_line in wrapped_lines:
                    self.c.drawString(50, self.y_position, wrapped_line)
                    self.y_position -= 16

    def draw_table(self, table_data):
        """Render table content as rows and columns in the PDF."""
        self.c.setFont("Helvetica", 10)
        for row in table_data:
            columns = row.split("|")  # Assuming "|" is the column separator
            x_position = 60
            for column in columns:
                self.c.drawString(x_position, self.y_position, column.strip())
                x_position += 100  # Adjust column width as necessary
            self.y_position -= 14  # Move to the next row

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
