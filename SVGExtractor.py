from bs4 import BeautifulSoup
import requests
import webbrowser
import os

class SVGExtractor():
    def extract(self, page, file_name, open_html = True):
        """
        Takes in the URL to a page and extracts all the <svg> elements on that page.
        DOES NOT WORK 100% ACCURATELY FOR ALL PAGES
        
        args-
        page:str - The url to a page to extract svgs from
        file_name:str - The file name to save the extracted svgs as (WITHOUT the extension. The script sets the extension as .html automatically)
        open_html:bool - Opens the extracted svgs in browser if True
        """
        
        #Get the page
        print('Getting the page you requested')
        response = requests.get(page)

        #Check for errors
        response.raise_for_status()
        print('Page retrieved succesfully\n')

        #Convert the response into a BeautifulSoup object
        html = BeautifulSoup(response.text, features="lxml")
        #Select all the svg elements
        svgs = html.select('svg')
        #Convert each element in svgs from a bs4.element.Tag object to just a string
        svg_strings = [str(x) for x in svgs]
        print('SVGs extracted...\n')

        #Initialize the metadata to write to the html file
        metadata = f"""
            <html>
                <head>
                    <title>{file_name} - SVGExtractor</title>
                    <style>
                        html, body {{
                            background-color: rgb(128, 128, 128);
                            padding: 20px;
                            display: flex;
                            flex-flow: row wrap;
                            justify-content: center;
                            align-items: stretch;
                        }}
                        .svg-element {{
                            padding: 20px;
                            margin: 30px;
                            border: 3px solid rgb(252, 173, 3);
                            border-radius: 7px;
                        }}
                    </style>
                </head>
                <body>
        """

        #Open a file
        print(f'Writing to {file_name}.html')
        with open(file_name + '.html', 'w') as file:
            #Set the file up to be written to and add some styles
            file.write(metadata)
            #Write all extracted svgs to the file
            for svg in svg_strings:
                file.write('<div class="svg-element">\n')
                file.write(svg)
                file.write('</div>\n')
            
            #End the file by closing the body and html tags
            file.write('</body></html>')
        print('HTML file created\n')

        #Open the file if open_html is True
        if open_html:
            print("Opening the created html file\n\n")
            #Get the path
            path = os.path.join(os.getcwd(), file_name + '.html')
            #Open the file
            webbrowser.open(path)

if __name__ == "__main__":
    svge = SVGExtractor()
    print('\n\nSVGExtractor does not work 100% accurately for all pages yet.\nIf you find an issue please report it on GitHub at https://www.github.com/hrushikeshrv/svgextract\n\n')

    continue_flag = True
    while continue_flag:
        page = input('Enter the direct url to the webpage you want to extract svgs from.')
        file_name = input("Enter a name to save the file as (WITHOUT the extension, the extension will be set to .html automatically)")
        flag = input('Do you want to open the extracted svgs when done? Y/n')
        flag = flag.lower().startswith('y')

        svge.extract(page, file_name + '.html', flag)
        
        continue_flag = input("Do you want to extract again? Y/n")
        continue_flag = continue_flag.lower().startswith('y')