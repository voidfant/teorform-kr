from src.compiler import Compiler
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='UVM Assembler')
    parser.add_argument('--build-ast-verbose', '-v', action='store_true', help='Флаг вывода Абстрактного Синтаксического Дерева')
    
    return parser.parse_args()

def main():
    sample_code = """
    { Пример программы }
    program var
        x, y, z, result : %;
    begin
        { Присваивание }
        x as 10;
        y as 20;
        
        { Условный оператор }
        if x LT y then
            z as x plus y
        else
            z as x min y;
        
        { Цикл с фиксированным числом повторений }
        for x as 0 to 10 do
            y as y plus x;
        
        { Условный цикл }
        while x GT 0 do
            x as x min 1;
        
        { Ввод и вывод }
        read(x, y);
        write(z, result)
    end.
    """
    args = parse_args()
    Compiler.compile(sample_code, ast_verbose=args.build_ast_verbose)

if __name__ == "__main__":
    main()
