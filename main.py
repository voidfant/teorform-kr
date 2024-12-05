from src.compiler import Compiler


def main():
    sample_code = """
    {Пример программы с новым функционалом}
    program var
        x, y, z, result : %;
    begin
        {Присваивание}
        x as 10;
        y as 20;
        
        {Условный оператор}
        if x LT y then
            z as x plus y
        else
            z as x min y;
        
        {Цикл с фиксированным числом повторений}
        for x as 0 to 10 do
            y as y plus x;
        
        {Условный цикл}
        while x GT 0 do
            x as x min 1;
        
        {Ввод и вывод}
        read(x, y);
        write(z, result)
    end.
    """
    
    Compiler.compile(sample_code)

if __name__ == "__main__":
    main()
