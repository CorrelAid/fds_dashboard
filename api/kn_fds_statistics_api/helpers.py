from sqlacodegen.codegen import CodeGenerator
import io

def generate_model(engine, metadata, outfile = None):
    outfile = io.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata)
    generator.render(outfile)