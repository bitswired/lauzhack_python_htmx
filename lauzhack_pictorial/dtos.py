from pydantic import BaseModel


class CreateUserDto(BaseModel):
    """
    Data Transfer Object for creating a new user.

    This class is used to define the required fields that should be provided
    by a client when creating a new user. It also provides automatic validation
    of the data structure when instantiated.

    Attributes:
        email (str): The email address of the user. Must be valid and unique.
        password (str): The password for the user account. Should be securely hashed
                        before storage, although hashing is not handled in this DTO
                        itself.

    Usage:
        - This DTO can be used in request parsing to ensure that only the necessary
          data is received and that it adheres to the specified format.
    """

    email: str
    password: str


class GenerateImageDto(BaseModel):
    """
    Data Transfer Object for generating an image based on provided prompt.

    This class encapsulates the information required to generate an image,
    ensuring that all necessary details are present and validated before
    processing the image generation task.

    Attributes:
        prompt (str): The textual description or prompt based on which an image
                      will be generated.

    Usage:
        - Utilize this DTO to validate and transfer data for image generation
          requests in the application.
    """

    prompt: str
