import io
import os
import latextools
import subprocess


def latex_to_pdf(tex):
    # Takes latex string and converts it to pdf
    expression = r'${tex}$'.format(tex=tex)
    snippet = latextools.render_snippet(expression, commands=[latextools.cmd.all_math])
    snippet.save('temp.pdf')


def pdf_to_png(source="temp.pdf", output_file="temp.png"):
    # latextools function adapted to work on Windows_
    cwd = os.getcwd()
    args = f'inkscape -z -D --export-dpi=300 --export-png={output_file} ' + source
    try:
        proc = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        # return 'File not found'
        pass
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        msg = ''
        if stdout:
            msg += stdout.decode()
        if stderr:
            msg += stderr.decode()
        raise RuntimeError(msg)


#latex_to_pdf(r'\frac{x^2+5x+123}{y^6+45y-546}')
#pdf_to_png()




