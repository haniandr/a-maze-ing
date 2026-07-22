from pydantic import Field, BaseModel, model_validator
import random
from typing import Any


class ValidFileInput(BaseModel):
    width: int = Field(ge=0, le=200)
    height: int = Field(ge=0, le=200)
    entry_x: int = Field(ge=0, le=200)
    entry_y: int = Field(ge=0, le=200)
    exit_x: int = Field(ge=0, le=200)
    exit_y: int = Field(ge=0, le=200)
    output_filename: str
    is_perfect: bool
    seed: int
    display_solution: bool

    # Create a pattern if there is None
    @model_validator(mode="before")
    @classmethod
    def transform_input(cls, data: dict[str, Any]) -> dict[str, Any]:
        if data.get("seed") == "None":
            data["seed"] = random.randint(0, 1000000000)
        return data

    """
    check the OUTPUT_FILE is a file ".txt",
    check the entry and exit are not overflowed the grid
    width and height must be more 2 cells
    """
    @model_validator(mode="after")
    def validate_input(self) -> "ValidFileInput":
        """
        Validate maze configuration constraints.

        Checks output filename format, entry and exit positions,
        and ensures maze dimensions are large enough.
        """
        if "." not in self.output_filename:
            raise ValueError("File input is invalid : no '.' detected")
        name, ext = self.output_filename.split(".", 1)
        if not name or ext != "txt":
            raise ValueError(
                "File input is invalid : wrong output file name"
            )

        if self.entry_x == self.exit_x and self.entry_y == self.exit_y:
            raise ValueError(
                "The maze entry and exit can't be in the same cell"
            )

        if self.entry_x >= self.width or self.entry_y >= self.height:
            raise ValueError(
                "The maze entry needs to be inside the maze"
            )

        if self.exit_x >= self.width or self.exit_y >= self.height:
            raise ValueError(
                "The maze exit needs to be inside the maze"
            )

        if self.width < 2:
            raise ValueError(
                "The maze width is too small to create a maze"
            )
        if self.height < 2:
            raise ValueError(
                "The maze height is too small to create a maze"
            )
        return self
