from sqlacodegen.codegen import CodeGenerator
import io
from database import SessionLocal,engine,metadata

def generate_model(engine, metadata, outfile = None):
    outfile = io.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata)
    generator.render(outfile)

generate_model(engine=engine, metadata=metadata, outfile='models.py')