import os
#import aspose.words as aw

from ebooklib import epub
from ebooklib import mobi

def convert_mobi_to_epub(input_mobi_path, output_epub_path):
    book = mobi.Mobi(input_mobi_path)
    epub_book = epub.EpubBook()

    # Set metadata
    epub_book.set_title(book.title)
    epub_book.set_language(book.language)

    # Add chapters
    for i, item in enumerate(book.get_items()):
        content = item.get_content().decode('utf-8')
        epub_book.add_html(epub.EpubHtml(title=item.get_title(), file_name=f'chap_{i}.xhtml', content=content))

    # Add other resources
    epub_book.add_metadata('DC', 'description', book.get_description())
    epub_book.add_author(book.get_author())

    # Write to output EPUB file
    epub.write_epub(output_epub_path, epub_book, {})


def mobi_epub(input_dir):
    dirs = os.listdir(input_dir)
    for d in dirs:
        files = os.listdir(d)
        for f in files:
            # Check if the file has the '.mobi' extension
            if f.endswith('.mobi'):
                input_mobi_path = f
                output_epub_path = "{f}.epub"
                convert_mobi_to_epub(input_mobi_path, output_epub_path)

                #output = aw.Document()
                # Remove all content from the destination document before appending.
                #output.remove_all_children()
                #for fileName in fileNames:
                #input = aw.Document(f)
                # Append the source document to the end of the destination document.
                #output.append_document(input, aw.ImportFormatMode.KEEP_SOURCE_FORMATTING)

                #output.save(f"{f}.epub");



if __name__ == "__main__":
    org_files = input("Org ebooks? y/n?")
    if org_files == "y":
        input_directory = input("Enter directory, e.g.: /media/HD_1/Media/books/Jacqueline - Copy ")
        try:
            mobi_epub(input_directory)
        except:
            print("Invalid path")