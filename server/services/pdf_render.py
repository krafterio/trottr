import os
import subprocess
import tempfile
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi import HTTPException
from core.config import get_settings

class PDFRenderService:
    
    def __init__(self):
        self.settings = get_settings()
        self.template_path = os.path.join(self.settings.project_dir, "templates", "pdf")
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_path),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    def render_template(self, template_name: str, context: dict) -> str:
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)
    
    def get_chromeless_bin_path(self) -> str:
        chromeless_bin = os.environ.get('CHROMELESS_BIN_PATH')
        if not chromeless_bin:
            possible_paths = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '/usr/bin/google-chrome',
                '/usr/bin/chromium-browser',
                '/snap/bin/chromium',
                'google-chrome',
                'chromium-browser',
                'chromium'
            ]
            for path in possible_paths:
                if os.path.isfile(path):
                    chromeless_bin = path
                    break
                else:
                    try:
                        result = subprocess.run(['which', path.split('/')[-1]], capture_output=True, text=True)
                        if result.returncode == 0:
                            chromeless_bin = result.stdout.strip()
                            break
                    except:
                        continue
        
        if not chromeless_bin:
            raise HTTPException(status_code=500, detail="Chrome/Chromium binary not found. Installez Chrome ou définissez CHROMELESS_BIN_PATH")
        
        return chromeless_bin
    
    async def generate_pdf(self, template_name: str, context: dict, output_filename: str = None) -> str:
        try:
            # Générer le contenu principal
            main_content = self.render_template(template_name, context)
            
            # Générer le header
            header_content = self.render_template('header.html', context)
            
            # Générer le footer  
            footer_content = self.render_template('footer.html', context)
            
                        # Intégrer header et footer dans le HTML principal avec CSS @page pour répétition
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    @page {{
                        size: A4;
                        margin: 2cm 1.5cm;
                        @top-center {{
                            content: element(pageHeader);
                        }}
                        @bottom-center {{
                            content: element(pageFooter);
                        }}
                    }}
                    
                    .page-header {{
                        position: running(pageHeader);
                        width: 100%;
                        border-bottom: 1px solid #ccc;
                        padding-bottom: 10px;
                        margin-bottom: 10px;
                    }}
                    
                    .page-footer {{
                        position: running(pageFooter);
                        width: 100%;
                        border-top: 1px solid #ccc;
                        padding-top: 10px;
                        margin-top: 10px;
                        font-size: 10px;
                    }}
                    
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        font-size: 12px;
                        color: #333;
                        line-height: 1.5;
                    }}
                    
                    .main-content {{
                        margin: 0;
                        padding: 0;
                    }}
                </style>
            </head>
            <body>
                <div class="page-header">
                    {header_content}
                </div>
                <div class="page-footer">
                    {footer_content}
                </div>
                <div class="main-content">
                    {main_content}
                </div>
            </body>
            </html>
            """
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Template rendering failed: {str(e)}")
        
        # Debug: vérifier la valeur de pdf_display
        print(f"DEBUG: pdf_display = {self.settings.pdf_display}")
        
        if self.settings.pdf_display:
            return html_content
        
        if not output_filename:
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                output_filename = temp_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_html:
            temp_html.write(html_content)
            temp_html_path = temp_html.name
        
        try:
            chromeless_bin = self.get_chromeless_bin_path()
            
            # UTILISER TES PARAMÈTRES EXACTS comme demandé
            cmd = [
                chromeless_bin,
                '--headless',
                '--incognito', 
                '--mute-audio',
                '--no-first-run',
                '--no-margins',
                '--enable-viewport',
                '--disable-gpu',
                '--disable-translate',
                '--disable-extensions',
                '--disable-sync',
                '--disable-default-apps',
                '--hide-scrollbars',
                '--print-to-pdf-no-header',
                f'--print-to-pdf={output_filename}',
                f'file://{temp_html_path}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout or "Unknown error"
                raise HTTPException(
                    status_code=500, 
                    detail=f"PDF generation failed (code {result.returncode}): {error_msg}"
                )
            
            if not os.path.exists(output_filename):
                raise HTTPException(
                    status_code=500, 
                    detail="PDF file was not created"
                )
            
            if os.path.getsize(output_filename) == 0:
                raise HTTPException(
                    status_code=500, 
                    detail="PDF file is empty"
                )
            
            return output_filename
                
        except Exception as e:
            if "HTTPException" in str(type(e)):
                raise
            raise HTTPException(status_code=500, detail=f"PDF generation error: {str(e)}")
        finally:
            if os.path.exists(temp_html_path):
                os.unlink(temp_html_path)
    
 