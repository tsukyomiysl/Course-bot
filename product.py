from dataclasses import dataclass

@dataclass(frozen=True)
class Course():
    id : int
    title : str
    description : str
    text : str
    price : int



PRODUCT = Course(
    id = 1,
    title=("ExampleGood"),
    description=("ExampleDescription"),
    text =("ExampleText"),
    price = 1
)


