from bs4 import BeautifulSoup
import requests
import webbrowser
import os

class SVGExtractor():
    def __get_page(self, page):
        """
        Takes in a url to a page as a string and returns the BeautifulSoup
        """
        print('Getting the page you requested...')
        response = requests.get(page)
        response.raise_for_status()
        print('Page retrieved succesfully\n')
        html = BeautifulSoup(response.text, features="lxml")
        
        return html
    
    def __get_svgs(self, soup):
        """
        Takes in the BeautifulSoup object and returns all svg elements with their width and height info in JSON format
        """
        svgs = soup.select('svg')
        svg_json = {}
        for svg in range(len(svgs)):
            svg_json[svg] = {}
            svg_json[svg]['html'] = svgs[svg]

            if 'viewbox' in svgs[svg].attrs:
                _ = svgs[svg].attrs['viewbox']
                if ',' in _:
                    svg_json[svg]['width'] = _.split(',')[-2]
                    svg_json[svg]['height'] = _.split(',')[-1]
                else:
                    svg_json[svg]['width'] = _.split()[-2]
                    svg_json[svg]['height'] = _.split()[-1]

            elif 'width' in svgs[svg].attrs or 'height' in svgs[svg].attrs:
                svg_json[svg]['width'] = svgs[svg].attrs.get('width', 'auto')
                svg_json[svg]['height'] = svgs[svg].attrs.get('height', 'auto')
            
            else:
                svg_json[svg]['width'] = 'auto'
                svg_json[svg]['height'] = 'auto'

            assert svg_json[svg]['width'].isnumeric() or svg_json[svg]['width'] == 'auto'
            assert svg_json[svg]['height'].isnumeric() or svg_json[svg]['height'] == 'auto'
            print('SVGs extracted successfully\n')
        return svg_json
    
    def __write_html(self, svg_json, file_name):
        """
        Takes in a file name and a JSON object of the svgs found and writes the svgs to an HTML file
        """
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
                            align-items: center;
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
        
        with open(os.path.join(os.getcwd(), 'extracted', file_name), 'w') as file:
            file.write(metadata)
            
            for key in svg_json:
                file.write(f'<div class="svg-element" style="width:{svg_json[key]["width"]};height:{svg_json[key]["height"]}">\n')
                file.write(str(svg_json[key]['html']))
                file.write('</div>\n')
            
            file.write('</body></html>')
        
        print('HTML file written successfully\n')
            
        
    def extract(self, page, file_name, open_html = True):
        """
        Takes in the url to a page and extracts all the <svg> elements on the page.
        
        args-
        page:str - The url to a page to extract <svg> elements from
        file_name:str - The file name to save it as (without the extension, the script sets the extension as html automatically)
        open_html:bool - Opens the extracted svgs in a browser if True
        """
        html = self.__get_page(page)
        svg_json = self.__get_svgs(html)
        self.__write_html(svg_json, file_name)
        
        if open_html:
            print('Opening the created html file')
            #Get the path
            path = os.path.join(os.getcwd(), 'extracted', file_name)
            #Open html file in the default browser
            webbrowser.open(path)

if __name__ == "__main__":
    svge = SVGExtractor()
    print('\n\nSVGExtractor does not work 100% accurately for all pages yet, most notably for pages which animate their SVGs.\nIf you find an issue please report it on GitHub at https://www.github.com/hrushikeshrv/svgextract\n\n')

    continue_flag = True
    while continue_flag:
        page = input('Enter the direct url to the webpage you want to extract svgs from. - ')
        file_name = input("Enter a name to save the file as (WITHOUT the extension, the extension will be set to .html automatically) - ")
        flag = input('Do you want to open the extracted svgs when done? Y/n - ').lower().startswith('y')

        svge.extract(page, file_name + '.html', flag)
        
        continue_flag = input("Do you want to extract again? Y/n - ").lower().startswith('y')