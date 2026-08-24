class AppConstants:

    _instance: "AppConstants | None" = None

    DEFAULT_PER_PAGE: int = 4
    PER_PAGE_OPTIONS: list[int] = [2, 4, 8, 12]

    CART_SESSION_KEY: str = "cart"

    IMAGE_SIZE_SMALL: int = 400
    IMAGE_SIZE_LARGE: int = 1000
    IMAGE_SIZES: list[int] = [400, 1000]
    IMAGE_FORMAT: str = "WEBP"

    def __new__(cls) -> "AppConstants":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> "AppConstants":
        return cls()
