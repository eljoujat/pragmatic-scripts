from plantweb.render import render_file


CONTENT = """
@startuml
actor Foo1
boundary Foo2
control Foo3
entity Foo4
database Foo5
Foo1 -> Foo2 : To boundary
Foo1 -> Foo3 : To control
Foo1 -> Foo4 : To entity
Foo1 -> Foo5 : To database
@enduml
"""


if __name__ == '__main__':

    infile = 'seq.puml'
    outfile = render_file(
        infile,
        renderopts={
            'engine': 'plantuml',
            'format': 'png'
        },
        cacheopts={
            'use_cache': False
        }
    )

    print('==> OUTPUT FILE:')
    print(outfile)